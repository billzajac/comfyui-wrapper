# Wrapper for ComfyUI

* https://github.com/comfyanonymous/ComfyUI

## Questions


## TODO

* DONE - Learn and understand more about ComfyUI
* DONE - Determine package management system
    * uv
    * fallback (poetry - awkward with Docker)
* DONE - Decide how to manage the ComfyUI github repo
    * git submodule (this will allow for the most straightforward way to independently manage)
* DONE - Pick a linting / pretty standard
    * ruff (with I)
* DONE - Learn how to get pytorch working on Mac M2
* DONE - Choose a CSS Framework
    * Tailwind CSS
* Code
    * DONE - Add ComfyUI (using git submodules)
    * Pick model
        * https://comfyui-wiki.com/resource/stable-diffusion-models
        * https://civitai.com/
            * https://civitai.com/models/62437/v1-5-pruned-emaonly
        * https://huggingface.co/models

        * Keep track of what is unique to this model and what requirements are specific (to potentially change or generalize)
    * Fork and hack the frontend (Future, look into alternative UIs listed here: https://www.comfy.org/)
        * https://github.com/Comfy-Org/ComfyUI_frontend
        * https://github.com/mcmonkeyprojects/SwarmUI
    * Write wrapper


* API documentation
    * Use Swagger to autogenerate
* Choose a gitflow branching strategy
    * https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/gitflow-branching-strategy.html
* Containerize
* Determine hosting, deployment, and development model
    * docker, docker-compose, git triggers
    * https://docs.astral.sh/uv/guides/integration/docker/
* Tests
    * Unit
    * Integration
    * Deployment stopping
    * Load / Performance
    * Cost
* Logging
* Metrics
* User accounts and SSO
* Save workflow files per user and request (and allow load)
* Enable high quality previews
    * https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#how-to-show-high-quality-previews


## Prereqs

* https://github.com/astral-sh/uv
* https://github.com/astral-sh/ruff

### uv Cheat Sheet

* https://docs.astral.sh/uv/getting-started/features/#tools


## Initial Build

```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init comfyui-wrapper
cd comfyui-wrapper
uv add ruff
# add tool.ruff.lint to pyproject.toml
# Note: needed --frozen
uv add --prerelease allow --index-url https://download.pytorch.org/whl/nightly/cpu --frozen torch torchvision torchaudio
# re-sync and lock due to frozen flag above
uv sync
uv lock
git submodule add git@github.com:comfyanonymous/ComfyUI.git comfyui
uv add --requirements comfyui/requirements.txt
uv add fastapi uvicorn
```

### Test pytorch on Apple Silicon

```
uv run python

import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")
```

## Working with ComfyUI as a git submodule

### After cloning this repo

```
git submodule init
git submodule update
```

### To pull the latest changes from ComfyUI

```
cd comfyui
git pull origin main
```

## New Development Env

* Install uv
    * https://docs.astral.sh/uv/getting-started/installation/

```
git clone git@github.com:billzajac/comfyui-wrapper.git
cd comfyui-wrapper
git submodule init
git submodule update
uv sync

# Download the model from: https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-archive/resolve/main/v1-5-pruned-emaonly.safetensors?download=true
# Save it to: comfyui/models/checkpoints
```

* To run things, you can use

```
uv run ...
```

or 

```
uv sync
source .venv/bin/activate
...
```


## ComfyUI

```
uv run comfyui/main.py --preview-method auto
```
