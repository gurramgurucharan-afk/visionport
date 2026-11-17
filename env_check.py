# env_check.py  –  VisionPort Session 4
# Gathers machine / environment facts and saves them to env_report.md
# Run:  python env_check.py

import sys
import platform
import shutil
import subprocess
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. Imports – optional packages handled gracefully
# ---------------------------------------------------------------------------
try:
    import torch
    TORCH_OK = True
except ImportError:
    TORCH_OK = False

# ---------------------------------------------------------------------------
# 2. Helper functions
# ---------------------------------------------------------------------------
def pkg_version(name: str) -> str:
    """Return installed version of a package, or 'NOT INSTALLED'."""
    try:
        import importlib.metadata as meta
        return meta.version(name)
    except Exception:
        return "NOT INSTALLED"

def run_cmd(cmd: list[str]) -> str:
    """Run a shell command and return stdout, or an error message."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() or result.stderr.strip()
    except FileNotFoundError:
        return "command not found"
    except Exception as e:
        return str(e)

# ---------------------------------------------------------------------------
# 3. Collect facts
# ---------------------------------------------------------------------------
rows: list[tuple[str, str]] = []

# System and Python
rows.append(("Date",            datetime.now().strftime("%Y-%m-%d %H:%M")))
rows.append(("OS",              platform.platform()))
rows.append(("Python version",  sys.version.split()[0]))
rows.append(("Python path",     sys.executable))

# Key packages
for pkg in ["streamlit", "fastapi", "uvicorn", "ultralytics",
            "torch", "torchvision", "numpy", "pillow", "opencv-python"]:
    rows.append((pkg, pkg_version(pkg)))

# NVIDIA driver (outside PyTorch)
if shutil.which("nvidia-smi"):
    driver_line = run_cmd(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"])
    rows.append(("NVIDIA driver", driver_line or "found (no version parsed)"))
else:
    rows.append(("NVIDIA driver", "No NVIDIA GPU / driver detected"))

# PyTorch GPU info
if TORCH_OK:
    rows.append(("torch.cuda.is_available", str(torch.cuda.is_available())))
    if torch.cuda.is_available():
        rows.append(("CUDA version (torch)",  torch.version.cuda or "unknown"))
        rows.append(("cuDNN version",         str(torch.backends.cudnn.version())))
        rows.append(("GPU name",              torch.cuda.get_device_name(0)))
        rows.append(("GPU memory (GB)",       f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}"))
        # Smoke-test: a real computation on the GPU
        try:
            a = torch.randn(1000, 1000, device="cuda")
            b = torch.randn(1000, 1000, device="cuda")
            _ = a @ b
            rows.append(("GPU compute test", "PASS (1000×1000 matmul on CUDA)"))
        except Exception as e:
            rows.append(("GPU compute test", f"FAIL – {e}"))
    else:
        rows.append(("CUDA version (torch)", "N/A – CPU build or no GPU"))
else:
    rows.append(("torch.cuda.is_available", "torch NOT INSTALLED"))

# ---------------------------------------------------------------------------
# 4. Print to console
# ---------------------------------------------------------------------------
width = max(len(k) for k, _ in rows) + 2
print("\n=== VisionPort Environment Report ===")
for k, v in rows:
    print(f"  {k:<{width}}: {v}")

# ---------------------------------------------------------------------------
# 5. Save as Markdown table  →  env_report.md
# ---------------------------------------------------------------------------
header  = "| Item | Value |\n|------|-------|\n"
table   = header + "".join(f"| {k} | {v} |\n" for k, v in rows)

report  = f"# VisionPort Environment Report\n\nGenerated: {datetime.now()}\n\n{table}\n"

with open("env_report.md", "w", encoding="utf-8") as fh:
    fh.write(report)

print("\nReport saved to env_report.md")
