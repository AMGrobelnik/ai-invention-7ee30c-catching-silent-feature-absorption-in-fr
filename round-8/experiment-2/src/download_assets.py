import os, time
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER","0")
from huggingface_hub import hf_hub_download, snapshot_download
tok=os.environ.get("HF_TOKEN")
t0=time.time()
p=hf_hub_download('google/gemma-scope-2b-pt-res','layer_12/width_16k/average_l0_82/params.npz',token=tok)
print(f"[{time.time()-t0:.0f}s] SAE -> {p}", flush=True)
try:
    d=snapshot_download('google/gemma-2-2b', token=tok,
        allow_patterns=["*.json","*.model","*.safetensors","tokenizer*","*.txt"])
    print(f"[{time.time()-t0:.0f}s] MODEL(gated) -> {d}", flush=True)
except Exception as e:
    print(f"gated failed: {repr(e)[:200]}; trying mirror", flush=True)
    d=snapshot_download('unsloth/gemma-2-2b', token=tok,
        allow_patterns=["*.json","*.model","*.safetensors","tokenizer*","*.txt"])
    print(f"[{time.time()-t0:.0f}s] MODEL(mirror) -> {d}", flush=True)
print("DONE", flush=True)
