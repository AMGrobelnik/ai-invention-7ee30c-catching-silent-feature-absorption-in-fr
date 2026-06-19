import os, sys, time
from huggingface_hub import hf_hub_download, snapshot_download
t0=time.time()
tok=os.environ.get("HF_TOKEN")
# 1) gemma-scope SAE params (only the L12/16k/l0_82 file)
try:
    p=hf_hub_download("google/gemma-scope-2b-pt-res","layer_12/width_16k/average_l0_82/params.npz",token=tok)
    print(f"[{time.time()-t0:.0f}s] SAE params:", p, flush=True)
except Exception as e:
    print("SAE download FAILED:", repr(e)[:200], flush=True); sys.exit(1)
# 2) gemma-2-2b model (gated; HF_TOKEN). Fall back to unsloth mirror if gated fails.
for mid in ("google/gemma-2-2b","unsloth/gemma-2-2b"):
    try:
        d=snapshot_download(mid, token=tok, ignore_patterns=["*.gguf","*.bin","*.pth","*.onnx","onnx/*"])
        print(f"[{time.time()-t0:.0f}s] MODEL {mid}:", d, flush=True)
        break
    except Exception as e:
        print(f"MODEL {mid} FAILED:", repr(e)[:200], flush=True)
print(f"[{time.time()-t0:.0f}s] DONE", flush=True)
