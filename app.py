from fastapi import FastAPI
from pydantic import BaseModel, Field, constr
import json
from urllib import request
import random
import uuid

app = FastAPI()
api_url = "http://127.0.0.1:8188/prompt"
# completed workflows write output images to this directory
output_dir = "./comfyui/output"

# Pydantic model for user input
class PromptParams(BaseModel):
    positive_text: constr(min_length=3)  # Require a min text length
    negative_text: str = Field(default=None)
    seed: int = Field(default=None)
    height: int = Field(default=None, le=768)  # Max height
    width: int = Field(default=None, le=768)   # Max width

def load_default_prompt():
    with open("defaults.json", "r") as file:
        return json.load(file)

# Queue the prompt via ComfyUI API
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request(api_url, data=data)
    request.urlopen(req)

def wait_for_image(file_prefix):
    # returns the image as bytes
    for f in Path(output_dir).iterdir():
        if f.name.startswith(file_prefix):
            return f.read_bytes()

# API route to receive and queue prompts with overrides
@app.post("/submit-prompt/")
def submit_prompt(params: PromptParams):
    from fastapi import Response

    # Load default prompt structure from file
    prompt = load_default_prompt()

    # Positive text is required and must be at least 3 characters
    if not params.positive_text or len(params.positive_text) < 3:
        raise HTTPException(status_code=400, detail="Positive text must be at least 3 characters long.")

    # Positive text is required and must be at least 3 characters
    if not params.seed:
        params.seed = random.randint(0, 10000)  # Random seed

    # Override the parameters based on user input
    if params.positive_text:
        prompt["6"]["inputs"]["text"] = params.positive_text
    if params.negative_text:
        prompt["7"]["inputs"]["text"] = params.negative_text
    if params.seed is not None:
        prompt["3"]["inputs"]["seed"] = params.seed
    if params.height is not None:
        prompt["5"]["inputs"]["height"] = params.height
    if params.width is not None:
        prompt["5"]["inputs"]["width"] = params.width

    # give the output image a unique id per client request
    client_id = uuid.uuid4().hex
    prompt["9"]["inputs"]["filename_prefix"] = client_id

    # Queue the prompt via ComfyUI
    queue_prompt(prompt)
    #return {"status": f"Prompt submitted with seed: {params.seed}"}

    img_bytes = wait_for_image(file_prefix)
    return Response(img_bytes, media_type="image/jpeg")
