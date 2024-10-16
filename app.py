import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
import json
from urllib import request
import random
import uuid
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve the API URL and output directory from environment variables
api_url = os.getenv("API_URL")
output_dir = os.getenv("OUTPUT_DIR")


# Pydantic model for user input
class PromptParams(BaseModel):
    positive_text: constr(min_length=3)  # Require a min text length
    negative_text: str = Field(default=None)
    seed: int = Field(default=None)
    height: int = Field(default=None, le=768)  # Max height
    width: int = Field(default=None, le=768)   # Max width
    wait_for_image: bool = Field(default=False)

def load_default_prompt():
    with open("defaults.json", "r") as file:
        return json.load(file)

# Queue the prompt via ComfyUI API
def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request(api_url, data=data)
    request.urlopen(req)

def wait_for_image(file_prefix, timeout=180, poll_interval=5):
    """Poll the output directory for the generated image file."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Check for the file in the output directory
        for f in Path(output_dir).iterdir():
            if f.name.startswith(file_prefix) and f.suffix in [".jpg", ".jpeg", ".png"]:
                return f.read_bytes()  # Return image bytes if the file is found
        time.sleep(poll_interval)  # Wait for the next poll

    # If the image is not found within the timeout period, raise an error
    raise HTTPException(status_code=408, detail="Image generation timed out.")

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

    # Check if we should wait for the image or not
    if params.wait_for_image:
        # Wait for the generated image (timeout after 180 seconds)
        img_bytes = wait_for_image(client_id)
        return Response(img_bytes, media_type="image/jpeg")
    else:
        # Simply return confirmation that the request was submitted
        return {"status": "Prompt submitted successfully.", "seed": params.seed, "client_id": client_id}
    #return {"status": f"Prompt submitted with seed: {params.seed}"}

    img_bytes = wait_for_image(client_id)
    return Response(img_bytes, media_type="image/jpeg")
