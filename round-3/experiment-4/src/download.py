import os, time
from huggingface_hub import hf_hub_download, snapshot_download
t0=time.time()
print("Downloading SAE npz...", flush=True)
p = hf_hub_download(repo_id="google/gemma-scope-2b-pt-res",
                    filename="layer_12/width_16k/average_l0_82/params.npz")
print(f"SAE npz at {p} ({time.time()-t0:.0f}s)", flush=True)
print("Downloading unsloth/gemma-2-2b model...", flush=True)
d = snapshot_download(repo_id="unsloth/gemma-2-2b",
                      allow_patterns=["*.json","*.model","*.safetensors","tokenizer*","*.txt"])
print(f"model at {d} ({time.time()-t0:.0f}s)", flush=True)
print("DOWNLOAD_COMPLETE", flush=True)
