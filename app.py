import os
import io
import torch

from PIL import Image
from torchvision import transforms

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from model import SuperResolver


CHECKPOINT_PATH = "checkpoint_gan_epoch_600.pth"
INPUT_DIR = "input_images"
OUTPUT_DIR = "upscaled_images"


os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


app = FastAPI(
    title="Image Upscaler",
    description="4× GAN-based image super-resolution",
    version="1.0.0"
)


# --------------------------------------------------
# Device
# --------------------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

model = SuperResolver(
    in_channels=3,
    out_channels=3,
    num_features=64,
    num_blocks=16,
    scale=4
)

checkpoint = torch.load(
    CHECKPOINT_PATH,
    map_location=device
)

model.load_state_dict(
    checkpoint["generator_state_dict"]
)

model = model.to(device)
model.eval()


# --------------------------------------------------
# Static image folders
# --------------------------------------------------

app.mount(
    "/input-images",
    StaticFiles(directory=INPUT_DIR),
    name="input-images"
)

app.mount(
    "/upscaled-images",
    StaticFiles(directory=OUTPUT_DIR),
    name="upscaled-images"
)


# --------------------------------------------------
# API
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "running",
        "model": "GAN Super-Resolution",
        "scale": "4x",
        "device": str(device),
        "checkpoint_epoch": checkpoint["epoch"]
    }


@app.get("/images")
def get_images():

    images = []

    for filename in os.listdir(INPUT_DIR):

        if filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".webp")
        ):
            images.append(filename)

    return {
        "images": sorted(images)
    }


@app.post("/upscale/{filename}")
def upscale(filename: str):

    input_path = os.path.join(INPUT_DIR, filename)

    if not os.path.isfile(input_path):
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    # Load image
    image = Image.open(input_path).convert("RGB")

    # Convert to tensor
    lr = transforms.ToTensor()(
        image
    ).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        sr = model(lr).clamp(0.0, 1.0)

    # Convert back to image
    sr_image = transforms.ToPILImage()(
        sr.squeeze(0).cpu()
    )

    # Output filename
    base_name = os.path.splitext(filename)[0]

    output_filename = (
        f"{base_name}_upscaled.png"
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        output_filename
    )

    # Save
    sr_image.save(output_path)

    return {
        "status": "success",
        "input": filename,
        "output": output_filename,
        "input_size": image.size,
        "output_size": sr_image.size
    }


@app.get("/upscaled")
def get_upscaled():

    images = []

    for filename in os.listdir(OUTPUT_DIR):

        if filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".webp")
        ):
            images.append(filename)

    return {
        "images": sorted(images)
    }

@app.get("/app")
def web_app():
    return FileResponse("static/index.html")