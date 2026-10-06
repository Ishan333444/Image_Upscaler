\# 4× GAN Image Upscaler



An ESRGAN-inspired deep learning project that upscales images to \*\*4× their original resolution\*\* using a Residual-in-Residual Dense Block (RRDB) generator. The project includes a FastAPI backend and an interactive web interface for selecting images, running inference, and comparing original and upscaled results.



\## Features



\- \*\*4× super-resolution:\*\* Upscales images to four times their original width and height.

\- \*\*RRDB-based generator:\*\* Uses densely connected residual blocks to reconstruct image details.

\- \*\*GAN-based training:\*\* Combines reconstruction, perceptual, edge-aware, structural similarity, and adversarial losses.

\- \*\*Degradation-aware training:\*\* Uses synthetic degradation such as blur, noise, JPEG compression, and bicubic downsampling.

\- \*\*Interactive web interface:\*\* Select images, run upscaling, and compare original and enhanced results with a comparison slider.

\- \*\*FastAPI backend:\*\* Provides endpoints for image listing, upscaling, and retrieving generated results.

\- \*\*Evaluation workflow:\*\* Includes evaluation metrics such as PSNR, SSIM, and LPIPS.



\## Model Architecture



The generator is inspired by ESRGAN and uses:



\- 16 Residual-in-Residual Dense Blocks (RRDBs)

\- 64 feature channels

\- Dense feature connections within residual dense blocks

\- Two PixelShuffle ×2 upsampling stages to achieve 4× scaling

\- A PatchGAN discriminator during adversarial training



The model was trained for 600 epochs. This is an ESRGAN-inspired implementation, not an exact reproduction of the original ESRGAN architecture.



\## Tech Stack



\- Python

\- PyTorch and Torchvision

\- FastAPI

\- Uvicorn

\- Pillow

\- HTML, CSS, and JavaScript



\## Project Structure



```text

Image\_Upscaler/

├── static/

│   └── index.html

├── input\_images/

├── upscaled\_images/

├── app.py

├── model.py

├── requirements.txt

├── environment.yml

├── start.bat

├── .gitignore

└── README.md

```



The model checkpoint is distributed separately and is not included in the Git repository.



\## Requirements



\- Windows

\- Python 3.11 for the standard Python setup, or Miniconda/Anaconda

\- The trained model checkpoint

\- An internet connection for the initial dependency installation



CPU inference is supported. Performance depends on the hardware and image dimensions.



\## Installation



\### Option A: Standard Python



1\. Install Python 3.11.

2\. Clone this repository:



&#x20;  ```bash

&#x20;  git clone https://github.com/YOUR-USERNAME/image-upscaler-using-GAN.git

&#x20;  cd image-upscaler-using-GAN

&#x20;  ```



3\. Download the trained model checkpoint using the link in the \*\*Model Weights\*\* section below.

4\. Place `checkpoint\_gan\_epoch\_600.pth` in the project root, alongside `app.py`.

5\. Run:



&#x20;  ```bat

&#x20;  start.bat

&#x20;  ```



On first launch, the script creates a project-local `.venv` environment and installs the dependencies. Subsequent launches reuse that environment.



\### Option B: Conda



1\. Install Miniconda or Anaconda.

2\. Clone the repository and navigate into the project directory.

3\. Download the checkpoint and place it in the project root.

4\. Create the environment:



&#x20;  ```bash

&#x20;  conda env create -f environment.yml

&#x20;  ```



5\. Activate it:



&#x20;  ```bash

&#x20;  conda activate imageupscaler

&#x20;  ```



6\. Start the server:



&#x20;  ```bash

&#x20;  python -m uvicorn app:app --host 127.0.0.1 --port 8000

&#x20;  ```



7\. Open `http://127.0.0.1:8000/app` in your browser.



\## Model Weights



The trained checkpoint is too large to include directly in this Git repository.



\*\*Download:\*\* TODO — add the model checkpoint link here.



After downloading, place the file in the project root:



```text

Image\_Upscaler/

├── checkpoint\_gan\_epoch\_600.pth

├── app.py

└── model.py

```



The application expects the checkpoint filename `checkpoint\_gan\_epoch\_600.pth`.



\## Usage



1\. Start the application using `start.bat` or the Conda command above.

2\. Open the web interface in your browser.

3\. Add images to the `input\_images/` directory.

4\. Select the images you want to upscale.

5\. Run the upscaling process.

6\. View the results and use the comparison slider to inspect the original and upscaled images.



Generated images are saved in `upscaled\_images/`.



\## API Endpoints



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | API status and model information |

| GET | `/images` | List available input images |

| POST | `/upscale/{filename}` | Upscale a selected image |

| GET | `/upscaled` | List generated images |

| GET | `/app` | Open the web interface |



Interactive API documentation is available at `http://127.0.0.1:8000/docs` while the server is running.



\## Evaluation



The evaluation workflow uses:



\- \*\*PSNR:\*\* Measures pixel-level reconstruction error.

\- \*\*SSIM:\*\* Measures structural similarity.

\- \*\*LPIPS:\*\* Measures perceptual similarity using deep features.



Evaluation datasets used in the project include Set5, Set12, Set14, BSD100, Urban100, General100, and Manga109.



Quantitative results and benchmark comparisons can be added here once the final measurements are documented.



\## Limitations



\- Inference speed depends on hardware and image size.

\- GAN-based super-resolution may generate plausible details that were not present in the original image.

\- Results can vary depending on image content and degradation.

\- The trained checkpoint must be downloaded separately before running the application.



\## Future Improvements



\- GPU acceleration where supported by the installed PyTorch build.

\- Additional benchmark comparisons against established super-resolution models.

\- Support for additional image formats and larger batches.

\- Improved model distribution and setup automation.



\## License



Add a license before redistributing this project. Until a license is included, the repository should not be assumed to grant permission for reuse or redistribution.

