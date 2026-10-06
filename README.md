::: {align="center"}
# 4× GAN Image Upscaler

### Deep Learning · Computer Vision · Image Super-Resolution

**Turn low-resolution images into 4× larger images with a trained
RRDB-based GAN.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Upscaling](https://img.shields.io/badge/Upscaling-4%C3%97-7C3AED)](#how-it-works)
[![Model](https://img.shields.io/badge/Model-Hugging%20Face-yellow?logo=huggingface&logoColor=black)](https://huggingface.co/coolknifer333444/image-upscaler-gan)

[**Get the Model
Weights**](https://huggingface.co/coolknifer333444/image-upscaler-gan) ·
[**API Docs**](#api-reference) · [**Installation**](#getting-started)
:::

------------------------------------------------------------------------

## ✨ Highlights

-   🖼️ **4× super-resolution** --- increases both image width and height
    by four.
-   🧠 **RRDB-based generator** --- an ESRGAN-inspired architecture
    trained for image reconstruction.
-   🌐 **Interactive web interface** --- select images, run upscaling,
    and compare results with a before/after slider.
-   ⚡ **FastAPI backend** --- inference endpoints and interactive API
    documentation.
-   📊 **Evaluation workflow** --- supports PSNR, SSIM, and LPIPS
    metrics.
-   📦 **One-click Windows launch** --- installs dependencies and
    downloads the checkpoint automatically.

## Overview

This project explores **single-image super-resolution**: reconstructing
a higher-resolution image from a lower-resolution input. It combines a
trained PyTorch GAN with a FastAPI service and a browser-based
interface.

The generator uses Residual-in-Residual Dense Blocks (RRDBs), dense
feature connections, and two PixelShuffle upsampling stages to produce a
4× output.

> **Note:** This is an ESRGAN-inspired implementation, not an exact
> reproduction of the original ESRGAN architecture.

## 🖥️ Preview

```{=html}
<!-- Replace these placeholders with screenshots of the real application and actual before/after results. -->
```
::: {align="center"}
  -----------------------------------------------------------------------
         Application interface              Original vs. 4× result
  ----------------------------------- -----------------------------------
    *Add a screenshot of the web UI     *Add a before/after comparison
                 here*                               here*

  -----------------------------------------------------------------------
:::

## 🧠 How It Works

### Generator architecture

``` text
Low-Resolution Image
        │
        ▼
   Input Convolution
        │
        ▼
  16 × RRDB Blocks
  (64 feature channels)
        │
        ▼
  Feature Convolution
        │
        ▼
 PixelShuffle ×2
        │
        ▼
 PixelShuffle ×2
        │
        ▼
 Output Convolution
        │
        ▼
4× Super-Resolved Image
```

The model was trained for **600 epochs**.

**Training components** - Charbonnier reconstruction loss - VGG
perceptual loss - Edge-aware loss - SSIM-based loss - Adversarial loss
with a PatchGAN discriminator

Synthetic degradation includes bicubic downsampling, blur, noise, and
JPEG compression.

## 🧰 Tech Stack

  Area               Technologies
  ------------------ ------------------------------------------------------------
  Deep learning      Python, PyTorch, Torchvision
  Model              RRDB-based generator, PatchGAN discriminator, PixelShuffle
  Backend            FastAPI, Uvicorn
  Image processing   Pillow
  Frontend           HTML, CSS, JavaScript
  Model hosting      Hugging Face

## 🚀 Getting Started

### Requirements

-   Windows for the one-click `start.bat` workflow
-   Python or Conda
-   Internet access for initial dependency and model downloads
-   Approximately 184 MB for the checkpoint, plus space for dependencies
    and images

### Option A --- Windows Quick Start

**Recommended if you just want to run the app.**

1.  Clone the repository:

    ``` bash
    git clone https://github.com/coolknifer333444/image-upscaler-using-GAN.git
    cd image-upscaler-using-GAN
    ```

2.  Run `start.bat` from the project folder.

3.  On first launch, the script creates a project-local `.venv`,
    installs `requirements.txt`, downloads the checkpoint if missing,
    starts the API, and opens the web interface.

4.  Open <http://127.0.0.1:8000/app>.

Later launches reuse the existing environment and checkpoint. The
launcher uses its own `.venv`, even if a Conda environment is active.

### Option B --- Conda

**1. Clone the repository**

``` bash
git clone https://github.com/coolknifer333444/image-upscaler-using-GAN.git
cd image-upscaler-using-GAN
```

**2. Create and activate the environment**

``` bash
conda env create -f environment.yml
conda activate imageupscaler
```

**3. Download the model checkpoint**

Run this in PowerShell from the project root:

``` powershell
Invoke-WebRequest `
  -Uri "https://huggingface.co/coolknifer333444/image-upscaler-gan/resolve/main/checkpoint_gan_epoch_600.pth" `
  -OutFile "checkpoint_gan_epoch_600.pth"
```

The checkpoint must be in the project root beside `app.py`.

**4. Start the server**

``` bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000/app>.

### Option C --- Standard Python virtual environment

Create and activate a virtual environment on Windows:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` bash
python -m pip install -r requirements.txt
```

Download the checkpoint using the PowerShell command in **Option B**,
then start the server:

``` bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

> **Checkpoint location:** `checkpoint_gan_epoch_600.pth` belongs in the
> project root beside `app.py`. It is hosted separately and is not
> stored in Git.

## 🕹️ Using the App

1.  Launch the application using one of the methods above.
2.  Open the web interface.
3.  Add or select images in the interface. The project uses
    `input_images/` for input files.
4.  Run the 4× upscaling process.
5.  View generated results in the interface. Outputs are saved in
    `upscaled_images/`.

For example, a 256 × 256 input produces a 1024 × 1024 output.

Inference speed depends on hardware and image dimensions. CPU inference
is supported but may take several seconds per image.

## 🔌 API Reference

   Method  Endpoint                Purpose
  -------- ----------------------- ----------------------------------
   `GET`   `/`                     API status and model information
   `GET`   `/images`               List available input images
   `POST`  `/upscale/{filename}`   Upscale a selected image
   `GET`   `/upscaled`             List generated output images
   `GET`   `/app`                  Serve the web interface
   `GET`   `/docs`                 Interactive API documentation

The server listens on `127.0.0.1:8000` with the launch instructions
above.

## 📈 Evaluation

The evaluation workflow supports:

-   **PSNR** --- pixel-level reconstruction fidelity
-   **SSIM** --- structural similarity
-   **LPIPS** --- perceptual similarity using deep features

Datasets used in the workflow include Set5, Set12, Set14, BSD100,
Urban100, General100, and Manga109.

Quantitative scores and baseline comparisons are omitted until final
measurements are documented.

## 📁 Project Structure

``` text
Image_Upscaler/
├── static/
│   └── index.html
├── input_images/
├── upscaled_images/
├── app.py
├── model.py
├── requirements.txt
├── environment.yml
├── start.bat
├── .gitignore
└── README.md
```

The trained checkpoint is downloaded separately from Hugging Face.

## ⚠️ Limitations

-   GAN-generated details can look plausible without perfectly matching
    the original scene.
-   Results vary with image content and input quality.
-   Large images require more processing time and memory.
-   CPU inference works but can be slower than GPU inference.
-   The project does not claim state-of-the-art results; benchmark
    scores should be assessed alongside visual quality.

## 🛣️ Future Work

-   Add documented benchmark results and baseline comparisons.
-   Include real application and before/after screenshots.
-   Improve inference speed and GPU support.
-   Expand image-format handling and batch-processing options.

## 👤 Author

**Ishan Lodwal**\
GitHub: [@coolknifer333444](https://github.com/coolknifer333444)

------------------------------------------------------------------------

::: {align="center"}
**Built as a deep learning and computer vision project.**
:::
