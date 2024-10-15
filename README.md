# Wrapper for CompyUI

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
* Code
    * DONE - Add ComfyUI (using git submodules)
    * Pick a model
        * Keep track of what is unique to this model and what requirements are specific (to potentially change or generalize)
    * Write wrapper

* Containerize
* Determine hosting, deployment, and development model
    * docker, docker-compose, git triggers
* Tests
    * Unit
    * Integration
    * Deployment stopping
    * Load / Performance
    * Cost


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
