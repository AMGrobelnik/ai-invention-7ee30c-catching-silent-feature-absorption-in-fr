#!/usr/bin/env python
"""Pre-fetch all heavy assets so the main run can go offline:
  - Gemma-Scope L12/16k SAE params.npz (google/gemma-scope-2b-pt-res)
  - unsloth/gemma-2-2b model weights + tokenizer (mirror of gated google/gemma-2-2b)
  - google/civil_comments train split (CC0; gazetteer-scanned for safety identity slices)
Idempotent: re-running uses the HF cache. Prints a one-line READY/FAIL per asset."""
import os, sys, time
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

t0 = time.time()
def el():
    return f"{time.time()-t0:6.1f}s"


def fetch_sae():
    from huggingface_hub import hf_hub_download
    p = hf_hub_download("google/gemma-scope-2b-pt-res",
                        "layer_12/width_16k/average_l0_82/params.npz",
                        token=os.environ.get("HF_TOKEN"))
    print(f"{el()} SAE READY {p}", flush=True)


def fetch_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    for mid in ("unsloth/gemma-2-2b", "google/gemma-2-2b"):
        try:
            AutoTokenizer.from_pretrained(mid, token=os.environ.get("HF_TOKEN"))
            AutoModelForCausalLM.from_pretrained(
                mid, torch_dtype=torch.bfloat16, token=os.environ.get("HF_TOKEN"))
            print(f"{el()} MODEL READY {mid}", flush=True)
            return
        except Exception as e:  # noqa: BLE001
            print(f"{el()} MODEL {mid} failed: {repr(e)[:160]}", flush=True)
    print(f"{el()} MODEL FAIL", flush=True)


def fetch_civil():
    try:
        from datasets import load_dataset
        ds = load_dataset("google/civil_comments", split="train")
        print(f"{el()} CIVIL READY n={len(ds)} cols={ds.column_names}", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"{el()} CIVIL FAIL {repr(e)[:200]}", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "sae"):
        fetch_sae()
    if which in ("all", "model"):
        fetch_model()
    if which in ("all", "civil"):
        fetch_civil()
    print(f"{el()} PREFETCH DONE", flush=True)
