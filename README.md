# VisionPort

> Real-time vision inference pipeline — object detection → API gateway → Streamlit dashboard.

## Codebase Tour (Module 1 — Session 4)

| Folder / File | What it will contain |
|---|---|
| `main.py` | Streamlit dashboard — live video feed and inference results display |
| `serve/gateway.py` | FastAPI gateway — receives frames, calls the model, returns detections |
| `serve/gateway_trace.py` | Request trace helper — logs latency and payload for each gateway call |
| `train/` | Model fine-tuning scripts and training configuration files |
| `eval/` | Evaluation scripts, metric plots, confusion matrices |
| `optimise/` | TensorRT / ONNX export and quantisation scripts |
| `models/` | Downloaded or exported model weights (not committed — see .gitignore) |
| `data/` | Sample images and annotation files for testing (not committed) |
| `docs/` | Architecture diagrams, session notes, and the env report |
| `failures/` | Logged inference failures and edge cases for review |
| `logs/` | Runtime logs produced by the gateway and training jobs |
| `env_check.py` | Prints and saves the Python / CUDA / package environment report |

## Quick Start

```bash
# 1. Activate the virtual environment
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the environment check
python env_check.py

# 4. Start the Streamlit app
streamlit run main.py

# 5. Start the FastAPI gateway (separate terminal)
uvicorn serve.gateway:app --reload
```

## Versions

| Tag | Description |
|-----|-------------|
| v0.1 | Session 4 — repo structure, environment check, first commit |

---
*Department: DLAC — VisionPort Project*
