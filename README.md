# 4× GAN Image Upscaler

**AI-powered image super-resolution using an ESRGAN-inspired generator.**

Upscale images to 4× their original resolution with a trained RRDB-based GAN, powered by PyTorch and served through a FastAPI backend with an interactive web interface.

<p align="center">
  <strong>Deep Learning · Computer Vision · Super-Resolution · FastAPI</strong>
</p>

---

## Overview

This project explores single-image super-resolution: reconstructing a higher-resolution image from a lower-resolution input.

The model uses Residual-in-Residual Dense Blocks (RRDBs), dense feature connections, and adversarial training to generate enhanced images at 4× spatial resolution.

The project combines model development with a usable application, allowing users to select images, run inference, and compare the original and upscaled results.

## Features

| Feature | Description |
|---|---|
| **4× Upscaling** | Increases image width and height by 4× |
| **RRDB Generator** | Dense residual feature extraction |
| **GAN Training** | Adversarial learning with multiple reconstruction and perceptual losses |
| **Interactive UI** | Image selection and before/after comparison slider |
| **FastAPI Backend** | API endpoints for inference and image management |
| **Model Evaluation** | PSNR, SSIM, and LPIPS evaluation workflow |

## Preview

<!-- Add screenshots here after capturing the working application. -->

<p align="center">
  <em>Application interface and upscaling results coming soon.</em>
</p>

## Model Architecture

The generator is inspired by ESRGAN and consists of:

- **16 RRDB blocks** for deep feature extraction
- **64 feature channels** throughout the main feature trunk
- Residual Dense Blocks with densely connected convolutional layers
- Two PixelShuffle ×2 stages for 4× upsampling
- A PatchGAN discriminator used during adversarial training

Training incorporates Charbonnier reconstruction, VGG perceptual, edge-aware, SSIM-based, and adversarial losses. Synthetic degradation—including blur, noise, JPEG compression, and bicubic downsampling—is used to create degraded training inputs.

The model was trained for **600 epochs**.

*This is an ESRGAN-inspired implementation, not an exact reproduction of the original ESRGAN architecture.*

## Tech Stack

**Machine Learning**
- Python
- PyTorch
- Torchvision

**Backend**
- FastAPI
- Uvicorn
- Pillow

**Frontend**
- HTML
- CSS
- JavaScript

## Getting Started

### Prerequisites

- Windows
- Python 3.11, or Miniconda/Anaconda
- The trained model checkpoint

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/image-upscaler-using-GAN.git
cd image-upscaler-using-GAN
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Download the model

Download `checkpoint_gan_epoch_600.pth` from the model link below and place it in the project root, next to `app.py`.

**Model weights:** TODO — add download link.

### 3. Install and run

<details>
<summary><strong>Option A — Standard Python (Windows)</strong></summary>

Install Python 3.11, then run:

```bat
start.bat
```

The launcher creates a project-local `.venv` environment and installs the dependencies on first launch. Subsequent launches reuse the environment.

</details>

<details>
<summary><strong>Option B — Conda</strong></summary>

Create the environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate imageupscaler
```

Start the server:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

</details>

### 4. Open the application

Navigate to:

**http://127.0.0.1:8000/app**

Place images in `input_images/`, select them in the interface, and run the upscaling process. Generated results are saved in `upscaled_images/`.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and model information |
| `GET` | `/images` | List input images |
| `POST` | `/upscale/{filename}` | Upscale an image |
| `GET` | `/upscaled` | List generated images |
| `GET` | `/app` | Serve the web interface |

Interactive API documentation is available at `/docs` while the server is running.

## Evaluation

The evaluation workflow supports three complementary metrics:

- **PSNR** — pixel-level reconstruction fidelity
- **SSIM** — structural similarity
- **LPIPS** — perceptual similarity using deep features

Evaluation datasets used in the project include Set5, Set12, Set14, BSD100, Urban100, General100, and Manga109.

Quantitative results and baseline comparisons will be documented when the final measurements are added.

## Repository Structure

```text
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

The trained checkpoint is distributed separately rather than committed to Git.

## Limitations

- Inference speed depends on hardware and image dimensions.
- GAN-generated details may look plausible without matching the original scene exactly.
- Results vary with image content and degradation.
- The checkpoint must be downloaded separately before running the application.

## Future Work

- Benchmark against established super-resolution baselines
- Document quantitative results and visual comparisons
- Improve inference performance and GPU support
- Expand batch-processing and image-format support

## License

No license has been specified yet. Add an appropriate license before granting permissions for reuse or redistribution.