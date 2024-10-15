# Wrapper for CompyUI

## Prereqs

* https://github.com/astral-sh/uv
* https://github.com/astral-sh/ruff


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
```
