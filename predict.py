import os
import json
from pathlib import Path
from comfy.cli_args import args
import server
import sys
sys.path.append('/workspace/ComfyUI')

# ComfyUI setup
args.output_directory = "/workspace/ComfyUI/output"
server.setup()

# Load workflow template
WORKFLOW_PATH = Path("/workspace/ComfyUI/workflows/prompt_to_image.json")
with open(WORKFLOW_PATH, "r") as f:
    workflow = json.load(f)

def predict(prompt: str = "a photo of a fantasy landscape"):
    # Inject prompt into workflow
    for node in workflow["nodes"]:
        if node["type"] == "CLIPTextEncode":
            node["inputs"]["text"] = prompt

    # Run workflow
    result = server.api_queue_prompt(workflow)

    # Return output image path
    output_image = result["ui"]["images"][0]["filename"]
    return os.path.join(args.output_directory, output_image)

# Example usage
if __name__ == "__main__":
    out = predict("a cyberpunk city at night, ultra detailed")
    print("Image generated at:", out)
