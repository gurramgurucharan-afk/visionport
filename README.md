# VisionPort

A GPU-trained, GPU-served vision system for Indian traffic.

## Current version

v0.1 - pretrained YOLOv8n demo, FastAPI gateway, request trace

## Codebase tour

| Part | Location | Will contain |
|------|----------|--------------|
| Data pipeline | `data/`, `train/dataset.py` | Loading COCO-format images and annotations, collate function |
| Training loop | `train/train.py` | Forward, loss, backward, optimiser step, scheduler, checkpointing |
| Architecture file | `train/model.py` | YOLO-style backbone, neck and head |
| Evaluation harness | `eval/` | mAP@0.5, latency and throughput measurement |
| Optimisation script | `optimise/` | ONNX export, TensorRT build, INT8 calibration |
| Triton config | `serve/triton/` | Model repository and `config.pbtxt` |

## Environment

Pinned package versions are in `requirements.txt`. Recreate with:

```
pip install -r requirements.txt
```

## How to run

```
uvicorn serve.gateway:app --reload
uvicorn serve.gateway_trace:app --reload
```

Then open `http://127.0.0.1:8000/docs`. The Streamlit demo is `app.py`.

## Known limitations

- Pretrained on COCO, not on Indian traffic. No auto-rickshaw class.

---

## Session 4 — Repository Setup & Environment

| Step | Command / File | Purpose |
|------|---------------|---------|
| Folder structure | `mkdir data models eval optimise serve train logs docs failures` | Project layout |
| Make serve a package | `serve/__init__.py` | Enables `uvicorn serve.gateway:app` |
| Environment check | `python env_check.py` | Prints Python, CUDA, package versions → `env_report.md` |
| Record versions | `pip freeze > requirements.txt` | Reproducible environment |
| First commit | `git commit -m "v0.1: ..."` | Tagged as `v0.1` |

### env_check.py output (this machine)

| Item | Value |
|------|-------|
| OS | Windows 11 |
| Python | 3.14.8 (.venv ✅) |
| streamlit | 1.67.0 |
| fastapi | 0.162.4 |
| torch | 2.15.0 |
| ultralytics | 8.4.210 |
| NVIDIA GPU | ❌ Not detected (CPU-only) |

---

## Session 5 — COCO Dataset Exploration

**Files:** `make_sample_idd.py`, `explore_coco.py`

**What was done:**
- Created synthetic IDD sample: 4 images, 5 categories, 13 annotations in `data/idd/`
- Explored COCO JSON structure: `images`, `categories`, `annotations` lists
- Drew bounding boxes on annotated images → `docs/coco_preview_*.jpg`
- Ran 4 verification checks (all PASS)

### COCO bounding box formats

| Format | Written as | Units |
|--------|-----------|-------|
| COCO bbox | `[x, y, w, h]` (top-left) | Pixels |
| xyxy | `[x1, y1, x2, y2]` | Pixels |
| YOLO label | `class cx cy w h` (centre) | Fractions 0–1 |

```
python make_sample_idd.py   # create synthetic images + instances.json
python explore_coco.py      # print summary, draw boxes, verify
```

---

## Session 6 — Dataset Audit & Visualisation

**Files:** `make_audit_dataset.py`, `audit_dataset.py`

**What was done:**
- Created 100-image synthetic audit dataset with **deliberate defects** in `data/audit/`
- Ran full dataset audit → `docs/audit_report.md` + `docs/audit_charts.png`
- Also audited Session 5 data → `docs/s5_audit/`

### Audit areas

| Area | Question | Finding (audit dataset) |
|------|----------|------------------------|
| Class distribution | Are all classes fairly represented? | autorickshaw rare (1.2%, 40:1 ratio) |
| Annotation validity | Are boxes and links correct? | 12 of 408 annotations have problems |
| Image quality | Do files exist, open, match JSON? | 12 of 100 images have problems |
| Object sizes | Small / medium / large? | 2 small, 306 medium, 98 large |

```
python make_audit_dataset.py                              # create 100-image audit dataset
python audit_dataset.py                                   # audit data/audit/
python audit_dataset.py --ann data/idd/annotations/instances.json \
                        --images data/idd/images \
                        --out docs/s5_audit              # audit Session 5 data
```

### Thresholds (tune by looking at flagged images)

| Constant | Default | Meaning |
|----------|---------|---------|
| `MIN_BOX_SIDE` | 10 px | Box side below this = tiny |
| `DARK_MEAN` | 50 | Mean brightness below this = too dark |
| `BLUR_VAR` | 100 | Sharpness score below this = blurry |
| `RARE_SHARE` | 5% | Class below this share = rare |
| `AREA_TOLERANCE` | 5% | Area vs w×h mismatch allowed |

---

## Versions

| Tag | Description |
|-----|-------------|
| v0.1 | Sessions 4–6: repo structure, environment check, COCO exploration, dataset audit |

---
*Department: DLAC — VisionPort Project*
