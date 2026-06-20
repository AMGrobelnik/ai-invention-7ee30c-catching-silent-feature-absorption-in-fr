# gen_art — test_idea

> Phase: `invention_loop` · round 8 · Substep: `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:50:20 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 58360 chars total]
```

### [2] HUMAN-USER prompt · 2026-06-18 10:50:20 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-python · 2026-06-18 10:50:30 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 10:50:30 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-18 10:50:30 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [6] SKILL-INPUT — aii-json · 2026-06-18 11:26:15 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [7] SYSTEM-USER prompt · 2026-06-18 19:46:53 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 58360 chars total]
```

### [8] HUMAN-USER prompt · 2026-06-18 19:46:53 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [9] SYSTEM-USER prompt · 2026-06-18 21:33:14 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_1/`:
... [truncated, 58302 chars total]
```

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:12 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<context>
<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3zaa2xXEp8Az
type: research
title: 'CCRG iter-6: Safety-Identity Absorption & u_sub Label-Efficiency Positioning'
summary: >-
  Positions the two new load-bearing iter-6 gates of the Counterfactual Co-Response Grouping (CCRG) paper and refreshes the
  venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0 LLM spend, no code; builds on iter-4 (art_QBxBPF-9Ldxe)
  and iter-5 (art_y_5u-bfJOq3V) without re-doing settled entries. THREE deliverables. (A) M2' SAFETY-RELEVANT IDENTITY ABSORPTION:
  a cite-and-distinguish block over FIVE sub-literatures never previously surveyed -- SAE debiasing (debiaSAE 2410.13146 VLM/COLM-under-review;
  Ahsan&Wallace 2511.00177 ICLR2026 healthcare; SteerRM 2603.12795 reward-model; DeBiasLens 2602.24014 VLM/CVPR2026-flag),
  model-editing for stereotype (BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025), fairness/concept-erasure
  editing (Karvonen&Marks 2506.10922 NeurIPS2025 Mech-Interp-WS affine edit; SPLINCE 2506.10703 NeurIPS2025; H-SAL 2606.12088),
  identity/entity/PII unlearning (Entity-Level-Unlearning COLING2025; Not-Every-Token 2506.00876; DFSU 2601.15595), and example-reweighting
  debiasing (JTT/GEORGE/EIIL/LfF, carried). VERDICT: CCRG's three-part conjunction -- a DISCOVERED single absorber latent
  for ONE identity sub-context + a PARENT-preserving sub-context edit + scoring vs a SUB-CONTEXT-targeted dense direction
  u_sub -- is distinct from all five (each edits a WHOLE attribute/entity/example-set and preserves UNRELATED material; closest
  near-miss Ahsan&Wallace steers a single race-latent that CO-FIRES with 'incarceration' = entanglement not absorption, and
  concedes SAE steering is 'of marginal utility for realistic tasks'). Both-branches honest-null framing supplied (safety-WIN
  vs absorption-not-exhibited NULL bounded to the auditable edit primitive, connected to the existing 0/28-professions + toxicity-co-firing
  negatives). (B) M1' u_sub LABEL-EFFICIENCY: RETIRES the now-FALSE 'a single dense hyperplane structurally cannot localize
  to a sub-context / erasing the is-a-country direction removes all countries' argument -- u_sub IS a dense hyperplane and
  DOES localize, the testbed already carries its labels, and SPLINCE (preserves covariance with target label), Karvonen&Marks
  (affine edit, bias <2.5%, perf maintained) and H-SAL (label-free matches label-based) externally prove a labeled dense direction
  localizes/preserves utility. Supplies an exact DELETE/REPLACE list + BOTH M1' fork paragraphs (FORK-WIN: discovered single
  feature beats sub-context-labeled dense; FORK-MATCH: matches u_sub WITHOUT sub-context labels = label-efficiency/discovery,
  grounded in Peng 'Discover-not-Act' 2506.23845 verbatim thesis + label-free SAE 2506.01247) + an honest cost note (counterfactual-pair
  cost of grouping vs sub-context-label cost of u_sub). (C) CITATION REFRESH: 14 new grep-verified entries + carry-forward
  flags RESOLVED (Deng 2506.18141 UPGRADE->ACL2026; SAEmnesia 2509.21379 UPGRADE->ICML2026; SNCE 2509.21008 authors confirmed;
  Muchane 2506.01197 keep-preprint), BibTeX, corrections diff, unresolved-flags list, and an updated presentation-strip checklist.
  Outputs research_out.json + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_IlzAiXYWeUYH
type: research
title: 'CCRG iter-7 Positioning: Gated-Dense Prior Art, Localization-First Reposition'
summary: >-
  Positions the iteration-7 CCRG paper and refreshes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research,
  $0, no code; builds on iter-5 (art_y_5u-bfJOq3V) and iter-6 (art_3zaa2xXEp8Az) without re-doing settled entries. FIVE deliverables.
  (A) GATED/CONDITIONAL ACTIVATION-EDITING SURVEY (the new load-bearing piece): VERDICT = gating a dense edit by a sparse/threshold
  detector is ESTABLISHED PRIOR ART, and the exact gated-dense operator the paper uses as a control is already published,
  so DENSE-SUB-ABL-GATED is a CONTROL, not a contribution. Four verified cites: CAST (2409.05907, ICLR 2025 Spotlight; condition-vector
  switch over the prompt's hidden state, gate fit on LABELED example sets), GUARD-IT (2605.12765, preprint; Sentence-Transformer
  Similarity Gate K(x)={j:sim(c_j,phi(x))>=T} over LABELED-forget clusters + norm-preserving rotation h'=(h-a*vhat)*||h||/||h-a*vhat||),
  GSS (2602.08901, preprint; the EXACT operator h'=h-G(|u^T h|>eps)*v Eq.3 / multi-component Eq.14, probe u + steer v OPTIMIZED
  on 1,000 memorization-labeled sequences with eps tuned to the 95th percentile), SADI (2410.12299, ICLR 2025 Poster; dynamic
  per-input steering via a contrastive-pair binary mask). The PLAN MIS-ATTRIBUTED the |u^T h|>eps formula to GUARD-IT; it
  is actually GSS (corrected). In ALL prior methods the gate is SUPERVISED; the SAE-specific contribution is therefore the
  TRAINING-FREE, LABEL-FREE DISCOVERY of WHERE to gate (the precise sub-context absorber marginal-attribution drops) plus
  the absorber's calibrated JumpReLU firing as a built-in calibration-free gate, grounded in Peng 'Discover-not-Act' (2506.23845).
  BOTH M1'' fork paragraphs supplied (WIN: discovered sparse handle beats even gated dense, advantage larger on absorption
  than co-firing cases => traces to structure not footprint; MATCH: gating not SAE-specific => value=label-free discovery;
  plus fallback FORK-c near-NOOP => scope to selective partial suppression). (B) LOCALIZATION-FIRST REPOSITION: drop-in abstract
  spine + intro opener leading with training-free auditable LOCALIZATION of homograph-polysemy absorption, stating localization-NOT-classification
  up front (toxicity unit AUC 0.762 ties/loses raw latents, trails dense 0.84-0.89; sub-attrs 0.63 vs 0.93), presenting the
  44-group safety screen (2/44 = white/straight, both homographs) as the HEADLINE LIMITATION-and-finding (absorption=lexical
  polysemy not demographic semantics; Ahsan-Wallace co-firing corroborates), naming the durable contribution triad (label-free
  discovery+editable feature-KG; a-priori recall-hole diagnostic=exploratory; absorption-regime selection wins). (C) METHOD-IDENTITY
  REFRAME: foreground single-absorber discovery (anchored set-cover effectively k=1; unit-vs-single-best-absorber ablation
  art_3WXWsaSoGMnK shows single absorber WINS; M7 multi-member adds collateral), demote multi-member grouping + C-track to
  secondary, 5 retitle options. (D) CLARITY FIXES: ONE canonical Georgia number (+0.561 CI[0.318,0.811], 2nd judge +0.465
  CI[0.289,0.658]) + exact footnote for the +0.743 safety-section re-run; concept-space-KL (u_sub 0.078 < whole-parent 0.102)
  vs judged-collateral (util_SUB 1.17 < util_whole 1.33, inverts) drop-in. (E) CITATIONS: inherited locked table carried forward
  verbatim + 6 new gated-steering cites with verified IDs/venues/full author lists + new-cite BibTeX + unresolved-flags list
  + 10-item presentation-strip checklist. Outputs research_out.json + research_report.md (sections A-E).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx4
type: research
title: >-
  CCRG iter-8 Positioning: Chanin/Max-Precision Delta, Concentration-as-Sharp-Gate, Localization+Editing Retarget, Locked
  Cites
summary: >-
  Pure web-research positioning pass (no code, $0 LLM spend, cpu_light) that finalizes the iteration-8 CCRG paper framing
  for GEN_PAPER_TEXT. Four deliverables: (D1) the precise LABEL-FREE delta of CCRG's anchored recall-hole-guided precision
  selection vs (i) Chanin's SUPERVISED absorption diagnostic and (ii) a simple max-precision selector, with the M5''' novelty-trim
  wording (set-cover/(1-1/e) demoted to MOTIVATION); (D2) a survey grounding the M3''' mechanism reframe -- the edit win is
  driven by latent CONCENTRATION/PRECISION acting as a sharper conditional gate than a footprint-matched dense projection,
  absorption being only ONE label-free source of concentration -- positioned against the feature-selection-for-steering literature
  so 'concentration not absorption' is grounded, not asserted; (D3) the M2''' retarget decision + BOTH retargeted abstract/intro
  spines (>=4 concentrated wins landed vs base-stays-thin), leading with 'training-free auditable LOCALIZATION + EDITING of
  homograph-polysemy absorption', safety-homograph null as headline limitation, with verified venue-area fit (ICLR primary
  per goal, ICML acceptable); (D4) the locked citation table carried verbatim from iter-6/iter-7 + new concentration/precision-steering
  cites with verified IDs/venues/authors + BibTeX + unresolved flags + a presentation-strip checklist. Builds on iter-7 art_IlzAiXYWeUYH
  (gated-steering prior art + localization-first reposition) and iter-6 art_3zaa2xXEp8Az (safety/u_sub positioning); does
  NOT redo those settled surveys.
runpod_compute_profile: cpu_light
question: >-
  For the iteration-8 CCRG paper (GEN_PAPER_TEXT), how should the positioning be finalized so that (1) the method's novelty
  is honestly trimmed to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' with a precise stated delta
  vs Chanin's supervised absorption diagnostic AND vs a simple max-precision selector (set-cover/(1-1/e) demoted to motivation
  only); (2) the mechanism reframe 'the edit win tracks latent CONCENTRATION/PRECISION, not absorption structure' is POSITIONED
  against prior work relating per-feature precision/sparsity/selectivity to steering surgicality/conditional-gate sharpness;
  (3) the paper is retargeted to lead with training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption
  (ICLR primary, ICML acceptable), with both a wins-landed and a base-thin abstract/intro spine and the safety-homograph-confinement
  null as the headline limitation; and (4) the full citation set is locked (carry iter-6/iter-7 verbatim, add verified concentration/precision-steering
  cites, flag unresolved, invent nothing)?
research_plan: |-
  PURE WEB RESEARCH via the aii-web-tools skill (search -> fetch -> fetch_grep). NO code, NO datasets, NO experiments. $0 LLM/OpenRouter spend. Compute: cpu_light. Wall-clock budget ~3h. Output TWO files in the artifact workspace: research_out.json {title, summary, answer, sources[], follow_up_questions[]} and research_report.md (sections D1-D5). This pass FINALIZES positioning for GEN_PAPER_TEXT; it is a sibling/successor of iter-7 art_IlzAiXYWeUYH and iter-6 art_3zaa2xXEp8Az -- READ THOSE FIRST and CARRY THEIR SETTLED ENTRIES VERBATIM (do NOT re-survey gated-steering prior art or safety/u_sub positioning, which are settled). Both dependency research_out.json files are available; their locked-cite tables and abstract spines are the starting point.

  ========== STEP 0 -- GROUND IN THE DEPENDENCIES (no new searches; ~15 min) ==========
  Read the two dependency outputs already in this run:
    - iter-7 art_IlzAiXYWeUYH: /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_research_1/research_out.json (+ research_report.md). Extract: (a) the LOCKED gated-steering cites (CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint = exact h'=h-G(|u^T h|>eps)v operator; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint), all SUPERVISED-gate => gating is PRIOR ART, SAE value = label-free DISCOVERY of WHERE to gate; (b) the localization-first abstract spine + intro opener; (c) the full carried-forward locked-cite table listed in section (E); (d) Peng 'Discover-not-Act' 2506.23845 framing.
    - iter-6 art_3zaa2xXEp8Az: same dir under iter_6. Extract the safety-absorption cite-and-distinguish block + the u_sub label-efficiency positioning + the locked-cite refresh (14 entries). These are SETTLED -- carry, do not redo.
  Also anchor the load-bearing NUMBERS from the hypothesis (do NOT invent or alter; keep consistent across the report): large KG-vs-STRONGEST-ungated-dense (DENSE-SUB-ABL) = +1.00 CI[0.79,1.21] (the LEAD edit number); large KG-vs-footprint-GATED-dense = +1.58 CI[1.36,1.79] (the INFLATED/caveated robustness number -- gate driven to beta~2.97 over-erasure, gated collateral 0.290 vs its own ungated 0.021, ~14x more); Amazon = +0.75 CI[0.41,1.08] (named-entity homograph win, absorber 6846 max_kg 1.14); Bush = KG_MATCHES_GATED (parity), Cook structured; insult 13367 = +0.47 CO-FIRING win found by max-AUC NOT set-cover (the concentration-not-absorption evidence); Georgia 16009 / Jordan 540 = NO_MEANINGFUL_FORGET (distributed sense, max_kg 0.064/0.114, NOOP-identical 89%); safety 2/44 (white, straight; both homographs); named-entity 3/5 (Amazon/Bush/Cook); professions 0/28; homograph entities 3/64 (months only); selectivity corrected 722x/676x (16k/65k comparably surgical); cross-dictionary 65k full / layer-9 partial; the NEW fair control = DENSE-SUB-ABL-GATED-FAIR (u_sub gated by the precise d_sub detector AUC~1.0, bounded beta<=1).

  ========== STEP 1 -- DELIVERABLE D1: CHANIN-DELTA + MAX-PRECISION DELTA (M5''' novelty trim) ==========
  GOAL: write the precise paragraph stating what the LABEL-FREE anchor + recall-hole + precision-gate buys over (i) running Chanin's diagnostic directly and (ii) a simple max-precision selector; and supply the trim wording (set-cover/(1-1/e) = MOTIVATION only; method identity = 'anchored recall-hole-guided PRECISION SELECTION of a single absorber').
  SEARCH/FETCH:
    1a. fetch_grep the Chanin 2409.14507 FULL TEXT (try https://arxiv.org/html/2409.14507v3 first; fallback OpenReview PDF https://openreview.net/pdf/5fa0d903675ab0ae5df67d598ecfe21ce2dff8f7.pdf). Grep for: 'absorption fraction', 'absorption_fraction', 'probe', 'logistic regression', 'projection', 'ablation', 'first letter', 'main latent', 'encoder cosine', 'mean absorption'. EXTRACT precisely: (a) HOW the parent/main latent is identified -- confirm it uses a SUPERVISED logistic-regression probe (max encoder-cosine with the LR probe direction); (b) HOW the absorbing latent is identified -- ablation effect on a TASK-SPECIFIC logit (the first-letter logit) after projecting out the probe direction; (c) the absorption-fraction metric definition. CONFIRM the diagnostic REQUIRES (i) a supervised probe and (ii) a task label/logit, and that the empirical demonstration is almost entirely first-letter spelling (running example 'short'/'starts-with-S').
    1b. State the DELTA vs Chanin (label-free): CCRG's anchor is chosen by content-response RECALL on counterfactual pairs (available to every baseline, NO probe); the recall-hole is the parent's uncovered counterfactual pairs (NO logit); the precision-gate is firing-precision on the target sub-context (NO label beyond the counterfactual partition). Chanin DETECTS absorption on an individually-named latent GIVEN a supervised probe+logit; it does NOT propose parent+absorber as a usable, editable handle WITHOUT supervision, and is form-bound to spelling in its demonstrations. CCRG uses the FORM-FREE probe+ablation diagnostic ONLY to SCORE already-formed KG edges (non-circular), never to FORM units. So the buy is: training-free, label-free, form-free SURFACING of the precise sub-context latent that marginal-attribution selection silently drops.
    1c. MAX-PRECISION delta: the open question the iter-8 EXPERIMENT answers is whether the anchored recall-hole-guided set-cover beats a simple 'pick the single most precise latent firing on the target sub-context' (max-precision / S-prec) selector. Because every reported edit win is effectively k=1, the LIKELY answer is a TIE. Supply TWO conditional wordings: (TIE) trim to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber'; present set-cover/(1-1/e) as MOTIVATION for the disjoint-support coverage view only, NOT a load-bearing guarantee; the discovery step's value over max-precision is the RECALL-HOLE ANCHORING that tells you WHICH sub-context to select a precise latent FOR (max-precision alone needs the sub-context handed to it). (SET-COVER ADDS SOMETHING) if any case shows k>1 or the recall-hole objective measurably helps, keep the set-cover framing but still demote (1-1/e) to motivation. Make clear GEN_PAPER_TEXT picks the wording matching the experiment's M3''' result.
    1d. Briefly search 'precision-weighted SAE latent selection' / 'recall-based vs precision-based SAE feature selection' / 'max-precision latent baseline steering' to confirm no existing named method already IS 'anchored recall-hole precision selection' (defensive novelty check); record near-misses (FGAA relevance/density filtering; CorrSteer correlation selection; Arad output-score filtering -- see D2) and state the delta (those select for steering EFFECT or correlation, not for the recall-hole an absorbed parent leaves).
  WRITE: research_report.md section D1 = the Chanin-and-max-precision delta paragraph (drop-in for the Related Work / Method-identity subsection), plus the two conditional trim sentences.

  ========== STEP 2 -- DELIVERABLE D2: CONCENTRATION-AS-SHARP-GATE (M3''' mechanism reframe grounding) ==========
  GOAL: ground the claim 'the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a SHARPER conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable source of concentration, not the cause of the win' against prior work relating per-feature precision/sparsity/selectivity to steering surgicality. This makes 'concentration not absorption' POSITIONED, not merely asserted.
  VERIFIED ANCHOR CITES (confirm IDs/venues/authors via fetch_grep of arXiv Comments; flag if unresolved):
    2a. Arad, Mueller, Belinkov -- 'SAEs Are Good for Steering -- If You Select the Right Features' (arXiv 2505.20063; verify EMNLP 2025). KEY: introduces input vs OUTPUT scores; filtering OUT low-output-score features gives 2-3x steering improvement => the right FEATURE SELECTION (a precise, output-effective feature), not the steering mechanism, drives steering quality. This is the HEADLINE cite for 'which precise latent you pick is what matters' -- directly supports CCRG's 'label-free discovery of WHERE to gate' and the concentration reframe.
    2b. CorrSteer -- 'Generation-Time LLM Steering via Correlated Sparse Autoencoder Features' (arXiv 2508.12535; Cho, Wu, Koshiyama; Comments say ICML 2026 -- FLAG/verify, cite preprint if unresolved). Correlation-based selection extracts 'more relevant features, thereby reducing spurious correlations' => precise/specific selection reduces collateral.
    2c. FGAA -- 'Steering LLMs with Feature Guided Activation Additions' (arXiv 2501.09929; verify authors/venue). Relevance + density/'concreteness' filtering: high-DENSITY (frequently-firing) features dominate despite limited task specificity and must be filtered out => low-density + high-precision = concentration = a clean handle. Directly supports the concentration axis (sparse firing + high per-sub-context precision).
    2d. Sparse Activation Steering -- 'Steering Large Language Model Activations in Sparse Spaces' (arXiv 2503.00177; verify). Scaling SAE width increases steering-vector sparsity/monosemanticity => 'better disentangle features by reducing overlap', improving intervention precision => sparser/more-concentrated => sharper gate.
    2e. Anthropic 'Scaling Monosemanticity' (Templeton et al. 2024, transformer-circuits.pub; cite as the canonical monosemanticity source). The precise-boundary claim: monosemantic features 'stop responding the moment text diverges from the target concept' -> a precise feature's firing IS a sharp conditional gate. Use to ground the conditional-gate-sharpness intuition.
    2f. Tie to the LOCKED iter-7 gating cites (CAST/GSS/GUARD-IT/SADI): the gating MECHANISM is prior art and supervised; a concentrated latent's calibrated JumpReLU firing is itself a sharp, threshold-free conditional gate, whereas a footprint-matched DENSE projection must be driven to beta~3 over-erasure to match the same forget (=> ~14x more collateral on 'large'). So the edit advantage = sharper conditioning from a concentrated detector, NOT absorption per se.
  SEARCH (to find any stronger/more-direct cite and avoid missing an obvious one): 'feature selectivity predicts steering side effects', 'sparse precise feature cleaner edit handle lower collateral', 'per-feature specificity steering fluency tradeoff', 'conditional steering reduces collateral selective feature'. Record 1-2 best additional hits with verified IDs.
  WRITE: research_report.md section D2 = the concentration-as-sharp-gate positioning paragraph(s): (i) state the property the method should select for = per-sub-context PRECISION x sparse firing = CONCENTRATION; (ii) cite 2a-2e that selection of a precise/specific/low-density feature is the established driver of clean steering; (iii) state that absorption is one label-free-discoverable source of concentration (absorber marginal-attribution drops) but a concentrated CO-FIRING latent (insult, found by max-AUC not set-cover) also wins, so the win predictor is concentration; (iv) explicitly DROP/heavily-qualify 'the win traces to the absorption structure the method discovers'.

  ========== STEP 3 -- DELIVERABLE D3: RETARGET/VENUE + BOTH ABSTRACT/INTRO SPINES (M2''' retarget) ==========
  GOAL: decide and justify leading the paper with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption', confirm venue-area fit, and supply BOTH spines.
    3a. VENUE FIT: confirm via iclr.cc/Conferences/2026/CallForPapers and icml.cc/Conferences/2026/CallForPapers that the framing fits. NOTE the GOAL says 'Target ICLR primary, ICML fallback' while THIS artifact-direction says 'ICML primary acceptable, ICLR fallback' -- TREAT THE GOAL AS AUTHORITATIVE (ICLR primary) but explicitly state fit for BOTH and resolve the tension in-report. ICLR 2026 lists 'Interpretability, fairness, privacy, and ethical AI' as an area (fits). NOTE ICML 2026 main-track submission closed ~Jan 28 2026 (so the live cycle for a mid-2026 paper is ICLR 2026 / the next ICML); the deliverable is AREA fit, not a deadline. Map the contribution to the reviewer-evaluable areas named in the goal (clustering methods, feature selection, classification, knowledge graphs, knowledge extraction, applied knowledge discovery, text data analytics, LLMs/deep learning) -- the localization + editable feature-KG + label-free discovery framing fits these far better than a classification-win framing (the paper makes NO out-classifies-dense claim). State this mapping explicitly so the title/abstract commit to localization+editing, not classification/steering wins.
    3b. RETARGET DECISION: lead with auditable LOCALIZATION (+ EDITING on concentrated features) of homograph-polysemy absorption; safety-homograph-confinement null (2/44, both homographs) as the HEADLINE LIMITATION-and-finding; the concentrated-feature edit (large +1.00, Amazon +0.75) as a SCOPED capability bounded by the fair gated control; classification SUPPORTING/within-SAE; router DEMOTED to exploratory. Build directly on the iter-7 localization-first spine (carry it, then update for: de-inflation to +1.00-lead; the new fair bounded-beta d_sub control; concentration-not-absorption mechanism; set-cover-as-motivation; both forget instruments; unified gate operator).
    3c. SUPPLY BOTH SPINES (drop-in abstract ~150-220 words + intro opener ~1 para each):
       - OUTCOME A (>=4 independent concentrated wins LANDED: large, Amazon + Bush/Cook/wider-vocab under the fair bounded-beta d_sub-gated control): the sparse-gated EDIT is a broader load-bearing capability. Abstract foregrounds: training-free label-free localization of homograph-polysemy absorption + an editable feature-KG; the edit win LED by KG-vs-STRONGEST-dense (+1.00 on large; never lead with +1.58) on >=4 concentrated features, shown to track CONCENTRATION (max-precision ablation) and to beat the genuinely-fair bounded-beta d_sub-gated dense control; safety null as capping scope.
       - OUTCOME B (base STAYS THIN, n~=2; or the fair gated control MATCHES KG): lead FULLY with the auditability/localization SPINE + the safety-homograph-confinement NULL as the finding; the edit is a scoped capability on concentrated features; if fair-gated matches => contribution = label-free DISCOVERY of where to gate (gating is prior art); concentration-not-absorption reframe central; set-cover = motivation only.
       Each spine must: state localization-NOT-classification up front; name the durable contribution triad (label-free discovery + editable feature-KG; recall-hole screening diagnostic = exploratory; absorption-regime/concentration selection wins where the signature holds); headline the homograph-confined safety null; and avoid the inflated +1.58-vs-footprint-gated number as the lead.
  WRITE: research_report.md section D3 = venue-fit justification + retarget decision + BOTH abstract+intro spines, clearly labeled OUTCOME-A and OUTCOME-B with a one-line selector telling GEN_PAPER_TEXT which to use based on the M1'''/M2''' experiment results.

  ========== STEP 4 -- DELIVERABLE D4: CITATION FINALIZATION + D5: PRESENTATION-STRIP CHECKLIST ==========
    4a. CARRY FORWARD the FULL locked-cite table from iter-7 section (E) + iter-6, VERBATIM (Chanin 2409.14507 NeurIPS2025; Feature-Hedging 2505.11756; AxBench 2501.17148 ICML2025; SAEBench 2503.09532 ICML2025; CanonicalUnits 2502.04878 ICLR2025; Matryoshka 2503.17547 ICML2025; Farrell 2410.19278 NeurIPS2024-Safe-GenAI-WS; SPLINCE 2506.10703 NeurIPS2025; Karvonen-Marks 2506.10922 NeurIPS2025-MechInterp-WS; Ahsan-Wallace 2511.00177 ICLR2026; BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025; Entity-Level-Unlearning COLING2025; Deng 2506.18141 ACL2026; SAEmnesia 2509.21379 ICML2026; Peng 2506.23845; CRISP 2508.13650 ACL2026; SAUCE 2503.14530 WITHDRAWN/ICCV2025-CVF; SSPU 2505.24428 EMNLP2025; LEACE 2306.03819 NeurIPS2023; CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint; the iter-6 debiasing set; JTT/GEORGE/EIIL/LfF; DiffCoEx/WGCNA; Nemhauser-Wolsey-Fisher/Feige set-cover; CDLC 2505.07073; Veitch 2106.00545; Kaushik CAD ICLR2020; CEBaB 2205.14140; ParaDetox). Do NOT re-verify settled locks; just list them with their locked venues and flag the ones the dependencies already flagged unresolved (GUARD-IT/GSS/DAC venues; DeBiasLens CVPR2026; Deng dual-listing; Karvonen-Marks workshop).
    4b. ADD the NEW concentration/precision-steering cites, each with fetch_grep-VERIFIED arXiv ID + Comments-field venue + FULL author list: Arad-Mueller-Belinkov 2505.20063 (verify EMNLP2025); CorrSteer 2508.12535 Cho-Wu-Koshiyama (Comments=ICML2026, FLAG); FGAA 2501.09929; Sparse-Activation-Steering 2503.00177; Anthropic Scaling-Monosemanticity (Templeton et al. 2024, transformer-circuits.pub -- cite by URL, no arXiv). For any venue not grep-confirmable from the Comments field, cite as PREPRINT and add to the unresolved-flags list. INVENT NOTHING.
    4c. EMIT BibTeX for every NEW cite added this iteration (the concentration set); carry the iter-6/iter-7 BibTeX by reference (note GEN_PAPER_TEXT already has it).
    4d. PRESENTATION-STRIP CHECKLIST (research_report.md section D5), 10-12 items: (1) lead title/abstract with 'training-free auditable LOCALIZATION (+ EDITING) of homograph-polysemy absorption'; (2) lead the edit table with KG-vs-STRONGEST-ungated-dense (+1.00 on large) -- caveat the +1.58-vs-footprint-gated number with the beta~2.97 over-erasure note (gated collateral 0.290 vs its own ungated 0.021); (3) report BOTH forget instruments (completion-drop AND sub-probe-drop) side by side and match operators on a BEHAVIORAL measure, not next-token KL; (4) UNIFY the gate operator into ONE definition across large/Amazon/Bush (or document the per-case clamp in-table: 3%-global-footprint vs 95%-X-rate); (5) present set-cover/(1-1/e) as MOTIVATION only; method identity = 'anchored recall-hole-guided precision selection of a single absorber'; (6) state the mechanism as CONCENTRATION/PRECISION not absorption (insult co-fires yet wins; Georgia/Jordan absorb yet lose); (7) safety-homograph null (2/44) = headline limitation; (8) state localization-NOT-classification (no SAE unit out-classifies a dense probe on any task); (9) router = exploratory (out-of-sample Wilson includes 0.5); (10) corrected selectivity (722x/676x; 16k/65k comparably surgical), cross-dictionary 65k full/layer-9 partial; (11) demote multi-member grouping + C-track to secondary (single absorber wins, multi-member adds collateral); (12) STRIP all iteration/rebuttal/infra scaffolding (M1''/M1'''/art_ tags/'iter-7 reviewer'/GPU-hours).

  ========== STEP 5 -- ASSEMBLE OUTPUTS ==========
  Write research_out.json with: title; summary; answer (a tight synthesis of D1-D5 with the key verdicts: method-identity = anchored recall-hole precision selection / set-cover=motivation; mechanism = concentration not absorption, positioned via 2505.20063/CorrSteer/FGAA/SAS/monosemanticity; retarget = localization+editing lead with both spines; cites locked); sources[] (every fetched URL with a one-line evidence note: Chanin body, the 4-5 concentration cites with verified venue/authors, ICLR/ICML CfP pages, plus the carried iter-6/iter-7 anchors by reference); follow_up_questions[] (e.g.: did M3''' show set-cover beats or ties max-precision? did M2''' land >=4 wins -> use OUTCOME-A or OUTCOME-B spine? did M1''' fair bounded-beta d_sub-gated control get beaten or matched? are the CorrSteer/Arad venues confirmable before camera-ready?). Write research_report.md with sections D1-D5 as specified, including all drop-in paragraphs, both spines, the locked+new cite table, BibTeX for new cites, unresolved-flags list, and the presentation-strip checklist.

  ========== CONTINGENCIES / FAILURE MODES ==========
  - If the Chanin HTML body is inaccessible, use the OpenReview PDF (fetch_grep) or the NeurIPS 2025 poster page; the supervised-probe + first-letter-logit + absorption-fraction facts are already corroborated by search snippets -- confirm and cite, do not block.
  - If a new concentration cite's venue is not grep-confirmable from the Comments field, cite as preprint + add to unresolved flags (NEVER invent a venue). CorrSteer's 'ICML 2026' is from Comments -> keep but flag (large 45-page preprint, may be a workshop/under-review listing).
  - If the concentration-steering literature turns out thinner than expected, fall back to the strongest anchors (Arad 2505.20063 + the locked CAST/GSS + Anthropic monosemanticity precise-boundary claim) -- these alone ground the reframe; do not pad with weak cites.
  - If venue CfP pages are unreachable, rely on the known areas (ICLR 'Interpretability, fairness, privacy, ethical AI'; reviewer-evaluable areas in the goal) and proceed; venue choice is ICLR-primary per the goal regardless.
  - Keep ALL load-bearing numbers consistent with the hypothesis; if a number is needed that is not in the hypothesis, mark it [VERIFY-AT-WRITE] rather than inventing.
  - Strictly $0 LLM spend (web research only); no OpenRouter calls.
explanation: >-
  This research artifact finalizes the iteration-8 CCRG paper positioning so GEN_PAPER_TEXT can write a defensible draft regardless
  of how the parallel iter-8 experiments (M1''' fair gated control, M2''' expanded base, M3''' max-precision ablation) land.
  The iter-7 reviewer raised three publication-gating majors that are framing/positioning problems this artifact must resolve:
  (R6/M5''') the set-cover/(1-1/e) framing oversells a step that is effectively k=1, so the novelty must be trimmed to 'anchored
  recall-hole-guided precision selection' with a precise stated delta vs Chanin's SUPERVISED diagnostic and vs a simple max-precision
  selector; (R3/M3''') the claim 'the win traces to absorption structure' is unsupported because a concentrated CO-FIRING
  latent also wins, so the mechanism must be reframed to latent CONCENTRATION/PRECISION and POSITIONED against the established
  feature-selection-for-steering literature (where selecting a precise/specific/low-density feature is the known driver of
  clean steering); (R2/M2''') the positive edit base is n~=2, so the paper must retarget to lead with auditable localization+editing
  of homograph-polysemy absorption with the safety-homograph null as the headline limitation, and needs both a wins-landed
  and a base-thin abstract/intro spine ready. The artifact also locks the citation set (carrying the iter-6/iter-7 venue-verified
  table verbatim and adding verified concentration/precision-steering cites) and supplies a presentation-strip checklist.
  Without this positioning pass the paper would lead with the inflated +1.58 number, an oversold set-cover guarantee, and
  an unsupported absorption-causation claim -- exactly the three things the reviewer flagged as blocking. Pure web research
  is the right tool: every deliverable is literature synthesis, delta articulation, venue-area mapping, and citation verification
  -- no computation, and it must run in parallel with the experiments so its both-outcome wording is ready for GEN_PAPER_TEXT.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-18 10:51:12 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 10:51:22 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [4] SYSTEM-USER prompt · 2026-06-18 19:51:21 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<context>
<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3zaa2xXEp8Az
type: research
title: 'CCRG iter-6: Safety-Identity Absorption & u_sub Label-Efficiency Positioning'
summary: >-
  Positions the two new load-bearing iter-6 gates of the Counterfactual Co-Response Grouping (CCRG) paper and refreshes the
  venue-locked citation set for GEN_PAPER_TEXT. Pure web research, $0 LLM spend, no code; builds on iter-4 (art_QBxBPF-9Ldxe)
  and iter-5 (art_y_5u-bfJOq3V) without re-doing settled entries. THREE deliverables. (A) M2' SAFETY-RELEVANT IDENTITY ABSORPTION:
  a cite-and-distinguish block over FIVE sub-literatures never previously surveyed -- SAE debiasing (debiaSAE 2410.13146 VLM/COLM-under-review;
  Ahsan&Wallace 2511.00177 ICLR2026 healthcare; SteerRM 2603.12795 reward-model; DeBiasLens 2602.24014 VLM/CVPR2026-flag),
  model-editing for stereotype (BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025), fairness/concept-erasure
  editing (Karvonen&Marks 2506.10922 NeurIPS2025 Mech-Interp-WS affine edit; SPLINCE 2506.10703 NeurIPS2025; H-SAL 2606.12088),
  identity/entity/PII unlearning (Entity-Level-Unlearning COLING2025; Not-Every-Token 2506.00876; DFSU 2601.15595), and example-reweighting
  debiasing (JTT/GEORGE/EIIL/LfF, carried). VERDICT: CCRG's three-part conjunction -- a DISCOVERED single absorber latent
  for ONE identity sub-context + a PARENT-preserving sub-context edit + scoring vs a SUB-CONTEXT-targeted dense direction
  u_sub -- is distinct from all five (each edits a WHOLE attribute/entity/example-set and preserves UNRELATED material; closest
  near-miss Ahsan&Wallace steers a single race-latent that CO-FIRES with 'incarceration' = entanglement not absorption, and
  concedes SAE steering is 'of marginal utility for realistic tasks'). Both-branches honest-null framing supplied (safety-WIN
  vs absorption-not-exhibited NULL bounded to the auditable edit primitive, connected to the existing 0/28-professions + toxicity-co-firing
  negatives). (B) M1' u_sub LABEL-EFFICIENCY: RETIRES the now-FALSE 'a single dense hyperplane structurally cannot localize
  to a sub-context / erasing the is-a-country direction removes all countries' argument -- u_sub IS a dense hyperplane and
  DOES localize, the testbed already carries its labels, and SPLINCE (preserves covariance with target label), Karvonen&Marks
  (affine edit, bias <2.5%, perf maintained) and H-SAL (label-free matches label-based) externally prove a labeled dense direction
  localizes/preserves utility. Supplies an exact DELETE/REPLACE list + BOTH M1' fork paragraphs (FORK-WIN: discovered single
  feature beats sub-context-labeled dense; FORK-MATCH: matches u_sub WITHOUT sub-context labels = label-efficiency/discovery,
  grounded in Peng 'Discover-not-Act' 2506.23845 verbatim thesis + label-free SAE 2506.01247) + an honest cost note (counterfactual-pair
  cost of grouping vs sub-context-label cost of u_sub). (C) CITATION REFRESH: 14 new grep-verified entries + carry-forward
  flags RESOLVED (Deng 2506.18141 UPGRADE->ACL2026; SAEmnesia 2509.21379 UPGRADE->ICML2026; SNCE 2509.21008 authors confirmed;
  Muchane 2506.01197 keep-preprint), BibTeX, corrections diff, unresolved-flags list, and an updated presentation-strip checklist.
  Outputs research_out.json + research_report.md (sections A-D).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_6/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_IlzAiXYWeUYH
type: research
title: 'CCRG iter-7 Positioning: Gated-Dense Prior Art, Localization-First Reposition'
summary: >-
  Positions the iteration-7 CCRG paper and refreshes the venue-locked citation set for GEN_PAPER_TEXT. Pure web research,
  $0, no code; builds on iter-5 (art_y_5u-bfJOq3V) and iter-6 (art_3zaa2xXEp8Az) without re-doing settled entries. FIVE deliverables.
  (A) GATED/CONDITIONAL ACTIVATION-EDITING SURVEY (the new load-bearing piece): VERDICT = gating a dense edit by a sparse/threshold
  detector is ESTABLISHED PRIOR ART, and the exact gated-dense operator the paper uses as a control is already published,
  so DENSE-SUB-ABL-GATED is a CONTROL, not a contribution. Four verified cites: CAST (2409.05907, ICLR 2025 Spotlight; condition-vector
  switch over the prompt's hidden state, gate fit on LABELED example sets), GUARD-IT (2605.12765, preprint; Sentence-Transformer
  Similarity Gate K(x)={j:sim(c_j,phi(x))>=T} over LABELED-forget clusters + norm-preserving rotation h'=(h-a*vhat)*||h||/||h-a*vhat||),
  GSS (2602.08901, preprint; the EXACT operator h'=h-G(|u^T h|>eps)*v Eq.3 / multi-component Eq.14, probe u + steer v OPTIMIZED
  on 1,000 memorization-labeled sequences with eps tuned to the 95th percentile), SADI (2410.12299, ICLR 2025 Poster; dynamic
  per-input steering via a contrastive-pair binary mask). The PLAN MIS-ATTRIBUTED the |u^T h|>eps formula to GUARD-IT; it
  is actually GSS (corrected). In ALL prior methods the gate is SUPERVISED; the SAE-specific contribution is therefore the
  TRAINING-FREE, LABEL-FREE DISCOVERY of WHERE to gate (the precise sub-context absorber marginal-attribution drops) plus
  the absorber's calibrated JumpReLU firing as a built-in calibration-free gate, grounded in Peng 'Discover-not-Act' (2506.23845).
  BOTH M1'' fork paragraphs supplied (WIN: discovered sparse handle beats even gated dense, advantage larger on absorption
  than co-firing cases => traces to structure not footprint; MATCH: gating not SAE-specific => value=label-free discovery;
  plus fallback FORK-c near-NOOP => scope to selective partial suppression). (B) LOCALIZATION-FIRST REPOSITION: drop-in abstract
  spine + intro opener leading with training-free auditable LOCALIZATION of homograph-polysemy absorption, stating localization-NOT-classification
  up front (toxicity unit AUC 0.762 ties/loses raw latents, trails dense 0.84-0.89; sub-attrs 0.63 vs 0.93), presenting the
  44-group safety screen (2/44 = white/straight, both homographs) as the HEADLINE LIMITATION-and-finding (absorption=lexical
  polysemy not demographic semantics; Ahsan-Wallace co-firing corroborates), naming the durable contribution triad (label-free
  discovery+editable feature-KG; a-priori recall-hole diagnostic=exploratory; absorption-regime selection wins). (C) METHOD-IDENTITY
  REFRAME: foreground single-absorber discovery (anchored set-cover effectively k=1; unit-vs-single-best-absorber ablation
  art_3WXWsaSoGMnK shows single absorber WINS; M7 multi-member adds collateral), demote multi-member grouping + C-track to
  secondary, 5 retitle options. (D) CLARITY FIXES: ONE canonical Georgia number (+0.561 CI[0.318,0.811], 2nd judge +0.465
  CI[0.289,0.658]) + exact footnote for the +0.743 safety-section re-run; concept-space-KL (u_sub 0.078 < whole-parent 0.102)
  vs judged-collateral (util_SUB 1.17 < util_whole 1.33, inverts) drop-in. (E) CITATIONS: inherited locked table carried forward
  verbatim + 6 new gated-steering cites with verified IDs/venues/full author lists + new-cite BibTeX + unresolved-flags list
  + 10-item presentation-strip checklist. Outputs research_out.json + research_report.md (sections A-E).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx4
type: research
title: >-
  CCRG iter-8 Positioning: Chanin/Max-Precision Delta, Concentration-as-Sharp-Gate, Localization+Editing Retarget, Locked
  Cites
summary: >-
  Pure web-research positioning pass (no code, $0 LLM spend, cpu_light) that finalizes the iteration-8 CCRG paper framing
  for GEN_PAPER_TEXT. Four deliverables: (D1) the precise LABEL-FREE delta of CCRG's anchored recall-hole-guided precision
  selection vs (i) Chanin's SUPERVISED absorption diagnostic and (ii) a simple max-precision selector, with the M5''' novelty-trim
  wording (set-cover/(1-1/e) demoted to MOTIVATION); (D2) a survey grounding the M3''' mechanism reframe -- the edit win is
  driven by latent CONCENTRATION/PRECISION acting as a sharper conditional gate than a footprint-matched dense projection,
  absorption being only ONE label-free source of concentration -- positioned against the feature-selection-for-steering literature
  so 'concentration not absorption' is grounded, not asserted; (D3) the M2''' retarget decision + BOTH retargeted abstract/intro
  spines (>=4 concentrated wins landed vs base-stays-thin), leading with 'training-free auditable LOCALIZATION + EDITING of
  homograph-polysemy absorption', safety-homograph null as headline limitation, with verified venue-area fit (ICLR primary
  per goal, ICML acceptable); (D4) the locked citation table carried verbatim from iter-6/iter-7 + new concentration/precision-steering
  cites with verified IDs/venues/authors + BibTeX + unresolved flags + a presentation-strip checklist. Builds on iter-7 art_IlzAiXYWeUYH
  (gated-steering prior art + localization-first reposition) and iter-6 art_3zaa2xXEp8Az (safety/u_sub positioning); does
  NOT redo those settled surveys.
runpod_compute_profile: cpu_light
question: >-
  For the iteration-8 CCRG paper (GEN_PAPER_TEXT), how should the positioning be finalized so that (1) the method's novelty
  is honestly trimmed to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber' with a precise stated delta
  vs Chanin's supervised absorption diagnostic AND vs a simple max-precision selector (set-cover/(1-1/e) demoted to motivation
  only); (2) the mechanism reframe 'the edit win tracks latent CONCENTRATION/PRECISION, not absorption structure' is POSITIONED
  against prior work relating per-feature precision/sparsity/selectivity to steering surgicality/conditional-gate sharpness;
  (3) the paper is retargeted to lead with training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption
  (ICLR primary, ICML acceptable), with both a wins-landed and a base-thin abstract/intro spine and the safety-homograph-confinement
  null as the headline limitation; and (4) the full citation set is locked (carry iter-6/iter-7 verbatim, add verified concentration/precision-steering
  cites, flag unresolved, invent nothing)?
research_plan: |-
  PURE WEB RESEARCH via the aii-web-tools skill (search -> fetch -> fetch_grep). NO code, NO datasets, NO experiments. $0 LLM/OpenRouter spend. Compute: cpu_light. Wall-clock budget ~3h. Output TWO files in the artifact workspace: research_out.json {title, summary, answer, sources[], follow_up_questions[]} and research_report.md (sections D1-D5). This pass FINALIZES positioning for GEN_PAPER_TEXT; it is a sibling/successor of iter-7 art_IlzAiXYWeUYH and iter-6 art_3zaa2xXEp8Az -- READ THOSE FIRST and CARRY THEIR SETTLED ENTRIES VERBATIM (do NOT re-survey gated-steering prior art or safety/u_sub positioning, which are settled). Both dependency research_out.json files are available; their locked-cite tables and abstract spines are the starting point.

  ========== STEP 0 -- GROUND IN THE DEPENDENCIES (no new searches; ~15 min) ==========
  Read the two dependency outputs already in this run:
    - iter-7 art_IlzAiXYWeUYH: /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_7/gen_art/gen_art_research_1/research_out.json (+ research_report.md). Extract: (a) the LOCKED gated-steering cites (CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint = exact h'=h-G(|u^T h|>eps)v operator; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint), all SUPERVISED-gate => gating is PRIOR ART, SAE value = label-free DISCOVERY of WHERE to gate; (b) the localization-first abstract spine + intro opener; (c) the full carried-forward locked-cite table listed in section (E); (d) Peng 'Discover-not-Act' 2506.23845 framing.
    - iter-6 art_3zaa2xXEp8Az: same dir under iter_6. Extract the safety-absorption cite-and-distinguish block + the u_sub label-efficiency positioning + the locked-cite refresh (14 entries). These are SETTLED -- carry, do not redo.
  Also anchor the load-bearing NUMBERS from the hypothesis (do NOT invent or alter; keep consistent across the report): large KG-vs-STRONGEST-ungated-dense (DENSE-SUB-ABL) = +1.00 CI[0.79,1.21] (the LEAD edit number); large KG-vs-footprint-GATED-dense = +1.58 CI[1.36,1.79] (the INFLATED/caveated robustness number -- gate driven to beta~2.97 over-erasure, gated collateral 0.290 vs its own ungated 0.021, ~14x more); Amazon = +0.75 CI[0.41,1.08] (named-entity homograph win, absorber 6846 max_kg 1.14); Bush = KG_MATCHES_GATED (parity), Cook structured; insult 13367 = +0.47 CO-FIRING win found by max-AUC NOT set-cover (the concentration-not-absorption evidence); Georgia 16009 / Jordan 540 = NO_MEANINGFUL_FORGET (distributed sense, max_kg 0.064/0.114, NOOP-identical 89%); safety 2/44 (white, straight; both homographs); named-entity 3/5 (Amazon/Bush/Cook); professions 0/28; homograph entities 3/64 (months only); selectivity corrected 722x/676x (16k/65k comparably surgical); cross-dictionary 65k full / layer-9 partial; the NEW fair control = DENSE-SUB-ABL-GATED-FAIR (u_sub gated by the precise d_sub detector AUC~1.0, bounded beta<=1).

  ========== STEP 1 -- DELIVERABLE D1: CHANIN-DELTA + MAX-PRECISION DELTA (M5''' novelty trim) ==========
  GOAL: write the precise paragraph stating what the LABEL-FREE anchor + recall-hole + precision-gate buys over (i) running Chanin's diagnostic directly and (ii) a simple max-precision selector; and supply the trim wording (set-cover/(1-1/e) = MOTIVATION only; method identity = 'anchored recall-hole-guided PRECISION SELECTION of a single absorber').
  SEARCH/FETCH:
    1a. fetch_grep the Chanin 2409.14507 FULL TEXT (try https://arxiv.org/html/2409.14507v3 first; fallback OpenReview PDF https://openreview.net/pdf/5fa0d903675ab0ae5df67d598ecfe21ce2dff8f7.pdf). Grep for: 'absorption fraction', 'absorption_fraction', 'probe', 'logistic regression', 'projection', 'ablation', 'first letter', 'main latent', 'encoder cosine', 'mean absorption'. EXTRACT precisely: (a) HOW the parent/main latent is identified -- confirm it uses a SUPERVISED logistic-regression probe (max encoder-cosine with the LR probe direction); (b) HOW the absorbing latent is identified -- ablation effect on a TASK-SPECIFIC logit (the first-letter logit) after projecting out the probe direction; (c) the absorption-fraction metric definition. CONFIRM the diagnostic REQUIRES (i) a supervised probe and (ii) a task label/logit, and that the empirical demonstration is almost entirely first-letter spelling (running example 'short'/'starts-with-S').
    1b. State the DELTA vs Chanin (label-free): CCRG's anchor is chosen by content-response RECALL on counterfactual pairs (available to every baseline, NO probe); the recall-hole is the parent's uncovered counterfactual pairs (NO logit); the precision-gate is firing-precision on the target sub-context (NO label beyond the counterfactual partition). Chanin DETECTS absorption on an individually-named latent GIVEN a supervised probe+logit; it does NOT propose parent+absorber as a usable, editable handle WITHOUT supervision, and is form-bound to spelling in its demonstrations. CCRG uses the FORM-FREE probe+ablation diagnostic ONLY to SCORE already-formed KG edges (non-circular), never to FORM units. So the buy is: training-free, label-free, form-free SURFACING of the precise sub-context latent that marginal-attribution selection silently drops.
    1c. MAX-PRECISION delta: the open question the iter-8 EXPERIMENT answers is whether the anchored recall-hole-guided set-cover beats a simple 'pick the single most precise latent firing on the target sub-context' (max-precision / S-prec) selector. Because every reported edit win is effectively k=1, the LIKELY answer is a TIE. Supply TWO conditional wordings: (TIE) trim to 'anchored recall-hole-guided PRECISION SELECTION of a single absorber'; present set-cover/(1-1/e) as MOTIVATION for the disjoint-support coverage view only, NOT a load-bearing guarantee; the discovery step's value over max-precision is the RECALL-HOLE ANCHORING that tells you WHICH sub-context to select a precise latent FOR (max-precision alone needs the sub-context handed to it). (SET-COVER ADDS SOMETHING) if any case shows k>1 or the recall-hole objective measurably helps, keep the set-cover framing but still demote (1-1/e) to motivation. Make clear GEN_PAPER_TEXT picks the wording matching the experiment's M3''' result.
    1d. Briefly search 'precision-weighted SAE latent selection' / 'recall-based vs precision-based SAE feature selection' / 'max-precision latent baseline steering' to confirm no existing named method already IS 'anchored recall-hole precision selection' (defensive novelty check); record near-misses (FGAA relevance/density filtering; CorrSteer correlation selection; Arad output-score filtering -- see D2) and state the delta (those select for steering EFFECT or correlation, not for the recall-hole an absorbed parent leaves).
  WRITE: research_report.md section D1 = the Chanin-and-max-precision delta paragraph (drop-in for the Related Work / Method-identity subsection), plus the two conditional trim sentences.

  ========== STEP 2 -- DELIVERABLE D2: CONCENTRATION-AS-SHARP-GATE (M3''' mechanism reframe grounding) ==========
  GOAL: ground the claim 'the edit advantage is a property of a PRECISE/CONCENTRATED latent acting as a SHARPER conditional gate than a footprint-matched dense projection; absorption is ONE label-free-discoverable source of concentration, not the cause of the win' against prior work relating per-feature precision/sparsity/selectivity to steering surgicality. This makes 'concentration not absorption' POSITIONED, not merely asserted.
  VERIFIED ANCHOR CITES (confirm IDs/venues/authors via fetch_grep of arXiv Comments; flag if unresolved):
    2a. Arad, Mueller, Belinkov -- 'SAEs Are Good for Steering -- If You Select the Right Features' (arXiv 2505.20063; verify EMNLP 2025). KEY: introduces input vs OUTPUT scores; filtering OUT low-output-score features gives 2-3x steering improvement => the right FEATURE SELECTION (a precise, output-effective feature), not the steering mechanism, drives steering quality. This is the HEADLINE cite for 'which precise latent you pick is what matters' -- directly supports CCRG's 'label-free discovery of WHERE to gate' and the concentration reframe.
    2b. CorrSteer -- 'Generation-Time LLM Steering via Correlated Sparse Autoencoder Features' (arXiv 2508.12535; Cho, Wu, Koshiyama; Comments say ICML 2026 -- FLAG/verify, cite preprint if unresolved). Correlation-based selection extracts 'more relevant features, thereby reducing spurious correlations' => precise/specific selection reduces collateral.
    2c. FGAA -- 'Steering LLMs with Feature Guided Activation Additions' (arXiv 2501.09929; verify authors/venue). Relevance + density/'concreteness' filtering: high-DENSITY (frequently-firing) features dominate despite limited task specificity and must be filtered out => low-density + high-precision = concentration = a clean handle. Directly supports the concentration axis (sparse firing + high per-sub-context precision).
    2d. Sparse Activation Steering -- 'Steering Large Language Model Activations in Sparse Spaces' (arXiv 2503.00177; verify). Scaling SAE width increases steering-vector sparsity/monosemanticity => 'better disentangle features by reducing overlap', improving intervention precision => sparser/more-concentrated => sharper gate.
    2e. Anthropic 'Scaling Monosemanticity' (Templeton et al. 2024, transformer-circuits.pub; cite as the canonical monosemanticity source). The precise-boundary claim: monosemantic features 'stop responding the moment text diverges from the target concept' -> a precise feature's firing IS a sharp conditional gate. Use to ground the conditional-gate-sharpness intuition.
    2f. Tie to the LOCKED iter-7 gating cites (CAST/GSS/GUARD-IT/SADI): the gating MECHANISM is prior art and supervised; a concentrated latent's calibrated JumpReLU firing is itself a sharp, threshold-free conditional gate, whereas a footprint-matched DENSE projection must be driven to beta~3 over-erasure to match the same forget (=> ~14x more collateral on 'large'). So the edit advantage = sharper conditioning from a concentrated detector, NOT absorption per se.
  SEARCH (to find any stronger/more-direct cite and avoid missing an obvious one): 'feature selectivity predicts steering side effects', 'sparse precise feature cleaner edit handle lower collateral', 'per-feature specificity steering fluency tradeoff', 'conditional steering reduces collateral selective feature'. Record 1-2 best additional hits with verified IDs.
  WRITE: research_report.md section D2 = the concentration-as-sharp-gate positioning paragraph(s): (i) state the property the method should select for = per-sub-context PRECISION x sparse firing = CONCENTRATION; (ii) cite 2a-2e that selection of a precise/specific/low-density feature is the established driver of clean steering; (iii) state that absorption is one label-free-discoverable source of concentration (absorber marginal-attribution drops) but a concentrated CO-FIRING latent (insult, found by max-AUC not set-cover) also wins, so the win predictor is concentration; (iv) explicitly DROP/heavily-qualify 'the win traces to the absorption structure the method discovers'.

  ========== STEP 3 -- DELIVERABLE D3: RETARGET/VENUE + BOTH ABSTRACT/INTRO SPINES (M2''' retarget) ==========
  GOAL: decide and justify leading the paper with 'training-free auditable LOCALIZATION + EDITING of homograph-polysemy absorption', confirm venue-area fit, and supply BOTH spines.
    3a. VENUE FIT: confirm via iclr.cc/Conferences/2026/CallForPapers and icml.cc/Conferences/2026/CallForPapers that the framing fits. NOTE the GOAL says 'Target ICLR primary, ICML fallback' while THIS artifact-direction says 'ICML primary acceptable, ICLR fallback' -- TREAT THE GOAL AS AUTHORITATIVE (ICLR primary) but explicitly state fit for BOTH and resolve the tension in-report. ICLR 2026 lists 'Interpretability, fairness, privacy, and ethical AI' as an area (fits). NOTE ICML 2026 main-track submission closed ~Jan 28 2026 (so the live cycle for a mid-2026 paper is ICLR 2026 / the next ICML); the deliverable is AREA fit, not a deadline. Map the contribution to the reviewer-evaluable areas named in the goal (clustering methods, feature selection, classification, knowledge graphs, knowledge extraction, applied knowledge discovery, text data analytics, LLMs/deep learning) -- the localization + editable feature-KG + label-free discovery framing fits these far better than a classification-win framing (the paper makes NO out-classifies-dense claim). State this mapping explicitly so the title/abstract commit to localization+editing, not classification/steering wins.
    3b. RETARGET DECISION: lead with auditable LOCALIZATION (+ EDITING on concentrated features) of homograph-polysemy absorption; safety-homograph-confinement null (2/44, both homographs) as the HEADLINE LIMITATION-and-finding; the concentrated-feature edit (large +1.00, Amazon +0.75) as a SCOPED capability bounded by the fair gated control; classification SUPPORTING/within-SAE; router DEMOTED to exploratory. Build directly on the iter-7 localization-first spine (carry it, then update for: de-inflation to +1.00-lead; the new fair bounded-beta d_sub control; concentration-not-absorption mechanism; set-cover-as-motivation; both forget instruments; unified gate operator).
    3c. SUPPLY BOTH SPINES (drop-in abstract ~150-220 words + intro opener ~1 para each):
       - OUTCOME A (>=4 independent concentrated wins LANDED: large, Amazon + Bush/Cook/wider-vocab under the fair bounded-beta d_sub-gated control): the sparse-gated EDIT is a broader load-bearing capability. Abstract foregrounds: training-free label-free localization of homograph-polysemy absorption + an editable feature-KG; the edit win LED by KG-vs-STRONGEST-dense (+1.00 on large; never lead with +1.58) on >=4 concentrated features, shown to track CONCENTRATION (max-precision ablation) and to beat the genuinely-fair bounded-beta d_sub-gated dense control; safety null as capping scope.
       - OUTCOME B (base STAYS THIN, n~=2; or the fair gated control MATCHES KG): lead FULLY with the auditability/localization SPINE + the safety-homograph-confinement NULL as the finding; the edit is a scoped capability on concentrated features; if fair-gated matches => contribution = label-free DISCOVERY of where to gate (gating is prior art); concentration-not-absorption reframe central; set-cover = motivation only.
       Each spine must: state localization-NOT-classification up front; name the durable contribution triad (label-free discovery + editable feature-KG; recall-hole screening diagnostic = exploratory; absorption-regime/concentration selection wins where the signature holds); headline the homograph-confined safety null; and avoid the inflated +1.58-vs-footprint-gated number as the lead.
  WRITE: research_report.md section D3 = venue-fit justification + retarget decision + BOTH abstract+intro spines, clearly labeled OUTCOME-A and OUTCOME-B with a one-line selector telling GEN_PAPER_TEXT which to use based on the M1'''/M2''' experiment results.

  ========== STEP 4 -- DELIVERABLE D4: CITATION FINALIZATION + D5: PRESENTATION-STRIP CHECKLIST ==========
    4a. CARRY FORWARD the FULL locked-cite table from iter-7 section (E) + iter-6, VERBATIM (Chanin 2409.14507 NeurIPS2025; Feature-Hedging 2505.11756; AxBench 2501.17148 ICML2025; SAEBench 2503.09532 ICML2025; CanonicalUnits 2502.04878 ICLR2025; Matryoshka 2503.17547 ICML2025; Farrell 2410.19278 NeurIPS2024-Safe-GenAI-WS; SPLINCE 2506.10703 NeurIPS2025; Karvonen-Marks 2506.10922 NeurIPS2025-MechInterp-WS; Ahsan-Wallace 2511.00177 ICLR2026; BiasEdit 2503.08588 TrustNLP@NAACL2025; Collapsed-LMs 2410.04472 ICLR2025; Entity-Level-Unlearning COLING2025; Deng 2506.18141 ACL2026; SAEmnesia 2509.21379 ICML2026; Peng 2506.23845; CRISP 2508.13650 ACL2026; SAUCE 2503.14530 WITHDRAWN/ICCV2025-CVF; SSPU 2505.24428 EMNLP2025; LEACE 2306.03819 NeurIPS2023; CAST 2409.05907 ICLR2025-Spotlight; GUARD-IT 2605.12765 preprint; GSS 2602.08901 preprint; SADI 2410.12299 ICLR2025-Poster; PID-Steering 2510.04309 preprint; DAC 2406.17563 preprint; the iter-6 debiasing set; JTT/GEORGE/EIIL/LfF; DiffCoEx/WGCNA; Nemhauser-Wolsey-Fisher/Feige set-cover; CDLC 2505.07073; Veitch 2106.00545; Kaushik CAD ICLR2020; CEBaB 2205.14140; ParaDetox). Do NOT re-verify settled locks; just list them with their locked venues and flag the ones the dependencies already flagged unresolved (GUARD-IT/GSS/DAC venues; DeBiasLens CVPR2026; Deng dual-listing; Karvonen-Marks workshop).
    4b. ADD the NEW concentration/precision-steering cites, each with fetch_grep-VERIFIED arXiv ID + Comments-field venue + FULL author list: Arad-Mueller-Belinkov 2505.20063 (verify EMNLP2025); CorrSteer 2508.12535 Cho-Wu-Koshiyama (Comments=ICML2026, FLAG); FGAA 2501.09929; Sparse-Activation-Steering 2503.00177; Anthropic Scaling-Monosemanticity (Templeton et al. 2024, transformer-circuits.pub -- cite by URL, no arXiv). For any venue not grep-confirmable from the Comments field, cite as PREPRINT and add to the unresolved-flags list. INVENT NOTHING.
    4c. EMIT BibTeX for every NEW cite added this iteration (the concentration set); carry the iter-6/iter-7 BibTeX by reference (note GEN_PAPER_TEXT already has it).
    4d. PRESENTATION-STRIP CHECKLIST (research_report.md section D5), 10-12 items: (1) lead title/abstract with 'training-free auditable LOCALIZATION (+ EDITING) of homograph-polysemy absorption'; (2) lead the edit table with KG-vs-STRONGEST-ungated-dense (+1.00 on large) -- caveat the +1.58-vs-footprint-gated number with the beta~2.97 over-erasure note (gated collateral 0.290 vs its own ungated 0.021); (3) report BOTH forget instruments (completion-drop AND sub-probe-drop) side by side and match operators on a BEHAVIORAL measure, not next-token KL; (4) UNIFY the gate operator into ONE definition across large/Amazon/Bush (or document the per-case clamp in-table: 3%-global-footprint vs 95%-X-rate); (5) present set-cover/(1-1/e) as MOTIVATION only; method identity = 'anchored recall-hole-guided precision selection of a single absorber'; (6) state the mechanism as CONCENTRATION/PRECISION not absorption (insult co-fires yet wins; Georgia/Jordan absorb yet lose); (7) safety-homograph null (2/44) = headline limitation; (8) state localization-NOT-classification (no SAE unit out-classifies a dense probe on any task); (9) router = exploratory (out-of-sample Wilson includes 0.5); (10) corrected selectivity (722x/676x; 16k/65k comparably surgical), cross-dictionary 65k full/layer-9 partial; (11) demote multi-member grouping + C-track to secondary (single absorber wins, multi-member adds collateral); (12) STRIP all iteration/rebuttal/infra scaffolding (M1''/M1'''/art_ tags/'iter-7 reviewer'/GPU-hours).

  ========== STEP 5 -- ASSEMBLE OUTPUTS ==========
  Write research_out.json with: title; summary; answer (a tight synthesis of D1-D5 with the key verdicts: method-identity = anchored recall-hole precision selection / set-cover=motivation; mechanism = concentration not absorption, positioned via 2505.20063/CorrSteer/FGAA/SAS/monosemanticity; retarget = localization+editing lead with both spines; cites locked); sources[] (every fetched URL with a one-line evidence note: Chanin body, the 4-5 concentration cites with verified venue/authors, ICLR/ICML CfP pages, plus the carried iter-6/iter-7 anchors by reference); follow_up_questions[] (e.g.: did M3''' show set-cover beats or ties max-precision? did M2''' land >=4 wins -> use OUTCOME-A or OUTCOME-B spine? did M1''' fair bounded-beta d_sub-gated control get beaten or matched? are the CorrSteer/Arad venues confirmable before camera-ready?). Write research_report.md with sections D1-D5 as specified, including all drop-in paragraphs, both spines, the locked+new cite table, BibTeX for new cites, unresolved-flags list, and the presentation-strip checklist.

  ========== CONTINGENCIES / FAILURE MODES ==========
  - If the Chanin HTML body is inaccessible, use the OpenReview PDF (fetch_grep) or the NeurIPS 2025 poster page; the supervised-probe + first-letter-logit + absorption-fraction facts are already corroborated by search snippets -- confirm and cite, do not block.
  - If a new concentration cite's venue is not grep-confirmable from the Comments field, cite as preprint + add to unresolved flags (NEVER invent a venue). CorrSteer's 'ICML 2026' is from Comments -> keep but flag (large 45-page preprint, may be a workshop/under-review listing).
  - If the concentration-steering literature turns out thinner than expected, fall back to the strongest anchors (Arad 2505.20063 + the locked CAST/GSS + Anthropic monosemanticity precise-boundary claim) -- these alone ground the reframe; do not pad with weak cites.
  - If venue CfP pages are unreachable, rely on the known areas (ICLR 'Interpretability, fairness, privacy, ethical AI'; reviewer-evaluable areas in the goal) and proceed; venue choice is ICLR-primary per the goal regardless.
  - Keep ALL load-bearing numbers consistent with the hypothesis; if a number is needed that is not in the hypothesis, mark it [VERIFY-AT-WRITE] rather than inventing.
  - Strictly $0 LLM spend (web research only); no OpenRouter calls.
explanation: >-
  This research artifact finalizes the iteration-8 CCRG paper positioning so GEN_PAPER_TEXT can write a defensible draft regardless
  of how the parallel iter-8 experiments (M1''' fair gated control, M2''' expanded base, M3''' max-precision ablation) land.
  The iter-7 reviewer raised three publication-gating majors that are framing/positioning problems this artifact must resolve:
  (R6/M5''') the set-cover/(1-1/e) framing oversells a step that is effectively k=1, so the novelty must be trimmed to 'anchored
  recall-hole-guided precision selection' with a precise stated delta vs Chanin's SUPERVISED diagnostic and vs a simple max-precision
  selector; (R3/M3''') the claim 'the win traces to absorption structure' is unsupported because a concentrated CO-FIRING
  latent also wins, so the mechanism must be reframed to latent CONCENTRATION/PRECISION and POSITIONED against the established
  feature-selection-for-steering literature (where selecting a precise/specific/low-density feature is the known driver of
  clean steering); (R2/M2''') the positive edit base is n~=2, so the paper must retarget to lead with auditable localization+editing
  of homograph-polysemy absorption with the safety-homograph null as the headline limitation, and needs both a wins-landed
  and a base-thin abstract/intro spine ready. The artifact also locks the citation set (carrying the iter-6/iter-7 venue-verified
  table verbatim and adding verified concentration/precision-steering cites) and supplies a presentation-strip checklist.
  Without this positioning pass the paper would lead with the inflated +1.58 number, an oversold set-cover guarantee, and
  an unsupported absorption-causation claim -- exactly the three things the reviewer flagged as blocking. Pure web research
  is the right tool: every deliverable is literature synthesis, delta articulation, venue-area mapping, and citation verification
  -- no computation, and it must run in parallel with the experiments so its both-outcome wording is ready for GEN_PAPER_TEXT.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [5] HUMAN-USER prompt · 2026-06-18 19:51:21 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

## Task: `gen_art_evaluation_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:12 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Evaluate experimental results using domain-appropriate methods, metrics, and analysis techniques.
When in doubt, prefer more metrics over fewer — but only ones that make sense for the domain.
</task>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_evaluation_1_idx3
type: evaluation
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflate the Edit Headline, Lay Both Forget Instruments Side-by-Side, Show Concentration>Absorption
  Predicts the Win, and Lock the Georgia +0.561 Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the EXISTING iter-6/7 edit data (art_Cgk9ETiZfvtl, art_ZxVw0e4seBq3, art_3WXWsaSoGMnK).
  Following the project integrity-lock pattern (COMPUTE-from-source then COMPARE-to-stored, never overwrite), it produces
  GEN_PAPER_TEXT drop-in numbers that are robust to any truncation of the new iter-8 experiments: (1) the DE-INFLATED lead
  KG-vs-strongest-ungated-dense (+1.00 on 'large') reconciled against the inflated +1.58-vs-footprint-gated with its beta~2.97
  over-erasure stats; (2) BOTH meaningful-forget instruments (gold-completion-drop AND frozen sub-probe-drop) per case/operator
  side-by-side, with an instrument-disagreement metric proving next-token-KL matching != behavioral matching; (3) a per-case
  CONCENTRATION proxy correlated with the win/meaningful-forget outcome vs the absorption-regime label (concentration predicts,
  absorption does not); (4) the consolidated Georgia +0.561 RETRACTION (iter-6 win sat at a near-NOOP operating point); plus
  an operator-divergence flag (3%-global-footprint vs 95%-X-rate gate) the new experiments must unify. Emits eval_out.json
  (exp_eval_sol_out) with metrics_agg, per-case datasets, cross_checks, and cross-checked drop-in paper_wording.
runpod_compute_profile: cpu_heavy
metrics_descriptions: |-
  PURE-ANALYSIS INTEGRITY LOCK. No GPU, no model load, no LLM calls ($0). Read-only over three stored experiment outputs. EVERY headline value is RECOMPUTED from source columns, then COMPARED to the stored expectation; mismatches are reported in metadata.cross_checks with an explanatory note and NEVER overwritten (this mirrors art_w7p8du2N1f0Y / art_-k4Yg-l4NaNO). Use a fixed seed (1234) for every bootstrap so results are deterministic and re-checkable.

  === INPUTS (exact paths; load full_method_out.json, fall back to method_out.json if absent) ===
  - D1 = art_Cgk9ETiZfvtl @ /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1/full_method_out.json. Use metadata.per_case[*] (5 cases: target_subcontext in {Georgia, large, Jordan, United States, insult}), metadata.summary, datasets.gated_dense_per_prompt (288 rows; columns predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-operator judged utilities + NOOP-identical + model-internal signals), datasets.kg_vs_gated_per_case (5 rows). Also read this dir's method.py to extract the EXACT joint-utility formula, paired_bootstrap_diff, completion_drop, fit_sub_probe and calibrate_gate_tau definitions so recomputation is faithful.
  - D2 = art_ZxVw0e4seBq3 @ .../iter_7/gen_art/gen_art_experiment_2/full_method_out.json. Use metadata.downstream[*] (3 cases: Amazon, Bush, Georgia-control), datasets.downstream_edit_per_prompt (90 rows), datasets.downstream_edit_per_case, metadata.screen_table (per-entity absorber_precision/hole/jaccard for Amazon/Bush/Cook).
  - D3 = art_3WXWsaSoGMnK @ .../iter_6/gen_art/gen_art_experiment_1/full_method_out.json. Use the Georgia kg_vs_dense_per_case entry (joint_diff_CI_KG_vs_SUB, matched_target_forget_kl, fork_verdict) and datasets.unlearn_per_prompt for Georgia if a recompute is needed.

  === GROUP A - DE-INFLATION (M1''' + M3''' lead number) ===
  A1. Mean joint utility per operator per D1 case: recompute from gated_dense_per_prompt judged-utility columns using the exact joint formula read from method.py (joint = judged retain-utility combined with fluency). Cross-check computed kg/gated/sub_joint_utility_mean against stored metadata.per_case[*].{kg_joint_utility_mean, gated_joint_utility_mean, sub_joint_utility_mean}. Expected for large: KG=1.8704, GATED=0.2870, SUB=0.8704.
  A2. Paired-bootstrap (B=10000, seed 1234, over preservation prompts) joint diffs per case: (i) DE-INFLATED LEAD = KG-ABL minus DENSE-SUB-ABL (ungated, strongest dense); (ii) INFLATED = KG-ABL minus DENSE-SUB-ABL-GATED. Cross-check (i) against stored joint_diff_CI_KG_vs_SUB_secondary and (ii) against joint_diff_CI_KG_vs_GATED. Expected for large: lead = +1.000 CI[0.787,1.213] (n=36); inflated = +1.583 CI[1.361,1.787]. Verify the reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 hold to <1e-3.
  A3. Over-erasure stats for large (and report for all cases): gated retain-collateral KL = retain_collateral_kl_gated_mean (0.290) vs ungated SUB retain_collateral_kl_sub_mean (0.021) -> over_erasure_ratio = 0.290/0.021 ~= 13.8x; the beta the gate was driven to = scale_gated_beta (2.967) vs scale_sub_beta (0.649); gated_vs_ungated_collateral_CI (diff -0.269, excl_0 true => gated has MORE collateral than its OWN ungated form). Also report collateral_diff_CI_KG_vs_GATED (+0.290) and collateral_diff_CI_KG_vs_SUB_secondary (+0.021).
  A4. Emit per-case de-inflation rows {case, kg/gated/sub joint means, lead_diff+CI, inflated_diff+CI, gated_collateral, sub_collateral, over_erasure_ratio, scale_gated_beta, scale_sub_beta, gated_vs_ungated_collateral_excl_0}. metrics_agg gets de_inflated_lead_large=+1.00 (with CI), inflated_gap_large=+1.58 (with CI), over_erasure_ratio_large~=13.8.

  === GROUP B - BOTH FORGET INSTRUMENTS SIDE-BY-SIDE (M4''') ===
  B1. For every D1 case x operator at the matched point, tabulate the TWO behavioral instruments: (a) gold-completion-drop = metadata.per_case[*].completion_drop_matched[op].drop_vs_noop with drop_ci/excl_0; (b) frozen sub-probe positive-rate drop = subprobe_drop[op].drop (and NOOP pos_rate, auc). Build one row per (case, operator) with both numbers + their CI/excl_0.
  B2. Instrument-disagreement metric, per case, on the decisive KG-vs-GATED contrast: completion_contrast = completion_drop[KG]-completion_drop[GATED]; subprobe_contrast = subprobe_drop[KG]-subprobe_drop[GATED]. Report sign_divergence = (sign(completion_contrast) != sign(subprobe_contrast)) and the signed magnitudes. For large this fires: completion favors GATED (KG 0.072 vs GATED 1.080 => completion_contrast=-1.008) while sub-probe favors KG (KG 0.417 vs GATED 0.0 => subprobe_contrast=+0.417) -> sign_divergence=TRUE. Also compute, per case, a rank-disagreement (Spearman or Kendall-tau between the two instruments' operator orderings over {KG,GATED,SUB}).
  B3. Quantify 'next-token-KL matching != behavioral matching': all operators are scaled to the SAME matched_target next-token KL, yet at that point completion_drop and subprobe_drop differ sharply across operators (e.g. large: KL-matched but completion_drop spans 0.072..1.080 and subprobe_drop spans 0.0..0.917). Report, per case, the across-operator spread (max-min) of each behavioral instrument at the KL-matched point as the divergence evidence, and recommend (for paper_wording) matching operators on a BEHAVIORAL measure (sub-probe drop or completion accuracy) rather than next-token KL. Flag that the load-bearing large completion CI is over only n=4 probes (RIGOR caveat) -- read drop_ci.n.
  B4. metrics_agg gets instrument_disagreement_cases (list of cases with sign_divergence=TRUE; expect {large}), and the large KG-vs-GATED contrast pair (-1.008 completion, +0.417 sub-probe).

  === GROUP C - CONCENTRATION-vs-ABSORPTION PREDICTOR (M3''' decisive descriptive) ===
  C1. Assemble a pooled case table across D1 (large, Georgia, Jordan, United States, insult) and D2 (Amazon, Bush). For each case read: absorber_precision (per-sub-context precision), gate_footprint_used / gate_target_footprint (firing footprint f_kg), firing_jaccard_with_parent, max_forget_kg (single-latent next-token-KL ceiling = edit leverage), regime label ('absorption' vs 'co-firing'), and outcomes: win_binary = (fork_verdict==KG_BEATS_GATED_DENSE...), meaningful_forget_binary = kg_can_forget (D1) / non-trivial-forget (D2), adv_continuous = joint KG-vs-GATED diff. For D2 use downstream[*] fields (gate_calibration, max_forget_kg, fork_verdict, joint_diff_CI_KG_vs_GATED) and screen_table absorber_precision.
  C2. CONCENTRATION PROXY (primary): concentration = absorber_precision * (1 / f_kg) read from stored fields (per the direction: per-sub-context precision x inverse footprint). ALSO compute two robustness variants and report all three: (v2) absorber_precision * max_forget_kg (precision x single-latent leverage), (v3) absorber_precision * (1 - firing_jaccard_with_parent) * sub_probe_max_drop. Rank/z-score each case under each proxy. The qualitative pattern to confirm: concentrated cases (large prec 1.0, Amazon prec 0.99/max_kg 1.14, insult high-precision co-firing) WIN; distributed cases (Georgia/Jordan country sense, US co-firing) LOSE -- crossing BOTH regime labels.
  C3. PREDICTIVE COMPARISON: compute point-biserial (proxy continuous vs binary outcome) and Spearman (proxy vs adv_continuous) for (a) each concentration proxy and (b) the absorption-regime binary label, each with a bootstrap CI (B=10000, seed 1234, resampling cases). predictive_delta = corr(concentration_proxy, outcome) - corr(absorption_label, outcome). EXPECT concentration to track win/meaningful_forget better than the absorption label (absorption label is near-uninformative because wins/losses cross it). Because n is small (~7 cases) this is EXPLICITLY descriptive: report the delta + CI but label it 'descriptive, small-n' in the row and in paper_wording. Cross-check the absorption-mean-vs-cofiring-mean comparison the paper currently leans on: adv_absorption_mean (1.583) vs adv_cofiring_mean (0.372) from metadata.summary, and note it is a 1-case-vs-2-case-mean (thin/circular) basis -- the per-case concentration correlation supersedes it.
  C4. metrics_agg gets concentration_vs_absorption_predictive_delta (primary proxy, with CI), the per-proxy correlations, and a boolean concentration_outpredicts_absorption.

  === GROUP D - GEORGIA +0.561 RETRACTION (M1''' carry / M6) ===
  D1. From D3 recompute (or read+cross-check) the iter-6 Georgia KG-vs-SUB joint = +0.5606 CI[0.318,0.811] n=44 at matched_target_forget_kl=0.0517. If recomputing from unlearn_per_prompt, use the method.py joint formula; else cross-check the stored CI.
  D2. From D1 (iter-7) read the near-NOOP evidence at/near that operating point for Georgia: max_forget_kg=0.0647 (17-30x smaller than dense ceilings), noop_identical_fraction.FORGET['KG-ABL']=0.889, subprobe_drop['KG-ABL'].drop=0.075, completion_drop_matched['KG-ABL'].drop_ci.excl_0=false, fork_verdict=NO_MEANINGFUL_FORGET, and the iter-7 KG-vs-GATED Georgia adv=+0.174 / KG-vs-SUB=+0.197 (vacuous, KG barely edits).
  D3. RETRACTION ROW + STATEMENT: the iter-6 +0.561 'win' sat at a near-NOOP operating point (KG won by barely editing, and also barely forgot); it is retracted/recontextualized as clean low-collateral PARTIAL suppression, not meaningful unlearning. metrics_agg gets retraction_iter6_georgia_adv=+0.561, retraction_iter6_matched_kl=0.0517, retraction_iter7_max_forget_kg=0.0647, retraction_noop_identical=0.889, retraction_subprobe_drop=0.075, retraction_status='RETRACTED_NEAR_NOOP'.

  === GROUP E - OPERATOR-DEFINITION DIVERGENCE FLAG (MINOR 4 / M1''' unify) ===
  E1. Cross-check the two 'footprint-matched gated dense' operators are NOT identical: D1 = global-neutral-pool footprint gate (calibrate_gate_tau; gate_tau~=101, gate_footprint_used~=0.025-0.028, gate_target_footprint~=0.014-0.03, ~3% global firing). D2 = gate_calibration.method=='footprint_match_clamped' on X-POSITIVE firing rate clamped ~0.95 (gate_fire_rate_X~=0.9467, gate_fire_rate_sibling~=0.045). Set metrics_agg.operator_divergence_flag=TRUE with both calibration descriptors and a note that the iter-7 headline aggregates a 3%-global-footprint comparison (large) with a 95%-X-rate comparison (Amazon); the new iter-8 experiments must unify into ONE gate operator (or document any per-case clamp in-table).

  === OUTPUT (eval_out.json, schema exp_eval_sol_out; validate full/mini/preview <100MB via aii-json + aii-file-size-limit) ===
  - metrics_agg: {de_inflated_lead_large, inflated_gap_large, over_erasure_ratio_large, instrument_disagreement_cases, large_kg_vs_gated_completion_contrast, large_kg_vs_gated_subprobe_contrast, concentration_vs_absorption_predictive_delta, concentration_outpredicts_absorption, retraction_* fields, operator_divergence_flag, absorption_mean_vs_cofiring_mean_basis_note}.
  - datasets: de_inflation_per_case (>=5 D1 rows + D2 rows), both_instrument_per_case_op (one row per case x {KG,GATED,SUB} with completion_drop+CI and subprobe_drop), concentration_predictor_per_case (~7 rows with proxies+outcomes+labels), retraction_per_case (Georgia row), operator_divergence (2 rows). Each dataset row must carry predict_* / value STRING fields if the project schema requires non-null string predictions (mirror the iter-5/6 validator gotcha: every example needs a predict_* string).
  - metadata.cross_checks: array of {name, computed, stored, abs_diff, rel_diff, match (bool at tol: 1e-3 for point stats; CI-overlap for bootstrap), note}. Include at minimum the A1 utility means, A2 lead/inflated diffs+CIs, D1/D2 collateral CIs, the iter-6 Georgia +0.561, and the summary adv_absorption/adv_cofiring means.
  - metadata.paper_wording: drop-in strings (cross-checked) for: (W1) de-inflated lead '+1.00 vs the strongest ungated dense on large (CI[0.79,1.21]), with +1.58 vs a footprint-matched gate reported only as a robustness check handicapped by beta~3 over-erasure (gated collateral 0.29 = 13.8x its own ungated 0.021)'; (W2) instrument disagreement 'at the next-token-KL-matched point the two forget instruments disagree in sign for large (completion favors the gated dense by 1.01, frozen sub-probe favors KG by 0.42), so KL-matching does not equalize behavioral forgetting; operators should be matched on a behavioral measure'; (W3) concentration finding 'the edit-win predictor is latent concentration/precision, not absorption: wins span an absorption case (large) and a co-firing case (insult), losses are distributed senses (Georgia/Jordan); a precision-x-inverse-footprint proxy tracks the outcome where the absorption-regime label does not (descriptive, n~7)'; (W4) retraction 'the iter-6 Georgia +0.561 win sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical on 89% of forget prompts, frozen sub-probe drop 0.075); it is retracted as low-collateral partial suppression, not meaningful unlearning'; (W5) operator unification note.

  === FAILURE / EDGE HANDLING ===
  - If a per-prompt judged-utility column is missing or the joint formula cannot be reproduced exactly, fall back to cross-checking the stored *_joint_utility_mean and *_diff_CI directly and mark the cross_check note 'stored-only (recompute unavailable)'; do not fabricate.
  - If a recomputed bootstrap CI does not overlap the stored CI, record match=false with a note (seeding/resample-unit difference) -- report, never overwrite.
  - Some D1 cases (insult, US) are regime='co-firing'; keep them in Group C (they are load-bearing for the concentration claim) but exclude US/insult from any absorption-only aggregate, matching metadata.summary.us_excluded_gate.
  - D2 Amazon/Bush use the 95%-X-rate gate, so their joint diffs are NOT directly comparable to D1's 3%-global-footprint diffs; carry them as supporting concentration points flagged with the operator note (Group E), not pooled into the D1 lead CI.
  - Keep all three output variants <100MB; per-prompt source datasets are tiny (288/90/~hundreds rows) so full retention is fine.
metrics_justification: >-
  These metrics are exactly the four reviewer-gating integrity issues (R1 de-inflation, R3 concentration-not-absorption, R4
  operator divergence, R5 instrument rigor) reduced to arithmetic over data that ALREADY exists, so GEN_PAPER_TEXT gets defensible
  drop-in numbers no matter how the new iter-8 edit experiments turn out. (1) The DE-INFLATED lead matters because the abstract
  currently leads with the largest, least-defensible gap: the +1.58 is KG beating a gated dense that was driven to beta~2.97
  over-erasure (its own collateral 0.29 is 13.8x its ungated 0.021), i.e. a handicapped control. Recomputing KG-minus-strongest-ungated-dense
  (+1.00, CI[0.79,1.21]) from the stored per-prompt utilities, and proving the +1.58/+1.00 reconciliation against the stored
  utility means, gives the paper an honest headline and pre-empts the #1 blocker. (2) Laying BOTH forget instruments side-by-side
  and quantifying their sign-disagreement at the KL-matched point is the only way to honestly support 'meaningful forget':
  the completion-drop and sub-probe-drop instruments rank KG vs the gated dense in OPPOSITE directions for the load-bearing
  large case, which both proves the forget is real on the behavioral sub-probe AND shows that matching on next-token KL does
  not equalize behavior -- a rigor fix the paper must state, not hide. (3) The concentration-vs-absorption predictor is the
  decisive evidence reframe: the wins cross both regime labels (absorption 'large' wins, co-firing 'insult' wins; absorption
  'Georgia/Jordan' lose), so a per-case precision-x-inverse-footprint proxy correlating with the outcome better than the absorption-regime
  label directly substantiates 'the win traces to concentration, not the absorption structure the method discovers' and retires
  the thin 1-vs-2-case absorption_exceeds_cofiring aggregate. It is correctly scoped as small-n descriptive. (4) Consolidating
  the Georgia +0.561 retraction closes the loop on a now-known-misleading prior headline by showing, in one row, that the
  win sat at a near-NOOP operating point (tiny max forget KL, 89% NOOP-identical, sub-probe barely moved) -- protecting the
  paper's integrity. The operator-divergence flag surfaces the 3%-global-footprint vs 95%-X-rate inconsistency the new experiments
  must unify. Because the whole artifact is a read-only, $0, deterministic recompute-and-cross-check, it is immediately runnable
  and fully robust to truncation of the expensive new GPU experiments, which is precisely its strategic value as the always-produced
  clean deliverable.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3WXWsaSoGMnK
type: experiment
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 2 ---
id: art_Cgk9ETiZfvtl
type: experiment
title: M1'' Gated-Dense Control + Honest Forget Test of KG Single-Absorber Suppression
summary: |-
  iter-7 M1'' decisively stress-tests the auditability-first two-track CCRG claim that ablating ONE KG-named absorber latent (KG-ABL) is a better unlearning handle than a dense baseline. It adds the FAIR control iter-6 lacked and an honest operating-point protocol.

  NEW OPERATOR (core.py): DENSE-SUB-ABL-GATED (kind='erase_dir_gated') erases the sub-context diff-of-means u_sub ONLY where |h.u_sub|>tau; tau is calibrated (calibrate_gate_tau) so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg. This removes the iter-6 confound (KG edits ~1-3% of tokens; ungated u_sub edits every token). tau threaded through make_edit_hook/forward_pos_logprobs/behavioral_curve/side_effects/generate_under_edit/last_tok_logprobs. FIVE operators at the SAME swept matched forget: NOOP, KG-ABL, DENSE-SUB-ABL-GATED (decisive), DENSE-SUB-ABL (ungated, iter-6, secondary), DENSE-WHOLE-ABL (secondary), +RAND +KG-ABL-UNIT (M7).

  HONEST OPERATING POINT: per case we report max_forget_{kg,sub,gated,whole} (KG's next-token-KL ceiling is 17-30x smaller than the dense directions'), NOOP-identical fraction (KG is NOOP-identical on ~0.89 of FORGET prompts for the country cases), full collateral-vs-forget curves, a gate footprint sweep {0.5,1,2,4}*f_kg, matched_target=0.8*min(max_kg,max_gated), and op_high=0.95*max_kg.

  MEANINGFUL-FORGET PROOF ($0, deterministic, the key addition): (a) completion-accuracy drop = drop in gold-token log-prob on hand probes (capital-of-Georgia->Tbilisi, large->L, etc) with bootstrap CI; (b) frozen 1-D-free sub-probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget[op] = (completion CI>0) OR (sub-probe positive-rate drop>=0.1). Decisive pair KG-ABL vs DENSE-SUB-ABL-GATED via paired_bootstrap_diff (B=10000) on the joint (retain-utility x fluency) outcome under TWO OpenRouter judges (claude-haiku-4.5 + gpt-4o-mini).

  PER-CASE 3-WAY FORK: KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET / GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE / NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. Aggregate requires absorption advantage to EXCEED co-firing advantage; a US-excluded gate counts only powered absorption cases.

  RESULTS (5 cases, 2109 judge calls, $0.80 << $3 target; overall=SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring=True, adv 1.58>0.37): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE: KG meaningfully forgets (sub-probe drop 0.42, completion 0.11) AND beats the footprint-matched gated dense by +1.58 joint under BOTH judges with strictly lower collateral (CI excl 0) and 1.0 curve dominance -- a discovered single SAE feature beats a labeled+footprint-matched dense control. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET: the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_kg 0.065/0.114, sub-probe drop 0.07/0.0); this directly EXPOSES that iter-6's KG_BEATS_USUB headline sat at a near-NOOP operating point (KG won by barely editing). (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED (+0.47) but co-firing, so excluded from the absorption gate. The month case was dropped because the iter-5 homograph month dataset's *_data_out.json artifacts were never materialized on disk; absorption set = {Georgia, large, Jordan}.

  OUTPUT (exp_gen_sol_out, validated full/mini/preview, 0.8MB): metadata.per_case (all operating points, gate tau sweep + footprint used, NOOP-identical, completion/sub-probe drops, meaningful_forget, collateral & joint CIs KG-vs-GATED decisive + KG-vs-SUB/WHOLE secondary + gated-vs-ungated, full-range collateral curves, M5/M6/M7, fork_verdict); metadata.summary (3-way fork counts, adv_absorption/adv_cofiring, absorption_exceeds_cofiring, us_excluded_gate, overall_verdict); 11 honest_negatives; datasets gated_dense_per_prompt (288 rows, predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-op judged utilities + NOOP-identical + model-internal signals) and kg_vs_gated_per_case (5 rows). For the paper: the honest, feature-dependent conclusion is that the single-SAE-absorber handle genuinely beats a fair dense control ONLY for concentrated features (spelling); for distributed taxonomic/co-firing senses it is clean low-collateral PARTIAL suppression, not meaningful unlearning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 3 ---
id: art_ZxVw0e4seBq3
type: experiment
title: Named-Entity Homograph SAE Absorption Screen + Gated-Dense Unlearning Downstream
summary: |-
  M2'' CONFIRMATORY (supporting, not load-bearing) experiment on Gemma-2-2b + Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.92, layer hidden_states[13]). It consumes the previously-unused named_entity_safety hierarchy (art_KNPsfjByyxiS) and reuses the iter-5/6 engine verbatim (core.py, method_iter6.py) with two genuinely-new pieces: a $0 absorption SCREEN (screen.py) and a NEW gated-dense edit operator 'erase_dir_gated' + a footprint-matched gate-calibration primitive (calibrate_gate) added to core.py.

  THESIS TESTED: feature absorption = LEXICAL HOMOGRAPHY (a suppressed 'named-entity/org' parent latent under a polysemous surface token), NOT safety/demographic semantics. A single coherent content-responsive parent latent (2768; xon-recall 0.99, probe AUC 1.0, not diffuse) was identified non-circularly (recall-only + >5% firing-floor). Per eligible entity the screen computes, with the absorber chosen on the diagnostic fit fold and every metric scored on the disjoint train fold: recall-hole, K-track-lite absorber, firing-Jaccard(parent,absorber), held-out precision, hole-coverage-gain with bootstrap CI, and a form-free decoder-probe-cosine oracle (Chanin/SAEBench, tau 0.025). 'absorption_structured' is gated on the firing-signature (the canonical iter-2..6 definition the Georgia positive control satisfies); the form-free decoder-projection oracle is reported separately and confirms 3/3 named-entity hits (it is spelling/concept-tuned and does not transfer to the taxonomic Georgia absorber, which would be wrongly rejected if it gated the verdict).

  PRIMARY RESULT ($0 screen): 3/5 eligible named-entity homographs are absorption-structured AND oracle-confirmed: Amazon (hole 0.61, jac 0.048, prec 0.99, gain 0.61 CI>0, dec-cos 0.12), Bush (0.79/0.021/1.00/0.79, 0.04), Cook (0.72/0.045/1.00/0.70, 0.03). Apple (hole 0.25) and King (0.42) are NOT structured (the parent detector fires on them). Four descriptive-only homographs (West, Bell, Hunt, Banks) show the relaxed signature (n<150). The Georgia self-check PASSED (the identical screen flags the canonical taxonomic absorber 16009 structured). This reinforces the settled iter-6 demographic null: absorption tracks lexical polysemy.

  CONDITIONAL DOWNSTREAM (supporting; both judges claude-haiku-4.5 + gpt-4o-mini, $0.35 total, 949 calls): at matched forget (0.8*min(maxKG,maxSUB)) with an edit-vs-NOOP forget delta, four operators KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED (footprint-matched gate, balanced-acc 0.95-0.97) / DENSE-WHOLE-ABL. Amazon = KG_BEATS_GATED_DENSE (non-trivial forget: median KL 0.58, 58% prompts changed; KG-vs-GATED joint CI [0.41,1.08] and 2nd-judge CI [0.35,0.68] both exclude 0; curve-dominance 1.0) -> a genuine NAMED_ENTITY_HOMOGRAPH_WIN. Bush = KG_MATCHES_GATED_DENSE (non-trivial forget, label-free parity). Georgia control = NEAR_NOOP_NO_WIN (KG cannot forget non-trivially at the matched point; the iter-5/6 Georgia 'win' was lower-collateral, not strong forgetting). Notably the named-entity absorber 6846 is a STRONGER edit handle (max_kg 1.14) than the country absorber (0.064).

  VERDICTS: overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND. 8 honest negatives recorded (confirmatory framing, oracle scope/decoder-tuning, Bush parity, Georgia NEAR_NOOP context, named-entity-vs-country edit-handle strength).

  DELIVERABLES: method.py (driver), screen.py (screen), core.py (engine + erase_dir_gated + calibrate_gate), method_iter6.py (reused engine). method_out.json (+ full/mini/preview, all PASS exp_gen_sol_out, <=208KB) holds metadata.{screen_table, breadth_count, georgia_sanity, parent_identification, downstream (per-case matched_target, max_forget_kg/sub/gated/whole, full_range_collateral_curve, edit_vs_noop_forget, gate_calibration, joint CIs KG-vs-{GATED,SUB,WHOLE} under both judges, curve_dominance), overall_verdict, secondary_tag, honest_negatives, llm_cost_usd}. Three datasets: named_entity_absorption_screen (19), downstream_edit_per_case (3), downstream_edit_per_prompt (90).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — evaluation metrics, agent orchestration patterns, benchmark design
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand prediction format. Evaluate ALL experiments provided — do not skip or select a subset. Avoid re-training or re-executing the method unless absolutely necessary; prefer loading predictions from each dependency's method_out.json / predict_* fields. Read domain handbook if applicable (see <available_domain_handbooks>). Decide evaluation metrics based on artifact plan. Test basic functionality with 'uv run'.
TODO 3. Fully implement evaluation as described in artifact plan in './eval.py'. Use exp_eval_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant metrics or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-18 10:51:12 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-json · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [4] SKILL-INPUT — aii-python · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [5] SKILL-INPUT — aii-file-size-limit · 2026-06-18 10:51:34 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [6] SYSTEM-USER prompt · 2026-06-18 11:11:10 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_evaluation_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_evaluation_1_idx3
type: evaluation
title: >-
  Iter-8 Integrity-Lock Eval: De-Inflate the Edit Headline, Lay Both Forget Instruments Side-by-Side, Show Concentration>Absorption
  Predicts the Win, and Lock the Georgia +0.561 Retraction
summary: >-
  Pure-CPU, $0, read-only re-analysis over the EXISTING iter-6/7 edit data (art_Cgk9ETiZfvtl, art_ZxVw0e4seBq3, art_3WXWsaSoGMnK).
  Following the project integrity-lock pattern (COMPUTE-from-source then COMPARE-to-stored, never overwrite), it produces
  GEN_PAPER_TEXT drop-in numbers that are robust to any truncation of the new iter-8 experiments: (1) the DE-INFLATED lead
  KG-vs-strongest-ungated-dense (+1.00 on 'large') reconciled against the inflated +1.58-vs-footprint-gated with its beta~2.97
  over-erasure stats; (2) BOTH meaningful-forget instruments (gold-completion-drop AND frozen sub-probe-drop) per case/operator
  side-by-side, with an instrument-disagreement metric proving next-token-KL matching != behavioral matching; (3) a per-case
  CONCENTRATION proxy correlated with the win/meaningful-forget outcome vs the absorption-regime label (concentration predicts,
  absorption does not); (4) the consolidated Georgia +0.561 RETRACTION (iter-6 win sat at a near-NOOP operating point); plus
  an operator-divergence flag (3%-global-footprint vs 95%-X-rate gate) the new experiments must unify. Emits eval_out.json
  (exp_eval_sol_out) with metrics_agg, per-case datasets, cross_checks, and cross-checked drop-in paper_wording.
runpod_compute_profile: cpu_heavy
metrics_descriptions: |-
  PURE-ANALYSIS INTEGRITY LOCK. No GPU, no model load, no LLM calls ($0). Read-only over three stored experiment outputs. EVERY headline value is RECOMPUTED from source columns, then COMPARED to the stored expectation; mismatches are reported in metadata.cross_checks with an explanatory note and NEVER overwritten (this mirrors art_w7p8du2N1f0Y / art_-k4Yg-l4NaNO). Use a fixed seed (1234) for every bootstrap so results are deterministic and re-checkable.

  === INPUTS (exact paths; load full_method_out.json, fall back to method_out.json if absent) ===
  - D1 = art_Cgk9ETiZfvtl @ /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1/full_method_out.json. Use metadata.per_case[*] (5 cases: target_subcontext in {Georgia, large, Jordan, United States, insult}), metadata.summary, datasets.gated_dense_per_prompt (288 rows; columns predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-operator judged utilities + NOOP-identical + model-internal signals), datasets.kg_vs_gated_per_case (5 rows). Also read this dir's method.py to extract the EXACT joint-utility formula, paired_bootstrap_diff, completion_drop, fit_sub_probe and calibrate_gate_tau definitions so recomputation is faithful.
  - D2 = art_ZxVw0e4seBq3 @ .../iter_7/gen_art/gen_art_experiment_2/full_method_out.json. Use metadata.downstream[*] (3 cases: Amazon, Bush, Georgia-control), datasets.downstream_edit_per_prompt (90 rows), datasets.downstream_edit_per_case, metadata.screen_table (per-entity absorber_precision/hole/jaccard for Amazon/Bush/Cook).
  - D3 = art_3WXWsaSoGMnK @ .../iter_6/gen_art/gen_art_experiment_1/full_method_out.json. Use the Georgia kg_vs_dense_per_case entry (joint_diff_CI_KG_vs_SUB, matched_target_forget_kl, fork_verdict) and datasets.unlearn_per_prompt for Georgia if a recompute is needed.

  === GROUP A - DE-INFLATION (M1''' + M3''' lead number) ===
  A1. Mean joint utility per operator per D1 case: recompute from gated_dense_per_prompt judged-utility columns using the exact joint formula read from method.py (joint = judged retain-utility combined with fluency). Cross-check computed kg/gated/sub_joint_utility_mean against stored metadata.per_case[*].{kg_joint_utility_mean, gated_joint_utility_mean, sub_joint_utility_mean}. Expected for large: KG=1.8704, GATED=0.2870, SUB=0.8704.
  A2. Paired-bootstrap (B=10000, seed 1234, over preservation prompts) joint diffs per case: (i) DE-INFLATED LEAD = KG-ABL minus DENSE-SUB-ABL (ungated, strongest dense); (ii) INFLATED = KG-ABL minus DENSE-SUB-ABL-GATED. Cross-check (i) against stored joint_diff_CI_KG_vs_SUB_secondary and (ii) against joint_diff_CI_KG_vs_GATED. Expected for large: lead = +1.000 CI[0.787,1.213] (n=36); inflated = +1.583 CI[1.361,1.787]. Verify the reconciliation 1.8704-0.8704=+1.00 and 1.8704-0.2870=+1.58 hold to <1e-3.
  A3. Over-erasure stats for large (and report for all cases): gated retain-collateral KL = retain_collateral_kl_gated_mean (0.290) vs ungated SUB retain_collateral_kl_sub_mean (0.021) -> over_erasure_ratio = 0.290/0.021 ~= 13.8x; the beta the gate was driven to = scale_gated_beta (2.967) vs scale_sub_beta (0.649); gated_vs_ungated_collateral_CI (diff -0.269, excl_0 true => gated has MORE collateral than its OWN ungated form). Also report collateral_diff_CI_KG_vs_GATED (+0.290) and collateral_diff_CI_KG_vs_SUB_secondary (+0.021).
  A4. Emit per-case de-inflation rows {case, kg/gated/sub joint means, lead_diff+CI, inflated_diff+CI, gated_collateral, sub_collateral, over_erasure_ratio, scale_gated_beta, scale_sub_beta, gated_vs_ungated_collateral_excl_0}. metrics_agg gets de_inflated_lead_large=+1.00 (with CI), inflated_gap_large=+1.58 (with CI), over_erasure_ratio_large~=13.8.

  === GROUP B - BOTH FORGET INSTRUMENTS SIDE-BY-SIDE (M4''') ===
  B1. For every D1 case x operator at the matched point, tabulate the TWO behavioral instruments: (a) gold-completion-drop = metadata.per_case[*].completion_drop_matched[op].drop_vs_noop with drop_ci/excl_0; (b) frozen sub-probe positive-rate drop = subprobe_drop[op].drop (and NOOP pos_rate, auc). Build one row per (case, operator) with both numbers + their CI/excl_0.
  B2. Instrument-disagreement metric, per case, on the decisive KG-vs-GATED contrast: completion_contrast = completion_drop[KG]-completion_drop[GATED]; subprobe_contrast = subprobe_drop[KG]-subprobe_drop[GATED]. Report sign_divergence = (sign(completion_contrast) != sign(subprobe_contrast)) and the signed magnitudes. For large this fires: completion favors GATED (KG 0.072 vs GATED 1.080 => completion_contrast=-1.008) while sub-probe favors KG (KG 0.417 vs GATED 0.0 => subprobe_contrast=+0.417) -> sign_divergence=TRUE. Also compute, per case, a rank-disagreement (Spearman or Kendall-tau between the two instruments' operator orderings over {KG,GATED,SUB}).
  B3. Quantify 'next-token-KL matching != behavioral matching': all operators are scaled to the SAME matched_target next-token KL, yet at that point completion_drop and subprobe_drop differ sharply across operators (e.g. large: KL-matched but completion_drop spans 0.072..1.080 and subprobe_drop spans 0.0..0.917). Report, per case, the across-operator spread (max-min) of each behavioral instrument at the KL-matched point as the divergence evidence, and recommend (for paper_wording) matching operators on a BEHAVIORAL measure (sub-probe drop or completion accuracy) rather than next-token KL. Flag that the load-bearing large completion CI is over only n=4 probes (RIGOR caveat) -- read drop_ci.n.
  B4. metrics_agg gets instrument_disagreement_cases (list of cases with sign_divergence=TRUE; expect {large}), and the large KG-vs-GATED contrast pair (-1.008 completion, +0.417 sub-probe).

  === GROUP C - CONCENTRATION-vs-ABSORPTION PREDICTOR (M3''' decisive descriptive) ===
  C1. Assemble a pooled case table across D1 (large, Georgia, Jordan, United States, insult) and D2 (Amazon, Bush). For each case read: absorber_precision (per-sub-context precision), gate_footprint_used / gate_target_footprint (firing footprint f_kg), firing_jaccard_with_parent, max_forget_kg (single-latent next-token-KL ceiling = edit leverage), regime label ('absorption' vs 'co-firing'), and outcomes: win_binary = (fork_verdict==KG_BEATS_GATED_DENSE...), meaningful_forget_binary = kg_can_forget (D1) / non-trivial-forget (D2), adv_continuous = joint KG-vs-GATED diff. For D2 use downstream[*] fields (gate_calibration, max_forget_kg, fork_verdict, joint_diff_CI_KG_vs_GATED) and screen_table absorber_precision.
  C2. CONCENTRATION PROXY (primary): concentration = absorber_precision * (1 / f_kg) read from stored fields (per the direction: per-sub-context precision x inverse footprint). ALSO compute two robustness variants and report all three: (v2) absorber_precision * max_forget_kg (precision x single-latent leverage), (v3) absorber_precision * (1 - firing_jaccard_with_parent) * sub_probe_max_drop. Rank/z-score each case under each proxy. The qualitative pattern to confirm: concentrated cases (large prec 1.0, Amazon prec 0.99/max_kg 1.14, insult high-precision co-firing) WIN; distributed cases (Georgia/Jordan country sense, US co-firing) LOSE -- crossing BOTH regime labels.
  C3. PREDICTIVE COMPARISON: compute point-biserial (proxy continuous vs binary outcome) and Spearman (proxy vs adv_continuous) for (a) each concentration proxy and (b) the absorption-regime binary label, each with a bootstrap CI (B=10000, seed 1234, resampling cases). predictive_delta = corr(concentration_proxy, outcome) - corr(absorption_label, outcome). EXPECT concentration to track win/meaningful_forget better than the absorption label (absorption label is near-uninformative because wins/losses cross it). Because n is small (~7 cases) this is EXPLICITLY descriptive: report the delta + CI but label it 'descriptive, small-n' in the row and in paper_wording. Cross-check the absorption-mean-vs-cofiring-mean comparison the paper currently leans on: adv_absorption_mean (1.583) vs adv_cofiring_mean (0.372) from metadata.summary, and note it is a 1-case-vs-2-case-mean (thin/circular) basis -- the per-case concentration correlation supersedes it.
  C4. metrics_agg gets concentration_vs_absorption_predictive_delta (primary proxy, with CI), the per-proxy correlations, and a boolean concentration_outpredicts_absorption.

  === GROUP D - GEORGIA +0.561 RETRACTION (M1''' carry / M6) ===
  D1. From D3 recompute (or read+cross-check) the iter-6 Georgia KG-vs-SUB joint = +0.5606 CI[0.318,0.811] n=44 at matched_target_forget_kl=0.0517. If recomputing from unlearn_per_prompt, use the method.py joint formula; else cross-check the stored CI.
  D2. From D1 (iter-7) read the near-NOOP evidence at/near that operating point for Georgia: max_forget_kg=0.0647 (17-30x smaller than dense ceilings), noop_identical_fraction.FORGET['KG-ABL']=0.889, subprobe_drop['KG-ABL'].drop=0.075, completion_drop_matched['KG-ABL'].drop_ci.excl_0=false, fork_verdict=NO_MEANINGFUL_FORGET, and the iter-7 KG-vs-GATED Georgia adv=+0.174 / KG-vs-SUB=+0.197 (vacuous, KG barely edits).
  D3. RETRACTION ROW + STATEMENT: the iter-6 +0.561 'win' sat at a near-NOOP operating point (KG won by barely editing, and also barely forgot); it is retracted/recontextualized as clean low-collateral PARTIAL suppression, not meaningful unlearning. metrics_agg gets retraction_iter6_georgia_adv=+0.561, retraction_iter6_matched_kl=0.0517, retraction_iter7_max_forget_kg=0.0647, retraction_noop_identical=0.889, retraction_subprobe_drop=0.075, retraction_status='RETRACTED_NEAR_NOOP'.

  === GROUP E - OPERATOR-DEFINITION DIVERGENCE FLAG (MINOR 4 / M1''' unify) ===
  E1. Cross-check the two 'footprint-matched gated dense' operators are NOT identical: D1 = global-neutral-pool footprint gate (calibrate_gate_tau; gate_tau~=101, gate_footprint_used~=0.025-0.028, gate_target_footprint~=0.014-0.03, ~3% global firing). D2 = gate_calibration.method=='footprint_match_clamped' on X-POSITIVE firing rate clamped ~0.95 (gate_fire_rate_X~=0.9467, gate_fire_rate_sibling~=0.045). Set metrics_agg.operator_divergence_flag=TRUE with both calibration descriptors and a note that the iter-7 headline aggregates a 3%-global-footprint comparison (large) with a 95%-X-rate comparison (Amazon); the new iter-8 experiments must unify into ONE gate operator (or document any per-case clamp in-table).

  === OUTPUT (eval_out.json, schema exp_eval_sol_out; validate full/mini/preview <100MB via aii-json + aii-file-size-limit) ===
  - metrics_agg: {de_inflated_lead_large, inflated_gap_large, over_erasure_ratio_large, instrument_disagreement_cases, large_kg_vs_gated_completion_contrast, large_kg_vs_gated_subprobe_contrast, concentration_vs_absorption_predictive_delta, concentration_outpredicts_absorption, retraction_* fields, operator_divergence_flag, absorption_mean_vs_cofiring_mean_basis_note}.
  - datasets: de_inflation_per_case (>=5 D1 rows + D2 rows), both_instrument_per_case_op (one row per case x {KG,GATED,SUB} with completion_drop+CI and subprobe_drop), concentration_predictor_per_case (~7 rows with proxies+outcomes+labels), retraction_per_case (Georgia row), operator_divergence (2 rows). Each dataset row must carry predict_* / value STRING fields if the project schema requires non-null string predictions (mirror the iter-5/6 validator gotcha: every example needs a predict_* string).
  - metadata.cross_checks: array of {name, computed, stored, abs_diff, rel_diff, match (bool at tol: 1e-3 for point stats; CI-overlap for bootstrap), note}. Include at minimum the A1 utility means, A2 lead/inflated diffs+CIs, D1/D2 collateral CIs, the iter-6 Georgia +0.561, and the summary adv_absorption/adv_cofiring means.
  - metadata.paper_wording: drop-in strings (cross-checked) for: (W1) de-inflated lead '+1.00 vs the strongest ungated dense on large (CI[0.79,1.21]), with +1.58 vs a footprint-matched gate reported only as a robustness check handicapped by beta~3 over-erasure (gated collateral 0.29 = 13.8x its own ungated 0.021)'; (W2) instrument disagreement 'at the next-token-KL-matched point the two forget instruments disagree in sign for large (completion favors the gated dense by 1.01, frozen sub-probe favors KG by 0.42), so KL-matching does not equalize behavioral forgetting; operators should be matched on a behavioral measure'; (W3) concentration finding 'the edit-win predictor is latent concentration/precision, not absorption: wins span an absorption case (large) and a co-firing case (insult), losses are distributed senses (Georgia/Jordan); a precision-x-inverse-footprint proxy tracks the outcome where the absorption-regime label does not (descriptive, n~7)'; (W4) retraction 'the iter-6 Georgia +0.561 win sat at a near-NOOP operating point (max single-latent forget KL 0.065, NOOP-identical on 89% of forget prompts, frozen sub-probe drop 0.075); it is retracted as low-collateral partial suppression, not meaningful unlearning'; (W5) operator unification note.

  === FAILURE / EDGE HANDLING ===
  - If a per-prompt judged-utility column is missing or the joint formula cannot be reproduced exactly, fall back to cross-checking the stored *_joint_utility_mean and *_diff_CI directly and mark the cross_check note 'stored-only (recompute unavailable)'; do not fabricate.
  - If a recomputed bootstrap CI does not overlap the stored CI, record match=false with a note (seeding/resample-unit difference) -- report, never overwrite.
  - Some D1 cases (insult, US) are regime='co-firing'; keep them in Group C (they are load-bearing for the concentration claim) but exclude US/insult from any absorption-only aggregate, matching metadata.summary.us_excluded_gate.
  - D2 Amazon/Bush use the 95%-X-rate gate, so their joint diffs are NOT directly comparable to D1's 3%-global-footprint diffs; carry them as supporting concentration points flagged with the operator note (Group E), not pooled into the D1 lead CI.
  - Keep all three output variants <100MB; per-prompt source datasets are tiny (288/90/~hundreds rows) so full retention is fine.
metrics_justification: >-
  These metrics are exactly the four reviewer-gating integrity issues (R1 de-inflation, R3 concentration-not-absorption, R4
  operator divergence, R5 instrument rigor) reduced to arithmetic over data that ALREADY exists, so GEN_PAPER_TEXT gets defensible
  drop-in numbers no matter how the new iter-8 edit experiments turn out. (1) The DE-INFLATED lead matters because the abstract
  currently leads with the largest, least-defensible gap: the +1.58 is KG beating a gated dense that was driven to beta~2.97
  over-erasure (its own collateral 0.29 is 13.8x its ungated 0.021), i.e. a handicapped control. Recomputing KG-minus-strongest-ungated-dense
  (+1.00, CI[0.79,1.21]) from the stored per-prompt utilities, and proving the +1.58/+1.00 reconciliation against the stored
  utility means, gives the paper an honest headline and pre-empts the #1 blocker. (2) Laying BOTH forget instruments side-by-side
  and quantifying their sign-disagreement at the KL-matched point is the only way to honestly support 'meaningful forget':
  the completion-drop and sub-probe-drop instruments rank KG vs the gated dense in OPPOSITE directions for the load-bearing
  large case, which both proves the forget is real on the behavioral sub-probe AND shows that matching on next-token KL does
  not equalize behavior -- a rigor fix the paper must state, not hide. (3) The concentration-vs-absorption predictor is the
  decisive evidence reframe: the wins cross both regime labels (absorption 'large' wins, co-firing 'insult' wins; absorption
  'Georgia/Jordan' lose), so a per-case precision-x-inverse-footprint proxy correlating with the outcome better than the absorption-regime
  label directly substantiates 'the win traces to concentration, not the absorption structure the method discovers' and retires
  the thin 1-vs-2-case absorption_exceeds_cofiring aggregate. It is correctly scoped as small-n descriptive. (4) Consolidating
  the Georgia +0.561 retraction closes the loop on a now-known-misleading prior headline by showing, in one row, that the
  win sat at a near-NOOP operating point (tiny max forget KL, 89% NOOP-identical, sub-probe barely moved) -- protecting the
  paper's integrity. The operator-divergence flag surfaces the 3%-global-footprint vs 95%-X-rate inconsistency the new experiments
  must unify. Because the whole artifact is a read-only, $0, deterministic recompute-and-cross-check, it is immediately runnable
  and fully robust to truncation of the expensive new GPU experiments, which is precisely its strategic value as the always-produced
  clean deliverable.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_3WXWsaSoGMnK
type: experiment
title: 'M1'': KG single-absorber unlearning vs a sub-context-targeted dense baseline'
summary: >-
  M1' replaces the near-tautological WHOLE-PARENT dense comparator of iter-5 with a STRONGER, sub-context-targeted dense baseline
  u_sub = diff-of-means(target-sub-context-positive, sibling-positive in the same parent context), fit on a DISJOINT fold
  from the per-sub-context labels the testbeds carry. The decisive downstream test is selective sub-concept UNLEARNING: at
  MATCHED forget-quality (next-token KL on held-out FORGET windows, matched_target = 0.8*min(maxKG,maxSUB)), it compares KG-ABL
  (ablate one KG-named absorber, h -= lambda*z_l*W_dec[l], gated by the latent's own sparse firing) against the DECISIVE DENSE-SUB-ABL
  (erase u_sub) and a clearly-labeled SECONDARY DENSE-WHOLE-ABL (erase the whole-parent diff-of-means), plus RAND and (M7)
  KG-ABL-UNIT. The joint (retain-utility x fluency) outcome is scored by an AxBench-style OpenRouter judge (anthropic/claude-haiku-4.5)
  with paired-bootstrap KG-vs-SUB CIs (B=10000), curve-dominance, and model-internal corroboration (continuation PPL + retain
  next-token KL). Per-case FORK verdict: KG_BEATS_USUB (joint CI excl 0 favoring KG AND a 2nd-family judge CI also excl 0),
  KG_MATCHES_USUB_LABEL_FREE (CI includes 0 - KG matches u_sub WITHOUT needing the labels), or KG_LOSES_TO_USUB. RESULTS (full
  run, both judges, $0.53/1459 calls): GATE PASSED. The two ABSORPTION cases are both KG_BEATS_USUB - taxonomic Georgia(16009)
  and first_letter large(8463) - each with u_sub localizing better than whole-parent and the M7 win tracing to the SINGLE
  discovered absorber (the multi-member K-track unit only adds collateral); human-proxy spot-checks pass. Folded-in modules:
  (M1') u_sub localization validation is CURVE-BASED over the achievable dense forget range (the KG-pinned matched point is
  tiny because KG single-latent next-token KL has a small ceiling, so a single-point check is mis-specified) - this DELETES
  the false 'a single dense hyperplane cannot localize' framing and reframes KG's edge as sparse-firing GATING (token footprint
  -> 0 for absorption), NOT the dense direction failing to localize; (M5) United States(846) is a ROUTER FALSE-NEGATIVE reclassified
  to co-firing - its absorber footprint is low/surgical-looking but the small parent recall-hole (0.197) flags co-firing,
  so it is moved out of the absorption gate; (M6) a second different-family judge (openai/gpt-4o-mini) with Cohen kappa +
  Pearson/Spearman utility correlation keeps a KG win only if its CI also excludes 0, plus a deterministic $0 human-proxy
  check that KG-ABL preserves sibling tokens while DENSE-WHOLE corrupts them; (M7) unit-vs-single ablation. Toxicity_insult
  is the co-firing case where KG is NOT surgical (footprint 0.166, firing-Jaccard 0.882, no recall-hole - the regime mechanism
  holds); it registers KG_BEATS_USUB on the LLM-judge joint but the $0 model-internal joint does NOT corroborate it (CI includes
  0) and u_sub itself fails to localize in co-firing, so it is reported as a weak judge-only edge, not a surgical win, and
  is not counted toward the gate. A per-case mi_corroborates_fork flag is reported (Georgia/US True; large/toxicity False
  - the noisier model-internal proxy is inconclusive there even though both LLM judges agree). Reuses the iter-4/iter-5 Gemma-Scope
  L12/16k JumpReLU engine via core.py (only the multi-latent abl_latent generalization for M7 + WORK repoint). Single GPU
  (NVIDIA L4); $0 model-internal, <$2 LLM judges (hard cap $10). All outputs validate against exp_gen_sol_out: unlearn_per_prompt
  (per (case,role,prompt) with predict_kg_abl / predict_dense_sub_abl / predict_dense_whole_abl / predict_rand / predict_noop
  continuations + both judges' utilities) and kg_vs_dense_per_case (fork verdicts + all decisive CIs).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_6/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 2 ---
id: art_Cgk9ETiZfvtl
type: experiment
title: M1'' Gated-Dense Control + Honest Forget Test of KG Single-Absorber Suppression
summary: |-
  iter-7 M1'' decisively stress-tests the auditability-first two-track CCRG claim that ablating ONE KG-named absorber latent (KG-ABL) is a better unlearning handle than a dense baseline. It adds the FAIR control iter-6 lacked and an honest operating-point protocol.

  NEW OPERATOR (core.py): DENSE-SUB-ABL-GATED (kind='erase_dir_gated') erases the sub-context diff-of-means u_sub ONLY where |h.u_sub|>tau; tau is calibrated (calibrate_gate_tau) so the gate's global firing fraction over a neutral pool equals the KG absorber's token footprint f_kg. This removes the iter-6 confound (KG edits ~1-3% of tokens; ungated u_sub edits every token). tau threaded through make_edit_hook/forward_pos_logprobs/behavioral_curve/side_effects/generate_under_edit/last_tok_logprobs. FIVE operators at the SAME swept matched forget: NOOP, KG-ABL, DENSE-SUB-ABL-GATED (decisive), DENSE-SUB-ABL (ungated, iter-6, secondary), DENSE-WHOLE-ABL (secondary), +RAND +KG-ABL-UNIT (M7).

  HONEST OPERATING POINT: per case we report max_forget_{kg,sub,gated,whole} (KG's next-token-KL ceiling is 17-30x smaller than the dense directions'), NOOP-identical fraction (KG is NOOP-identical on ~0.89 of FORGET prompts for the country cases), full collateral-vs-forget curves, a gate footprint sweep {0.5,1,2,4}*f_kg, matched_target=0.8*min(max_kg,max_gated), and op_high=0.95*max_kg.

  MEANINGFUL-FORGET PROOF ($0, deterministic, the key addition): (a) completion-accuracy drop = drop in gold-token log-prob on hand probes (capital-of-Georgia->Tbilisi, large->L, etc) with bootstrap CI; (b) frozen 1-D-free sub-probe d_sub (AUC~1.0) scored on the REAL post-edit residual via read_resid_under_edit; meaningful_forget[op] = (completion CI>0) OR (sub-probe positive-rate drop>=0.1). Decisive pair KG-ABL vs DENSE-SUB-ABL-GATED via paired_bootstrap_diff (B=10000) on the joint (retain-utility x fluency) outcome under TWO OpenRouter judges (claude-haiku-4.5 + gpt-4o-mini).

  PER-CASE 3-WAY FORK: KG_BEATS_GATED_DENSE_AT_MEANINGFUL_FORGET / GATED_DENSE_CLOSES_GAP_DISCOVERY_IS_THE_VALUE / NO_MEANINGFUL_FORGET_SCOPE_TO_PARTIAL_SUPPRESSION. Aggregate requires absorption advantage to EXCEED co-firing advantage; a US-excluded gate counts only powered absorption cases.

  RESULTS (5 cases, 2109 judge calls, $0.80 << $3 target; overall=SPARSE_SAE_HANDLE_ESTABLISHED, absorption_exceeds_cofiring=True, adv 1.58>0.37): (1) first_letter_large (spelling absorber 8463) = KG_BEATS_GATED_DENSE: KG meaningfully forgets (sub-probe drop 0.42, completion 0.11) AND beats the footprint-matched gated dense by +1.58 joint under BOTH judges with strictly lower collateral (CI excl 0) and 1.0 curve dominance -- a discovered single SAE feature beats a labeled+footprint-matched dense control. (2) taxonomic_georgia (16009) and taxonomic_jordan (540) = NO_MEANINGFUL_FORGET: the single-latent ablation CANNOT remove the DISTRIBUTED country sense even at full strength (max_kg 0.065/0.114, sub-probe drop 0.07/0.0); this directly EXPOSES that iter-6's KG_BEATS_USUB headline sat at a near-NOOP operating point (KG won by barely editing). (3) taxonomic_us (846) = NO_MEANINGFUL (co-firing). (4) toxicity_insult (13367) = KG_BEATS_GATED (+0.47) but co-firing, so excluded from the absorption gate. The month case was dropped because the iter-5 homograph month dataset's *_data_out.json artifacts were never materialized on disk; absorption set = {Georgia, large, Jordan}.

  OUTPUT (exp_gen_sol_out, validated full/mini/preview, 0.8MB): metadata.per_case (all operating points, gate tau sweep + footprint used, NOOP-identical, completion/sub-probe drops, meaningful_forget, collateral & joint CIs KG-vs-GATED decisive + KG-vs-SUB/WHOLE secondary + gated-vs-ungated, full-range collateral curves, M5/M6/M7, fork_verdict); metadata.summary (3-way fork counts, adv_absorption/adv_cofiring, absorption_exceeds_cofiring, us_excluded_gate, overall_verdict); 11 honest_negatives; datasets gated_dense_per_prompt (288 rows, predict_kg_abl/predict_dense_sub_gated/predict_dense_sub_abl/predict_dense_whole_abl/predict_noop + per-op judged utilities + NOOP-identical + model-internal signals) and kg_vs_gated_per_case (5 rows). For the paper: the honest, feature-dependent conclusion is that the single-SAE-absorber handle genuinely beats a fair dense control ONLY for concentrated features (spelling); for distributed taxonomic/co-firing senses it is clean low-collateral PARTIAL suppression, not meaningful unlearning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_1
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Dependency 3 ---
id: art_ZxVw0e4seBq3
type: experiment
title: Named-Entity Homograph SAE Absorption Screen + Gated-Dense Unlearning Downstream
summary: |-
  M2'' CONFIRMATORY (supporting, not load-bearing) experiment on Gemma-2-2b + Gemma-Scope L12/16k JumpReLU SAE (gating cosine 0.92, layer hidden_states[13]). It consumes the previously-unused named_entity_safety hierarchy (art_KNPsfjByyxiS) and reuses the iter-5/6 engine verbatim (core.py, method_iter6.py) with two genuinely-new pieces: a $0 absorption SCREEN (screen.py) and a NEW gated-dense edit operator 'erase_dir_gated' + a footprint-matched gate-calibration primitive (calibrate_gate) added to core.py.

  THESIS TESTED: feature absorption = LEXICAL HOMOGRAPHY (a suppressed 'named-entity/org' parent latent under a polysemous surface token), NOT safety/demographic semantics. A single coherent content-responsive parent latent (2768; xon-recall 0.99, probe AUC 1.0, not diffuse) was identified non-circularly (recall-only + >5% firing-floor). Per eligible entity the screen computes, with the absorber chosen on the diagnostic fit fold and every metric scored on the disjoint train fold: recall-hole, K-track-lite absorber, firing-Jaccard(parent,absorber), held-out precision, hole-coverage-gain with bootstrap CI, and a form-free decoder-probe-cosine oracle (Chanin/SAEBench, tau 0.025). 'absorption_structured' is gated on the firing-signature (the canonical iter-2..6 definition the Georgia positive control satisfies); the form-free decoder-projection oracle is reported separately and confirms 3/3 named-entity hits (it is spelling/concept-tuned and does not transfer to the taxonomic Georgia absorber, which would be wrongly rejected if it gated the verdict).

  PRIMARY RESULT ($0 screen): 3/5 eligible named-entity homographs are absorption-structured AND oracle-confirmed: Amazon (hole 0.61, jac 0.048, prec 0.99, gain 0.61 CI>0, dec-cos 0.12), Bush (0.79/0.021/1.00/0.79, 0.04), Cook (0.72/0.045/1.00/0.70, 0.03). Apple (hole 0.25) and King (0.42) are NOT structured (the parent detector fires on them). Four descriptive-only homographs (West, Bell, Hunt, Banks) show the relaxed signature (n<150). The Georgia self-check PASSED (the identical screen flags the canonical taxonomic absorber 16009 structured). This reinforces the settled iter-6 demographic null: absorption tracks lexical polysemy.

  CONDITIONAL DOWNSTREAM (supporting; both judges claude-haiku-4.5 + gpt-4o-mini, $0.35 total, 949 calls): at matched forget (0.8*min(maxKG,maxSUB)) with an edit-vs-NOOP forget delta, four operators KG-ABL / DENSE-SUB-ABL / DENSE-SUB-ABL-GATED (footprint-matched gate, balanced-acc 0.95-0.97) / DENSE-WHOLE-ABL. Amazon = KG_BEATS_GATED_DENSE (non-trivial forget: median KL 0.58, 58% prompts changed; KG-vs-GATED joint CI [0.41,1.08] and 2nd-judge CI [0.35,0.68] both exclude 0; curve-dominance 1.0) -> a genuine NAMED_ENTITY_HOMOGRAPH_WIN. Bush = KG_MATCHES_GATED_DENSE (non-trivial forget, label-free parity). Georgia control = NEAR_NOOP_NO_WIN (KG cannot forget non-trivially at the matched point; the iter-5/6 Georgia 'win' was lower-collateral, not strong forgetting). Notably the named-entity absorber 6846 is a STRONGER edit handle (max_kg 1.14) than the country absorber (0.064).

  VERDICTS: overall_verdict = SAFETY_ABSORPTION_HOMOGRAPH_CONFINED (demographic null unchanged); secondary_tag = NAMED_ENTITY_HOMOGRAPH_WIN_FOUND. 8 honest negatives recorded (confirmatory framing, oracle scope/decoder-tuning, Bush parity, Georgia NEAR_NOOP context, named-entity-vs-country edit-handle strength).

  DELIVERABLES: method.py (driver), screen.py (screen), core.py (engine + erase_dir_gated + calibrate_gate), method_iter6.py (reused engine). method_out.json (+ full/mini/preview, all PASS exp_gen_sol_out, <=208KB) holds metadata.{screen_table, breadth_count, georgia_sanity, parent_identification, downstream (per-case matched_target, max_forget_kg/sub/gated/whole, full_range_collateral_curve, edit_vs_noop_forget, gate_calibration, joint CIs KG-vs-{GATED,SUB,WHOLE} under both judges, curve_dominance), overall_verdict, secondary_tag, honest_negatives, llm_cost_usd}. Three datasets: named_entity_absorption_screen (19), downstream_edit_per_case (3), downstream_edit_per_prompt (90).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_7/gen_art/gen_art_experiment_2
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — evaluation metrics, agent orchestration patterns, benchmark design
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input eval_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to eval_out.json and full_eval_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "EvaluationExpectedFiles": {
      "description": "All expected output files from evaluation artifact.",
      "properties": {
        "script": {
          "description": "Path to eval.py script. Example: 'eval.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full evaluation JSON file. Example: 'full_eval_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini evaluation JSON file. Example: 'mini_eval_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview evaluation JSON file. Example: 'preview_eval_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "EvaluationExpectedFiles",
      "type": "object"
    }
  },
  "description": "Evaluation artifact \u2014 structured output + file metadata.\n\nEvaluates both proposed and baseline methods with appropriate metrics.\nProduces eval.py and eval_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/EvaluationExpectedFiles",
      "description": "All output files you created. Must include eval.py script plus full/mini/preview evaluation JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "EvaluationArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [7] SYSTEM-USER prompt · 2026-06-18 11:12:32 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Iter-8 Integrity-Lock Eval: De-Inflated Edit Lead, Dual Forget Instruments, Concentration>Absorption, Georgia Retraction' is too long (at most 90 characters, got 120)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

## Task: `gen_art_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 10:51:16 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-18 10:51:16 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [3] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 10:51:46 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-18 10:51:46 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [5] SYSTEM-USER prompt · 2026-06-18 19:59:22 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>
YOUR PREVIOUS EXECUTION ATTEMPT CATASTROPHICALLY FAILED.
The entire worker container crashed after 765s.
Error: Pod launch failed — no instance booted (tried 4, 11 still out of stock): Container did not start within 240s on 8zu2qu2axkdeih (container_running=false, uptime=0, host_id=8zu2qu2axkdeih-64411ae3)

This was NOT a normal code error — the entire container died. Study the error
and last messages above carefully. Identify what caused the crash and be
EXTREMELY careful to avoid repeating it. Do NOT use the same approach.
</CRITICAL_WARNING__PREVIOUS_ATTEMPT_CRASHED>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [6] HUMAN-USER prompt · 2026-06-18 19:59:22 UTC

```
### Goal

Develop a new clustering-based method for organising sparse autoencoder (SAE) activations from large language models into more reliable units of analysis than individual latents.

### Reviewer Scope

Limit the technical core to areas the reviewer can deeply evaluate. Other fields are welcome for inspiration but should not host the substantive contribution.

Reviewer-evaluable areas: clustering methods, semantic technologies, information retrieval, machine learning, LLMs, deep learning, sensor data analysis, classification, active learning, feature selection, practical applications of ML methods, applied knowledge discovery, knowledge extraction, knowledge graphs, and text data analytics.

Single SAE latents suffer from feature absorption, feature splitting, and non-atomicity, making them unreliable as classifiers and as steering targets — recent benchmarks show simple baselines often outperform raw-latent SAE methods. Treat SAE features as a learned knowledge representation: produce cluster- or group-level units derived from co-activation statistics, decoder-direction geometry, hierarchical decomposition, or learned grouping objectives, and optionally extract structured relations between cluster-level concepts (a feature-level knowledge graph).

Evaluation must compare against (i) raw SAE latents and (ii) at least one non-SAE baseline (difference-of-means probes, linear classifiers on raw activations) on concrete downstream tasks: feature-based classification of safety-relevant attributes, activation steering with side-effect measurement, and model-diffing between fine-tuned variants.

Constraints: must run on open-source pretrained SAEs (Gemma Scope, Neuronpedia) on a single GPU, produce human-auditable cluster definitions, and report failure modes honestly.

### Publication

Target ICLR primary, ICML fallback.

### Things to Avoid

Theoretical results in computational learning theory (generalisation bounds, sample complexity, convergence proofs). The contribution must be a method or empirical finding, not a theorem.
```

### [7] SKILL-INPUT — aii-json · 2026-06-18 20:18:27 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [8] SYSTEM-USER prompt · 2026-06-18 20:22:37 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_8/gen_art/gen_art_experiment_2/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_2_idx2
type: experiment
title: >-
  Base-Widener + Concentration-vs-Absorption Population Test (iter-8 M2''' + M3''')
summary: >-
  Screen a WIDER vocabulary of candidate tokens (first-letter spelling word-absorbers L/O/T/I/D + homograph entities/given-names/brands/months)
  for lexical CONCENTRATION (per-sub-context firing precision x sparse footprint), independent of absorption structure, then
  run the IDENTICAL unified fair-gated edit (the new DENSE-SUB-ABL-GATED-FAIR = u_sub gated by the precise d_sub detector
  with bounded beta<=1) on the most-concentrated candidates. Report (1) how many candidates clear the fair-control bar at
  MEANINGFUL forget => additional independent concentrated wins beyond large/Amazon (verdict BASE_REACHES_4_PLUS vs BASE_STAYS_THIN_RETARGET);
  (2) whether a candidate's continuous CONCENTRATION score predicts its edit-win/meaningful-forget outcome better than its
  binary ABSORPTION-regime label (the decisive M3''' population evidence); (3) per candidate, whether the precision-selected
  absorber EQUALS the unconstrained max-precision latent (set-cover inertness, M5'''). Reuses iter-7 core.py/method.py VERBATIM
  for the SAE pipeline, edit operators, judges, u_sub/d_sub, and meaningful-forget proof; adds ONE new operator, a $0 concentration
  screen, a budget-bounded edit loop, and the population correlation. Compute: GPU (gemma-2-2b + Gemma-Scope L12/16k). LLM
  judge target <$3, hard cap $10.
runpod_compute_profile: gpu
implementation_pseudocode: |
  ############################################################################
  # WORKSPACE: 3_invention_loop/iter_8/gen_art/gen_art_experiment_2  (executor's CWD)
  # READ-ONLY INPUTS (existing run-tree artifacts, accessed by absolute path):
  #   CORE7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/core.py     (SAE+edit machinery)
  #   METH7 = 3_invention_loop/iter_7/gen_art/gen_art_experiment_1/method.py   (u_sub/d_sub/judge/forget proof)
  #   KG4   = 3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method_out.json (named absorbers)
  #   D1    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first-letter spelling; art_dpYpjSn2Xvg3)
  #   D2    = 3_invention_loop/iter_1/gen_art/gen_art_dataset_2/full_data_out.json (taxonomic+numeric; for distributed-absorption population anchors Georgia/Jordan)
  #   HG_DIR= 3_invention_loop/iter_5/gen_art/gen_art_dataset_1                  (homograph entities; art_2xQn686KUmV5)
  #   DOSS  = 3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json (SAE pins + baseline specs; art_RidEJtBC7gPT)
  # SAE pins (from core.py / dossier, DO NOT change): release google/gemma-scope-2b-pt-res,
  #   layer_12/width_16k/average_l0_82/params.npz, d_model 2304, hook blocks.12.hook_resid_post,
  #   model google/gemma-2-2b (mirror unsloth/gemma-2-2b), SEED 1234, B_BOOT 10000.
  ############################################################################

  # ============================ STEP A. ENV + REUSE (verbatim copy, not cross-dir import) ===========
  # Cross-dir import is unsafe because CORE7/METH7 hardcode WORK=iter_7 and create RESULTS/CACHE/LOGS there.
  #  - `uv init`; install: torch (CUDA cu124: `uv pip install torch --index-strategy unsafe-best-match`,
  #    add `--link-mode=copy` because the venv lives on mfs), transformers, numpy, scipy, scikit-learn,
  #    loguru, requests, huggingface_hub. Mirror iter-7 pyproject.toml.
  #  - Copy CORE7 -> ./core.py and METH7 -> ./method_lib.py VERBATIM. In BOTH, repoint the module-level
  #    WORK constant to THIS workspace so RESULTS/CACHE/LOGS/cache land here (never write into iter_7).
  #    Keep _find_sae_params() (auto-locates the cached SAE npz) and the unsloth fallback loader untouched.
  #  - Set HF_HUB_OFFLINE=1 if the SAE+model are already cached; else allow one download. HF_TOKEN optional
  #    (unsloth mirror is ungated). cache/ holds encodings + is EXCLUDED from upload (.gitignore-style).
  #  - aii-openrouter-llms for the judge; reuse METH7 judge infra (PRIMARY=anthropic/claude-haiku-4.5,
  #    SECOND auto-resolved from gpt-4o-mini / gemini-2.5-flash). Global SPENT cap TARGET=3.0, HARD_CAP=10.0.

  # ============================ STEP B. ADD THE NEW FAIR-GATED OPERATOR (the only genuinely-new edit code) =====
  # In ./core.py add kind=='erase_dir_gated_fair' to make_edit_hook(), _make_clamped_hook(),
  # and thread it through read_resid_under_edit()/forward_pos_logprobs()/behavioral_curve()/generate_under_edit().
  # Extend the hook signature with: gw (d_sub weight tensor [d_model]), gb (d_sub bias float), beta (<=1), gate_thresh.
  # Operator (UNIFIED, identical to iter-8 Artifact-1 spec -> MINOR-4 unification):
  #     dot  = h @ u                                   # u == unit u_sub (the labeled sub-direction; full projection)
  #     gate = (h @ gw + gb) > gate_thresh             # PRECISE d_sub detector (AUC~1.0) decides WHERE to erase
  #     hf   = hf - min(beta,1.0) * dot.unsqueeze(-1) * u.view(1,1,-1) * gate.unsqueeze(-1).to(hf.dtype)
  #     counter['edited'] += int(gate.sum()); counter['total'] += int(gate.numel())
  # RATIONALE vs iter-7 erase_dir_gated: iter-7 gated on |h.u_sub|>tau (a CRUDE magnitude gate calibrated to a
  # 3% GLOBAL footprint) which forced beta~2.97 over-erasure. THIS gate uses the precise supervised d_sub and
  # CAPS beta at 1.0 (beta=1 == full removal of the labeled component at exactly the detected X tokens), so it is
  # the genuinely-FAIR conditional-dense control. gate_thresh default 0.0 (prob 0.5); also record an alt calibration
  # where gate_thresh is set so the gate's X-recall equals the KG absorber's X firing-recall (report both, primary=0.0).

  # ============================ STEP C. BUILD THE CANDIDATE POOL ($0) ================================
  # C1. SPELLING word-absorbers (hierarchy='first_letter_spelling', parent=<letter>):
  #   curated = {L: large,list,line,law,like,level,low,leave,land,life ; O: our,one,only,other,out,over ;
  #              T: that,their,there,time,take,this ; I: in,into,it,is,if ; D: day,down,do,did,does}
  #   UNION the NON-EMPTY words in KG4.metadata.canonical_units.first_letter.{L,O,T,I,D}.sub_by_absorber
  #   (e.g. L: 3069->list, 2416->line, 3353->level, 3858->low, 7544->leave). Keep only words present in D1's
  #   per-letter corpus with >=12 word-initial windows (load via core.load_first_letter(['L','O','T','I','D'])).
  #   The absorber latent is RE-DERIVED in STEP D (do NOT trust sub_by_absorber gaps; large->8463 came from iter-7
  #   re-derivation, not iter-4). Carry 'large'=8463 as a hardcoded positive-control anchor.
  # C2. HOMOGRAPH entities (hierarchies city/month/given_name/brand):
  #   The shipped HG_DIR/full_data_out.json + manifest.json are ABSENT on disk -> REBUILD first (exactly as the
  #   iter-6 router experiment did): copy HG_DIR to ./homograph_data/, run `python pipeline.py --scale full --no-llm`
  #   there ($0, writes full_data_out.json + manifest.json). Read manifest.absorption_readiness per (hierarchy,entity);
  #   keep entities with status 'eligible' (>=150 diagnostic positives) OR diagnostic_positives>=120.
  #   curated must-include (reviewer-named): Apple,Shell,Target,Orange (brand); Grace,Hope,Mark,Will (given_name);
  #   March,June,May (month); Amazon,Bush,Cook (positive-control anchors from iter-7). sub_context=entity in TARGET
  #   sense; siblings=other eligible entities SAME hierarchy in target sense; hard-negatives=homograph_competitor rows.
  # C3. DISTRIBUTED-ABSORPTION population anchors (load from D2 via core.load_taxonomic): Georgia(16009),
  #   Jordan(540) -- known NO_MEANINGFUL_FORGET losers. Include 2-3 so the population scatter has the
  #   low-concentration/absorption-structured quadrant (else the M3''' contrast is unidentified).
  # Each candidate := {token, hierarchy, parent, dataset_handle}.  Expect ~45-70 candidates total.

  # ============================ STEP D. PER-CANDIDATE CONCENTRATION SCREEN ($0, GPU encode, cached) ===
  # load_sae(); ModelBundle(); determine_layer_idx() once (expect idx 13, FVU~0.19, cosine>0.9 gating PASS).
  # Build a NEUTRAL token pool (core.NEUTRAL_TEXT) once for footprint calibration.
  # for cand in pool:
  #   rows_X    = corpus windows where token appears in TARGET sense  (held-out fold for eval; disjoint fit fold for u_sub/d_sub)
  #   rows_SIB  = corpus windows of SIBLING tokens (same hierarchy, target sense)
  #   pairs     = content_pairs (x_on/x_off) for the token if present (spelling+homograph ship these)
  #   lat_csr, resid = mb.encode_rows(rows_X+rows_SIB+pairs)         # cache under cache/enc_<cand>_*.npz
  #   cr, prec_vec, _ = core.content_responsive(A_on, A_off)         # per-latent content-responsiveness + precision
  #   anchor      = highest-recall content-responsive latent on PARENT contexts (hierarchy-level; reuse KG4 anchor when available)
  #   recall_hole = 1 - mean(anchor fires on rows_X)
  #   # K-track precision selection (anchored, recall-hole-guided) -> the 'absorber' the method discovers:
  #   absorber    = argmax over cr latents s.t. firing_Jaccard(l,anchor)<0.1 AND precision_on_X(l)>=0.7 of coverage(l on rows_X)
  #                 (if none qualifies -> absorber=None, candidate flagged structure_absent, still screened for concentration)
  #   # UNCONSTRAINED max-precision selector (M3''' / M5''' baseline -- NO anchor/Jaccard constraint):
  #   max_prec_latent = argmax over cr latents with firing_on_X>=min_fire of precision_on_X(l)
  #   precision   = precision_on_X(absorber or max_prec_latent)
  #   footprint   = mean over NEUTRAL pool tokens of (chosen latent fires)   # forward over NEUTRAL_TEXT, count z[l]>0
  #   concentration_score = precision * (1 - footprint)                      # high precision AND sparse => concentrated
  #   firing_jaccard      = Jaccard(absorber/parent positive-token sets)
  #   absorption_structured = (recall_hole >= 0.6) and (firing_jaccard < 0.1)  # REPORTED, never gates the screen
  #   set_cover_eq_max_precision = (absorber is not None and absorber == max_prec_latent)
  #   record screen_row{token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,
  #                     absorber,max_prec_latent,set_cover_eq_max_precision,absorption_structured}
  # rank pool by concentration_score DESC.

  # ============================ STEP E. EDIT SET SELECTION (gradual scaling, breadth-first) ==========
  # edit_set = top-K by concentration_score (K ~= 10-14, concentrated co-firing candidates ARE eligible -- the
  #   reframe predicts they can win) UNION the population anchors {large(8463), Amazon, Bush, Cook} (positive controls,
  #   re-run to confirm the pipeline reproduces iter-7's KG win) UNION {Georgia, Jordan} (distributed-absorption losers).
  # Edit MOST-CONCENTRATED FIRST so breadth of independent wins is maximized before budget/time exhausts.
  # Use aii-long-running-tasks gradual pattern: smoke(2 cands) -> mini(5) -> full. Track SPENT after every judge batch.

  # ============================ STEP F. PER-CANDIDATE EDIT + MATCHED-FORGET COMPARISON ==============
  # for cand in edit_set (ordered):
  #   u_sub, u_meta = method_lib.build_u_sub(resid, X_pos_fit_mask, SIB_pos_fit_mask, probe.d_mu, fb...)
  #   d_sub         = method_lib.fit_sub_probe(resid, X_pos_fit_mask, SIB_pos_fit_mask)   # frozen {w,b,auc}; need auc>~0.9
  #   if u_meta.underpowered (n_pos<MIN_SUB=20) or d_sub is None: mark descriptive_only, emit screen row, CONTINUE
  #   # ---- OPERATORS (sweep each; all share ONE u_sub + ONE d_sub) ----
  #   OPS = {
  #     'KG-ABL'                  : (abl_latent,           l=absorber,          sweep LAM_GRID [0,.5,1,2,3,4]),
  #     'DENSE-SUB-ABL'           : (erase_dir,            u=u_sub,             sweep BETA_GRID [0,.5,1,1.5,2,3,4,6,8])  # LEAD comparator (strongest ungated dense),
  #     'DENSE-SUB-ABL-GATED-FAIR': (erase_dir_gated_fair, u=u_sub,gw=d_sub.w,gb=d_sub.b,gate_thresh=0, sweep beta [0,.25,.5,.75,1.0])  # BOUNDED beta<=1 (establishing control),
  #     'MAX-PREC-ABL'            : (abl_latent,           l=max_prec_latent,   sweep LAM_GRID)  # M3''' set-cover-vs-max-precision ablation
  #   }
  #   # ---- BEHAVIORAL forget curve per op (M4''': match on BEHAVIOR, NOT next-token KL) ----
  #   base_rate = subprobe_positive_rate(d_sub, resid_of(X_held_rows))   # ~1.0
  #   for op,scale: resid_e = read_resid_under_edit(X_held_rows, kind=op,...,scale); sub_drop(op,scale)=base_rate-subprobe_positive_rate(d_sub,resid_e)
  #   completion_drop via method_lib.completion_drop with TEMPLATED probes (M4''' ~20-50/case):
  #       spelling: ['{w} starts with the letter','The first letter of the word {w} is','{w} is spelled starting with',
  #                  'The word {w} begins with the letter', ... ~10 templates] gold=first letter (uppercase)
  #       homograph: target-sense completions where templatable (brand: '{e} announced a new'->product;
  #                  month: 'The month after {prev} is'->{e}; given_name: weak->rely on sub_drop); else completion=None.
  #   # ---- MATCHED MEANINGFUL-FORGET POINT (behavioral) ----
  #   FORGET_FLOOR=0.10 (meaningful); matched_target = max(FORGET_FLOOR, 0.8*min_op(max achievable sub_drop))
  #   for op: s_op = smallest scale whose interpolated sub_drop reaches matched_target; if op cannot reach it within its
  #           sweep (esp FAIR-GATED at beta=1.0) -> op_saturated=True, s_op=max-forget scale, note 'cannot match'.
  #   meaningful_forget = (KG sub_drop at s_KG >= 0.10) AND (completion drop CI>0 OR KG sub_drop>=0.10)  # success-criteria OR
  #   # ---- JUDGED JOINT at the matched point (2 judges) ----
  #   prompts: FORGET (~24, prefixes from X-held rows), RETAIN (~20, sibling rows), UNRELATED (~20, NEUTRAL_TEXT)
  #   for op: conts = generate_under_edit(prompts, kind=op,...,scale=s_op, clamp_norm=True)
  #           judge each (claude-haiku + 2nd) -> {fluency0-2, content_pres0-2}; joint=HM(fluency,content_pres)
  #           op_joint = aggregate(forget_quality on FORGET, preservation on RETAIN+UNRELATED)   # iter-7 convention
  #   Delta_joint(KG vs DENSE-SUB-ABL)     = paired_bootstrap_diff(joint_KG, joint_ungated)  per judge, B=10000
  #   Delta_joint(KG vs DENSE-SUB-ABL-GATED-FAIR) = paired_bootstrap_diff(...)               per judge, B=10000
  #   KG_beats_ungated  = both judges' CI excl 0 favoring KG
  #   KG_beats_fair     = both judges' CI excl 0 favoring KG (if fair op_saturated below match: KG auto-wins on forget,
  #                       still report the joint delta at the common achievable forget + the saturation note)
  #   concentrated_win  = meaningful_forget AND KG_beats_fair
  #   emit per-(token,role,prompt) prediction rows: predict_kg_abl/predict_dense_sub_abl/predict_dense_sub_gated_fair/
  #       predict_max_precision/predict_noop = the continuation STRINGS (all rows MUST carry these as strings -> validator),
  #       + per-op joint, sub_drop, footprint, s_op utilities.
  #   STOP issuing NEW judge calls once SPENT>=TARGET; remaining edit_set candidates fall back to $0 screen-only rows
  #   (concentration + structure + set_cover flag computed, edit/Delta marked budget_skipped).

  # ============================ STEP G. VERDICT (base count, M2''') ================================
  # known_wins = {'large','Amazon'} (iter-7); re-confirmed here as positive controls (assert KG_beats_fair reproduces;
  #   if a control FAILS to reproduce, that is a flagged honest negative about the new fair operator, not a silent pass).
  # new_wins = {token : concentrated_win True and token not in known_wins}
  # total_independent_concentrated_wins = | dedupe_by_token(known_wins UNION new_wins) |
  # verdict = 'BASE_REACHES_4_PLUS' if total>=4 else 'BASE_STAYS_THIN_RETARGET'
  #   (the latter triggers the paper retarget to 'localization+editing of homograph-polysemy absorption').

  # ============================ STEP H. POPULATION PREDICTOR ANALYSIS (decisive M3''' evidence) =====
  # over EDITED candidates that produced a Delta_joint (include the Georgia/Jordan distributed anchors + any co-firing):
  #   features: C=concentration_score (continuous), S=absorption_structured (binary 0/1)
  #   outcomes: Ymag=Delta_joint(KG vs fair) (continuous win-magnitude), Ywin=concentrated_win (binary 0/1)
  #   spearman(C,Ymag)+bootstrap CI ; point_biserial(C,Ywin)+CI
  #   point_biserial(S,Ymag)+CI     ; phi/point_biserial(S,Ywin)+CI
  #   predictor_verdict = 'CONCENTRATION_PREDICTS' if |corr(C,.)| CI is higher and excludes 0 while |corr(S,.)| does not,
  #                       'ABSORPTION_PREDICTS' if reverse, else 'TIE/UNDERPOWERED' (report n and CIs honestly).
  #   set_cover_inertness_rate = mean(set_cover_eq_max_precision over candidates with an absorber)  # M5'''
  #   (Report the expected story per the reframe: a concentrated CO-FIRING latent CAN win; Georgia/Jordan absorb but
  #    have LOW concentration and lose. Do NOT assert it -- let the correlation+CI decide; underpowered is reportable.)

  # ============================ STEP I. OUTPUT (exp_gen_sol_out schema) =============================
  # method_out.json:
  #   metadata: {method_name, description, sae{release,sae_params,width,d_model,hook}, model, seed, B_boot,
  #     gating_check{cosine,L0,fvu_by_idx,layer_idx}, forget_grids, judge{models,target_usd,hard_cap,spent_usd,calls},
  #     fair_gate_spec{operator='erase_dir_gated_fair', beta_cap=1.0, gate_thresh_primary=0.0, gate_alt='X-recall-matched'},
  #     concentration_screen_table:[per-candidate dict],
  #     base_count{known_wins, new_wins, total_independent_concentrated_wins, verdict},
  #     population_predictor{spearman_conc_mag_ci, pb_conc_win_ci, pb_absorp_mag_ci, pb_absorp_win_ci, predictor_verdict, n},
  #     set_cover_inertness_rate,
  #     honest_negatives:[ verbatim list -- see fallback ] }
  #   datasets:
  #     {dataset:'concentration_screen', examples:[ one per candidate; input=human-readable desc, output=tag
  #        ('concentrated_win'/'meaningful_no_win'/'no_meaningful_forget'/'structure_absent'/'budget_skipped'),
  #        metadata_*: token,hierarchy,precision,footprint,concentration_score,recall_hole,firing_jaccard,absorber,
  #        max_prec_latent,set_cover_eq_max_precision,absorption_structured,meaningful_forget,
  #        delta_joint_vs_ungated_{primary,second}_{diff,ci_lo,ci_hi,excl0}, delta_joint_vs_fair_{...},
  #        kg_beats_ungated,kg_beats_fair,fair_saturated, AND predict_* STRING fields (set to op tag/'NA') ]},
  #     {dataset:'edit_predictions', examples:[ per (token,role,prompt): input=prompt, output=role,
  #        predict_kg_abl, predict_dense_sub_abl, predict_dense_sub_gated_fair, predict_max_precision, predict_noop
  #        (continuation STRINGS), metadata_*: token,role,sub_probe_drop_kg, joint_kg, joint_ungated, joint_fair, s_op_* ]}
  #   EVERY example in EVERY dataset MUST carry the five predict_* keys as STRINGS (iter-5 GOTCHA: missing/
  #   non-string predict_* => validator FAIL). Use make_variants.py (copied from iter-7) to emit
  #   full/mini/preview_method_out.json each <100MB; validate all three with aii-json against exp_gen_sol_out.
  #   Exclude cache/ and .venv/ from the uploaded artifact.

  # ============================ COST / TIME BUDGET ==================================================
  # $0 screen over the full pool first. Editing ~12-16 candidates x 2 judges x ~64 continuations ~= $1.5-2.5 (iter-7
  # was $0.80 for 5 cases). Hard-stop judge calls at SPENT>=3.0. GPU wall-clock budget ~5h of the 6h: encoding is the
  # bulk (cached); generation+forward sweeps dominate per edited candidate (~10-15 min each). PID-based process mgmt only.
fallback_plan: |-
  DATA / REBUILD failures: (1) If `pipeline.py --scale full --no-llm` for the homograph dataset errors (geonamescache/protobuf/libgomp quirks seen in prior iters), fall back to `--scale smoke` for structure then hand-load the entities directly from HG_DIR/data.py's entity gazetteers + D1-style corpus windows; if it still fails, DROP the homograph hierarchies and run the base-widener on SPELLING words alone (L/O/T/I/D give 20-40 candidates -- enough for the population test and >=4-win target on concentrated spelling absorbers). (2) If a candidate has too few corpus positives for a trustworthy u_sub/d_sub (n_pos<MIN_SUB=20, AUC<0.9), mark it descriptive_only and keep it in the $0 screen (still contributes concentration + structure + set_cover flag) but exclude from the edit/Delta analysis -- report the excluded count.
  OPERATOR failures: (3) If the bounded-beta (<=1) fair-gated dense CANNOT reach the matched meaningful-forget for many candidates, that is a SUBSTANTIVE result, not a bug: KG wins on forget by construction -- report it as 'fair gated dense saturates below meaningful forget at beta<=1' and compare joint collateral at the common achievable forget. Also run the alt gate_thresh (X-recall-matched) to show the conclusion is calibration-robust. (4) If generation NaNs in bf16, use the clamp_norm=True path (_make_clamped_hook, already supports the new operator).
  BUDGET / TIME truncation (pre-registered drop order, breadth-first): keep the $0 full-pool concentration screen + set_cover_inertness ALWAYS (they alone answer M3''' structurally and M5'''); then the positive-control re-runs (large, Amazon); then top-concentration new candidates until SPENT>=3.0 or time runs low; DROP (first-dropped-first) the MAX-PREC-ABL judged edit (keep its $0 set_cover_eq flag), then the second judge on lowest-concentration candidates (keep primary), then the distributed-absorption Georgia/Jordan re-edit (cite iter-7 numbers as population anchors instead). NEVER drop: the concentration screen, >=the two positive-control wins, the population correlation over whatever edited points exist.
  VERDICT robustness: (5) If <4 independent concentrated wins land, emit BASE_STAYS_THIN_RETARGET honestly (this is an expected, publishable outcome that triggers the paper's localization-first retarget) -- do NOT inflate by re-counting the confirmatory Amazon or the excluded co-firing insult as load-bearing. (6) If the population correlation is underpowered (too few edited points / wide CIs), report 'TIE/UNDERPOWERED' with n and CIs rather than asserting CONCENTRATION_PREDICTS.
  HONEST NEGATIVES to record verbatim in metadata.honest_negatives: fair-gated-dense matches KG (=> value is label-free where-to-gate discovery, gating is prior art CAST/GSS/GUARD-IT/SADI); set-cover absorber == max-precision latent for most candidates (=> method is precise-latent discovery, set-cover inert); base stays thin (n~2-3) => retarget; concentration does NOT out-predict absorption (=> reframe unsupported, report as-is); distributed-absorption candidates show no meaningful forget (carries iter-7 Georgia/Jordan); homograph rebuild required (data not shipped); positive control fails to reproduce under the new fair operator.
testing_plan: |-
  1) SMOKE (logic, ~2-5 min, $0): run with a 2-candidate pool {large (spelling, known win), Georgia (taxonomic, known no-forget loser)} and tiny caps (cap=20 rows, 3 FORGET/2 RETAIN prompts, judges DISABLED by unsetting OPENROUTER_API_KEY). CONFIRM: SAE loads (d_sae=16384, d_model=2304), determine_layer_idx selects 13 with cosine>0.9 (gating PASS), encode_rows runs, the new erase_dir_gated_fair hook executes without shape/NaN errors and its token-footprint counter is >0 on X tokens and ~0 on neutral tokens, content_responsive returns cr latents, the concentration screen emits rows with precision/footprint/concentration_score in [0,1], and large's re-derived absorber == 8463 (sanity vs iter-7). Output a valid (judge-less) method_out.json skeleton.
  2) OPERATOR UNIT CHECK ($0): on 'large', verify (a) KG-ABL sub-probe positive-rate drops monotonically with lambda; (b) DENSE-SUB-ABL-GATED-FAIR at beta=1.0 produces a LARGE sub_drop ON X tokens but tiny token_footprint on UNRELATED/neutral text (precise gate), and at beta=1.0 the on-X erasure is full-projection (sub_drop>=ungated at matched gate) -- confirming it is a strong, fair, non-over-erasing control; (c) MAX-PREC-ABL on 'large' selects a latent and set_cover_eq_max_precision resolves to a definite bool. Print the matched-forget scales s_op and confirm they are finite.
  3) MINI (~15-25 min, <$0.5): 5 candidates {large, Amazon (rebuild homograph first), one new concentrated spelling word, one new homograph entity, Jordan}. ENABLE both judges on a reduced prompt set (~10/role). CONFIRMATION SIGNALS before scaling: large reproduces KG_beats_fair (positive control passes); Jordan shows NO meaningful forget (sub_drop<0.10); Delta_joint CIs compute under both judges; SPENT tracked and well under TARGET; the population-predictor function runs on >=4 points without error. If the large positive control does NOT reproduce a KG win under the new fair operator, STOP and debug the operator/gate calibration before spending more budget.
  4) FULL: only after mini confirms the positive control + judge pipeline + cost tracking. Screen the full pool ($0), then edit most-concentrated-first until SPENT approaches 3.0 or ~5h elapsed. After completion: validate full/mini/preview method_out.json with aii-json against exp_gen_sol_out (every example has the 5 predict_* STRING keys), confirm each variant <100MB, confirm cache/ excluded. Sanity-check the verdict arithmetic (total_independent_concentrated_wins dedup by token) and that honest_negatives reflects the actual outcome (no inflation of confirmatory/co-firing cases into the load-bearing count).
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_RidEJtBC7gPT
type: research
title: 'Two-Track CCRG Implementation Dossier: SAE Pipeline, 11 Baselines, Protocols'
summary: >-
  A decision-complete, code-ready implementation blueprint for the two-track Counterfactual Co-Response Grouping (CCRG) method
  on frozen Gemma Scope SAEs. Pins the SAE encoding pipeline (defensive from_pretrained loader, JumpReLU firing=encode>0,
  hook blocks.12.hook_resid_post), the C-track (signed soft-threshold + leidenalg RBConfigurationVertexPartition) and K-track
  (anchored greedy max-coverage) algorithm with all thresholds, all eleven baselines (a)-(k) as runnable specs (LEACE for
  f, SAEBench SCR/TPP for g/h, JTT/GEORGE/group-DRO for j/k), the AxBench steering protocol (harmonic-mean LLM-judge 0/1/2),
  a corrected model-diffing recipe (shared frozen pt-SAE on gemma-2-2b vs gemma-2-2b-it because no gemma-scope-2b-it SAE exists),
  the statistics plan (paired bootstrap, exact McNemar, MDE n_min=150, Holm-Bonferroni), and a fully-verified 30+ citation
  table including all four high-risk future-dated arXiv IDs (all resolve).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_dpYpjSn2Xvg3
type: dataset
title: >-
  First-Letter-Spelling Absorption Testbed (L/O/T/I/D): minimal pairs + frozen Pile corpus
summary: |-
  First-Letter-Spelling Absorption Testbed — the load-bearing dataset for the Two-Track Co-Response Grouping hypothesis (building reliable cluster-level units from individual SAE latents). Pure CPU/data artifact: NO SAE, no model weights, no GPU. 17,180 examples in 5 per-letter dataset groups (first_letter_spelling_{L,O,T,I,D}; L primary, O/T/I/D secondary; degenerate S/X excluded), schema exp_sel_data_out (full/mini/preview all PASSED).

  Three linked components per letter: (A) content_flip minimal pairs — (x_on,x_off) in an IDENTICAL carrier where x_on slots a word STARTING WITH the target letter and x_off a surface-matched word that does NOT (matched on char length, single-token-ness, Pile log-frequency); 1,750 pairs / 3,500 rows. Feeds the Tier-0 K-track anchored set-cover PROPOSAL pilot and the C3 absorber-recovery spine; reconstruct via metadata_pair_id and compute r_l=a_l(x_on)-a_l(x_off). (B) surface_flip pairs — (x_a,x_b) in an identical carrier, BOTH words start with the target letter but differ; 590 pairs / 1,180 rows; for the unit-level surface-invariance admission check (pooled response to surface flips ~0). (C) corpus_context — 12,500 real ~48-token windows (2,500/letter) from monology/pile-uncopyrighted @ rev 3be9033, each centred on a slot-eligible word-initial target-letter token with token_position annotated; plus a per-letter occurrence table (<=2,000 word-types) in dataset-level metadata — the substrate for iteration-2's form-free/Chanin (2409.14507) absorption diagnostic to locate false-negative absorbers (e.g. lion, London).

  Words are anchored in the real gemma-2-2b vocabulary (unsloth/gemma-2-2b ungated mirror, vocab==256000) via the exact sae-spelling get_alpha_tokens slot-eligibility recipe (word-initial '_' marker AND alpha). 7 carriers per content pair: sae-spelling spelling prompts (t_verbose '{word} has the first letter:', t_colon, t_icl with contamination-free ICL examples) + 4 word-class-agnostic mention carriers.

  Row schema is FLAT (exp_sel_data_out): input, output (first letter, uppercase), and metadata_* keys (dataset, letter, pair_id, pair_type, role, sub_context=the word covered, target_word, counterpart_word, template_id, label_starts_with_target, is_single_token, is_slot_eligible, first_letter, fold, word_char_span; corpus rows add source_doc_id, pile_revision, token_position, target_token_id, window_char_span, target_char_in_window). Pairs LINK via shared metadata_pair_id + metadata_role ({on,off}/{var_a,var_b}). Folds: minimal pairs by target_word, corpus by source_doc_id (5 folds, no leakage).

  Validation: the deterministic check is AUTHORITATIVE and reports 0 violations / 17,180 rows (flip property + input-span correctness are guaranteed by construction). The LLM judge (google/gemini-3.1-flash-lite, $0.12 total, < $3 cap) is a SECONDARY grammaticality/independent audit with pass rates 0.89-0.99 per (letter,pair_type); judge false-negatives are retained because the deterministic check governs drops. Corpus token_position verified EXACT (tok(input,add_special_tokens=False)[token_position]==target_token_id) on sampled rows. Frozen & reproducible: pinned tokenizer + Pile revision 3be90335..., seed 1234, deps pinned in pyproject.toml; data.py rebuilds end-to-end. full_data_out.json=21MB (<100MB, no split). NOTE: iteration-2 reads SAE activations on these inputs; this artifact itself does not run the SAE.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 3 ---
id: art_2xQn686KUmV5
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands)
summary: |-
  A pure CPU/text artifact: a FOUR-hierarchy homograph/polysemy entity absorption testbed, built as a strict structural drop-in extension of the iter-1 non-spelling absorption testbed (art_t2uUbjSwpd3t). It is explicitly a NEXT-ITERATION BUILDING BLOCK (not consumed by this iteration's parallel experiments): it supplies breadth of suppressed-parent candidates so the persistent single-slice taxonomic critique (Georgia-only) can be answered with many homograph cases.

  Four `dataset`s, one per is-a hierarchy, whose surface tokens carry a strong competing NON-target sense (the competition that produces feature absorption / a suppressed-parent recall hole):
    1. city_homograph_absorption  (parent = is-a-city): Phoenix, Mobile, Reading, Bath, Nice, Buffalo, Paris, Mercury, Jackson, Columbus, Cleveland, Florence, ... (23 entities).
    2. month_name_absorption (parent = is-a-month): all 12 calendar months; homograph-strong May/March/August/April/June.
    3. given_name_absorption (parent = is-a-given-name): Grace, Hope, Mark, Will, Rose, Frank, Faith, Joy, Dawn, Jack, ... (34 entities).
    4. brand_homograph_absorption (parent = is-a-brand): Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java, ... (24 entities).

  Each hierarchy ships the SAME three coordinated components as dataset_2: (A) content-flip minimal pairs (parent present vs absent, surface-matched), (B) surface-flip pairs (concept fixed, surface varied; both positive, for the unit-level surface-invariance check), and (C) a frozen monology/pile-uncopyrighted diagnostic corpus (pinned rev 3be90335b66f24456a5d6659d9c8d208c0357119) of real windows labelled by frozen, model-independent sub-context. The NEW homograph_competitor negative family (the same surface token in its non-target sense, e.g. lowercase 'apple'/'will'/'march', 'Joaquin Phoenix', 'Christopher Columbus') is the matched hard control that makes a suppressed parent visible.

  On-disk format is the AII exp_sel_data_out schema: {metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]} with FLAT metadata_* keys (no nested objects). New/extended fields vs iter-1: metadata_hierarchy (city|month|given_name|brand), metadata_entity (canonical surface), metadata_target_sense (city|month|given_name|brand|competitor|null), metadata_competitor_sense (gloss of competing sense), metadata_homograph_strength (wordfreq Zipf of the lowercase competitor), and metadata_neg_family expanded to include homograph_competitor / other_place / other_time / other_person_ref / other_company_ref / easy. Fold semantics are unchanged (pairs 70/30 train/test by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified), gemma-2-2b offset-mapping token anchoring is reused (metadata_target_token_indices), and the downstream K-track + form-free absorption diagnostic pipeline runs unchanged except for the new enum values.

  Labels are assigned PURELY from surface form / regex / gazetteer (geonamescache for cities) / disambiguating local context — never from a model — so the degenerate-construction guard holds and absorption presence/absence stays a future-iteration EMPIRICAL finding: the corpus equally supports the 'absorption is spelling-specific' null and a positive homograph-absorption finding. Corpus target-sense labels use high-precision case-aware cues; an LLM-judged stratified sample MEASURES per-hierarchy target-sense precision (reported in manifest.json, target >=0.9; it does not relabel the corpus). manifest.json carries per-(hierarchy,entity) absorption_readiness with diagnostic_positives counts and status (eligible if >=150 diagnostic-fold positives, else descriptive_only), eligible_entities_per_hierarchy, per-component counts, source/pile-set counts, llm_pair_pass_rate, llm_corpus_sense_precision, llm_cost_breakdown, city geonames provenance, and cross-hierarchy collision notes (Dawn, Chase, Jordan, Mercury, Paris). Deliverables: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, and full/mini/preview_data_out.json (validated against exp_sel_data_out, each <100MB). Reproducible via fixed seed 20240617 and pinned pile revision; total LLM spend well under $1.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_4i-Wywa44JXf/3_invention_loop/iter_5/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — framework choices, implementation patterns, agent orchestration
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [9] SYSTEM-USER prompt · 2026-06-18 20:23:53 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [10] SYSTEM-USER prompt · 2026-06-18 20:28:00 UTC

```
<validation-feedback>
Attempt 2 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [11] SYSTEM-USER prompt · 2026-06-18 20:33:32 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 1/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [12] SYSTEM-USER prompt · 2026-06-18 20:37:33 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 2/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json
  - Missing file: mini_method_out.json
  - Missing file: preview_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```
