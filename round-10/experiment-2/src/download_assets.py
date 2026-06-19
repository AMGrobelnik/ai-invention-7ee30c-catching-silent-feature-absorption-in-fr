import os, time
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
from huggingface_hub import hf_hub_download, snapshot_download, HfApi
import re

REPO = "google/gemma-scope-2b-pt-res"
tok = os.environ.get("HF_TOKEN")
t0 = time.time()


def _l0_of(p):
    m = re.search(r"average_l0_(\d+)", str(p)); return int(m.group(1)) if m else 99999


# ---- model ----
try:
    d = snapshot_download("google/gemma-2-2b", token=tok,
                          allow_patterns=["*.json", "*.model", "*.safetensors", "tokenizer*", "*.txt"])
    print(f"[{time.time()-t0:.0f}s] MODEL(gated) -> {d}", flush=True)
except Exception as e:
    print(f"gated failed: {repr(e)[:200]}; trying mirror", flush=True)
    d = snapshot_download("unsloth/gemma-2-2b", token=tok,
                          allow_patterns=["*.json", "*.model", "*.safetensors", "tokenizer*", "*.txt"])
    print(f"[{time.time()-t0:.0f}s] MODEL(mirror) -> {d}", flush=True)

# ---- the 4 SAE configs (pick avg_l0 closest to target) ----
api = HfApi()
files = api.list_repo_files(REPO, token=tok)
targets = [(12, "16k", 82), (12, "65k", 72), (9, "16k", 100), (9, "65k", 100)]
for layer, width, l0t in targets:
    cands = [f for f in files if re.match(rf"layer_{layer}/width_{width}/average_l0_\d+/params\.npz$", f)]
    if not cands:
        print(f"NO params for layer_{layer}/width_{width}", flush=True); continue
    l0s = sorted({_l0_of(f) for f in cands})
    best = min(l0s, key=lambda v: abs(v - l0t))
    sid = f"layer_{layer}/width_{width}/average_l0_{best}/params.npz"
    p = hf_hub_download(REPO, sid, token=tok)
    print(f"[{time.time()-t0:.0f}s] SAE layer{layer}/{width} avail={l0s} -> picked {best} -> {p}", flush=True)
print("DONE", flush=True)
