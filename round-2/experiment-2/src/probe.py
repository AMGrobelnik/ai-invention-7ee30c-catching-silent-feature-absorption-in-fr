#!/usr/bin/env python3
"""De-risk probe: load Gemma-Scope SAE + gemma-2-2b (unsloth mirror), validate the
manual forward-hook residual extraction against SAE reconstruction cosine and L0 sparsity."""
import os, sys
os.environ.setdefault("HF_HOME", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_cache"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import torch
import numpy as np
from loguru import logger

logger.remove(); logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

RELEASE = "gemma-scope-2b-pt-res-canonical"
SAE_ID = "layer_12/width_16k/canonical"
HOOK = "blocks.12.hook_resid_post"
MODEL_ID = "unsloth/gemma-2-2b"
LAYER = 12
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

TEXTS = [
    "haha you guys are a bunch of losers.",
    "This is so cool, really great idea, well done!",
    "he had steel balls too !",
    "I appreciate your thoughtful and kind response.",
    "you are an idiot and everyone hates you",
    "The weather today is mild with a gentle breeze.",
    "shut up you worthless piece of garbage",
    "Thank you for sharing this informative article.",
]


def main():
    from sae_lens import SAE
    logger.info("Loading SAE %s / %s" % (RELEASE, SAE_ID))
    ret = SAE.from_pretrained(RELEASE, SAE_ID, device=DEVICE)
    sae = ret[0] if isinstance(ret, tuple) else ret
    sae = sae.to(torch.float32)
    logger.info(f"SAE loaded. cfg.hook_name={getattr(sae.cfg,'hook_name',None)} "
                f"d_in={getattr(sae.cfg,'d_in',None)} d_sae={getattr(sae.cfg,'d_sae',None)} "
                f"normalize={getattr(sae.cfg,'normalize_activations',None)} "
                f"W_dec={tuple(sae.W_dec.shape)} dtype_after_cast={sae.W_dec.dtype}")
    assert tuple(sae.W_dec.shape) == (16384, 2304), f"unexpected W_dec {tuple(sae.W_dec.shape)}"

    from transformers import AutoModelForCausalLM, AutoTokenizer
    logger.info(f"Loading model {MODEL_ID} (eager attn for gemma-2 softcap)")
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation="eager",
    ).to(DEVICE).eval()
    logger.info(f"Model loaded. n_layers={model.config.num_hidden_layers} d_model={model.config.hidden_size}")

    captured = {}
    layer_mod = model.model.layers[LAYER]
    def hook(module, inp, out):
        captured["resid"] = (out[0] if isinstance(out, tuple) else out).detach()
    h = layer_mod.register_forward_hook(hook)

    tok.padding_side = "right"
    enc = tok(TEXTS, return_tensors="pt", padding=True, truncation=True, max_length=128).to(DEVICE)
    with torch.no_grad():
        model(**enc, output_hidden_states=True)
        resid_hook = captured["resid"].float()  # [B,T,2304]
        # cross-check against output_hidden_states[LAYER+1] (output of block LAYER)
        out_hs = model(**enc, output_hidden_states=True).hidden_states
        resid_hs = out_hs[LAYER + 1].float()
    h.remove()
    diff = (resid_hook - resid_hs).abs().max().item()
    logger.info(f"hook vs hidden_states[{LAYER+1}] max abs diff = {diff:.2e} (should be ~0)")

    with torch.no_grad():
        feats = sae.encode(resid_hook)         # [B,T,16384]
        recon = sae.decode(feats)              # [B,T,2304]
    mask = enc["attention_mask"].bool()
    # exclude BOS (first real token) from pooling
    content_mask = mask.clone()
    content_mask[:, 0] = False
    fmask = content_mask.unsqueeze(-1)
    # reconstruction cosine on real tokens
    rh = resid_hook[mask]; rc = recon[mask]
    cos = torch.nn.functional.cosine_similarity(rh, rc, dim=-1)
    logger.info(f"recon cosine (real tokens): mean={cos.mean():.4f} min={cos.min():.4f} p10={cos.quantile(0.1):.4f}")
    fired = (feats > 0)
    l0_tok = fired[mask].float().sum(-1)
    logger.info(f"L0 per token: mean={l0_tok.mean():.1f} median={l0_tok.median():.1f} max={l0_tok.max():.0f}")

    # pooled features
    feats_masked = feats.masked_fill(~fmask, 0.0)
    act_max = feats_masked.max(dim=1).values  # [B,16384]
    cnt = content_mask.sum(1, keepdim=True).clamp(min=1)
    act_mean = feats_masked.sum(dim=1) / cnt
    fires = (act_max > 0)
    logger.info(f"per-example L0 (max-pool firing): {fires.float().sum(-1).tolist()}")
    # toxic vs clean separation on a candidate latent: latent with biggest mean-act gap toxic vs clean
    toxic_idx = torch.tensor([0, 2, 4, 6], device=DEVICE)
    clean_idx = torch.tensor([1, 3, 5, 7], device=DEVICE)
    gap = act_max[toxic_idx].mean(0) - act_max[clean_idx].mean(0)
    top = torch.topk(gap, 5)
    logger.info(f"top toxic-vs-clean latents (max-pool): idx={top.indices.tolist()} gap={[round(x,3) for x in top.values.tolist()]}")
    logger.info("PROBE OK")


if __name__ == "__main__":
    main()
