# gen_art — test_idea

> Phase: `invention_loop` · round 5 · Substep: `gen_art`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave the agent(s) in this substep — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_evaluation_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:11:52 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 52201 chars total]
```

### [2] HUMAN-USER prompt · 2026-06-18 02:11:52 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-18 02:11:58 UTC

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

### [4] SKILL-INPUT — aii-json · 2026-06-18 02:11:58 UTC

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

### [5] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:11:58 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-06-18 02:11:58 UTC

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

### [7] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:11:58 UTC

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

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-18 02:11:58 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SYSTEM-USER prompt · 2026-06-18 02:22:56 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1/`:
... [truncated, 52746 chars total]
```

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:12:05 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 47678 chars total]
```

### [2] HUMAN-USER prompt · 2026-06-18 02:12:05 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-18 02:12:15 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:12:15 UTC

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

### [5] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:12:15 UTC

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

### [6] SKILL-INPUT — aii-json · 2026-06-18 02:12:19 UTC

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

### [7] SKILL-INPUT — aii-parallel-computing · 2026-06-18 02:12:19 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [8] SKILL-INPUT — aii-openrouter-llms · 2026-06-18 02:12:19 UTC

The agent loaded the **aii-openrouter-llms** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-openrouter-llms
description: Searches and calls LLMs from OpenRouter's extensive catalog (Claude, GPT, Gemini, Llama, Mistral, DeepSeek, etc.) with reasoning and temperature control. Use when user needs to access various LLMs, compare language models, call different model providers, find the best model for a task, or look up model pricing and costs per million tokens.
---

## Contents

- Workflow (2-phase model discovery and calling)
- Scripts (Search, Get Params, Call)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: Model Discovery and Calling

### Phase 1: Search for Models
Find models with pricing, context length, and descriptions
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

### Phase 2 (optional): Get Model Parameters
Check what parameters a specific model supports
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

### Phase 3: Call Model
Call a model using the API name from search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

---

## Scripts

### Search OpenRouter models (aii_or_search_llms.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_search_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 5' ::: 'claude' 'gpt' 'gemini'
```

**Example output:**
```
Found 5 models for query: claude

[1] Anthropic: Claude Opus 4.5
    API: anthropic/claude-opus-4.5
    Context: 200,000 tokens
    Price: $5.00/M in, $25.00/M out
    Claude Opus 4.5 is Anthropic's frontier reasoning model...

[2] Anthropic: Claude Haiku 4.5
    API: anthropic/claude-haiku-4.5
    Context: 200,000 tokens
    Price: $1.00/M in, $5.00/M out
    ...
```

**Parameters:**

`query` (optional, positional)
- Search query to filter models (e.g., 'claude', 'gpt', 'reasoning')

`--limit, -n` (optional)
- Maximum number of results (default: 10)

`--series, -s` (optional)
- Filter by model family
- Valid: GPT, Claude, Gemini, Grok, Cohere, Nova, Qwen, Yi, DeepSeek, Mistral, Llama2, Llama3, Llama4, RWKV, Qwen3, Router, Media, Other, PaLM

`--timeout` (optional)
- Request timeout in seconds (default: 60)

**Tips:**
- Use the `API` field from results for the `--model` parameter in calls
- Search is fast (queries OpenRouter's model list)

---

### Get model parameters (aii_or_get_llm_params.py)

Get detailed information and supported parameters for a specific model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

**Parallel execution (multiple models):**

IMPORTANT: When checking multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_get_llm_params.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: Anthropic: Claude Haiku 4.5
API: anthropic/claude-haiku-4.5

=== Capabilities ===
Context Length: 200,000 tokens
Max Output: 64,000 tokens
Modality: text+image->text
Input: image, text
Output: text
Moderated: Yes

=== Pricing ===
Input: $1.0000/M tokens
Output: $5.0000/M tokens

=== Supported Parameters ===
  - include_reasoning
  - max_tokens
  - reasoning
  - stop
  - temperature
  - tool_choice
  - tools
  - top_k
  - top_p
```

**Parameters:**

`model` (required, positional)
- Model API name (e.g., 'anthropic/claude-haiku-4.5', 'openai/o1')

`--timeout` (optional)
- Request timeout in seconds (default: 30)

**Tips:**
- Use after search to see which parameters a model supports
- Check supported_parameters before using --reasoning or other options

---

### Call OpenRouter model (aii_or_call_llms.py)

Make an API call to an OpenRouter LLM model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

**Parallel execution (multiple calls):**

IMPORTANT: When calling multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_call_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --model {} --input "What is 2+2?"' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: anthropic/claude-haiku-4.5

Response:
Four.

Tokens: 12 in, 5 out
```

**Parameters:**

`--model, -m` (required)
- API model name from search results (format: `provider/model-name`)
- Examples: `anthropic/claude-sonnet-4`, `openai/gpt-5`, `google/gemini-2.5-pro`

`--input, -i` (required, unless using --input-json)
- Simple string prompt

`--input-json` (optional)
- Full conversation JSON for multi-turn (mutually exclusive with --input)

`--max-tokens` (optional)
- Maximum output tokens (default: 9000)

`--reasoning` (optional)
- Reasoning effort for reasoning models: `minimal`, `low`, `medium`, `high`

`--temperature, -t` (optional)
- Randomness (0.0-2.0): 0.0=deterministic, 0.7=balanced, 1.5+=creative

`--top-p` (optional)
- Nucleus sampling (0.0-1.0)

`--instructions` (optional)
- System instructions/prompt

`--web-search` (optional)
- Enable web search with max results (e.g., 10)

`--params, -p` (optional)
- Extra model-specific parameters as JSON string
- Use `aii_or_get_llm_params.py` to see which params a model supports
- Example: `--params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'`

`--timeout` (optional)
- Request timeout in seconds (default: 120)

**Examples:**

Simple call:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "Write a haiku about coding" \
  --temperature 0.8
```

With system instructions:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-haiku-4.5" \
  --input "Explain recursion" \
  --instructions "You are a helpful programming tutor. Keep explanations concise."
```

With reasoning (for o1-style models):
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "openai/o1" \
  --input "Solve this complex math problem" \
  --reasoning high
```

With web search:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "What are the latest AI news?" \
  --web-search 10 \
  --max-tokens 15000
```

With extra model-specific params:
```bash
# Step 1: Check what params the model supports
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "meta-llama/llama-3.3-70b-instruct"
# Shows: frequency_penalty, top_k, seed, min_p, etc.

# Step 2: Call with those params
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "meta-llama/llama-3.3-70b-instruct" \
  --input "Write a short poem" \
  --params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'
```

---

## Tips

- Use `aii_or_search_llms.py` first to find models, then copy `API` field for `--model`
- Use `aii_or_get_llm_params.py` to check what params a model supports before using `--params`
- For web search, increase `--max-tokens` to handle larger responses (15000+)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [9] SYSTEM-USER prompt · 2026-06-18 02:34:52 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_1/`:
... [truncated, 47620 chars total]
```

### [10] SKILL-INPUT — aii-file-size-limit · 2026-06-18 03:20:22 UTC

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

### [11] SYSTEM-USER prompt · 2026-06-18 03:24:17 UTC

```
continue the M1 unlearning experiment: check smoke result and proceed to mini
```

## Task: `gen_art_experiment_4` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:12:06 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/results/out.json`
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
id: gen_plan_experiment_4_idx4
type: experiment
title: >-
  M7 — Second Polysemy/Absorption Case Beyond Georgia: Profession Is-A Hierarchy + Homograph Scan + Jordan-Beside-Georgia
summary: >-
  Search for >=1 additional suppressed-parent absorption case to corroborate the non-spelling set-cover-selection result that
  is currently effectively n=1 (Georgia), 1-2 with descriptive Jordan. Three parts on the FROZEN Gemma-2-2b / Gemma-Scope
  layer_12/width_16k JumpReLU SAE: (1) NEW corpus-only test of a SECOND is-a hierarchy = bias_in_bios professions (general
  'occupation' parent suppressed on specific professions), GPU-encoded fresh; (2) HOMOGRAPH SCAN re-running the country cross-tab
  + entity-token scan on the CACHED taxonomic encodings (CPU); (3) JORDAN-BESIDE-GEORGIA side-by-side selection table with
  n + eligibility. Reuse the iter-4 precision-gated K-track + selectors + AUC-diff machinery verbatim where possible. The
  EXPECTED, fully-publishable outcome is an honest negative ('absorption is narrow / specific to homograph-polysemy, not a
  general is-a-hierarchy phenomenon'); a positive second case strengthens the paper. Emit method_out.json (exp_gen_sol_out
  schema) with full hole tables, set-cover results with CIs, the side-by-side table, a 'second-case-found' vs 'absorption-remains-narrow'
  verdict, and per-row diagnostic predictions; validate full/mini/preview < 100MB.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ===================================================================================
  # GOAL (M7): corroborate the non-spelling absorption/set-cover result beyond Georgia.
  # THREE PARTS. Part 1 (professions) is the NEW science and needs GPU encoding (no cache).
  # Parts 2-3 reuse the iter-4 taxonomic CACHE on CPU. Honest negative is the EXPECTED, publishable outcome.
  # ===================================================================================
  #
  # ---- ABSOLUTE PATHS (verified to exist by the planner) ----
  # ITER4_DIR  = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
  # METHOD_SRC = ITER4_DIR/method.py            # 2108-line engine to COPY+adapt (do not re-derive)
  # TAX_LAT    = ITER4_DIR/cache/lat_taxonomic_w16384_n15748.npz   # cached taxonomic latents (CSR)
  # TAX_RES    = ITER4_DIR/cache/resid_taxonomic_w16384_n15748.npy # cached taxonomic residuals (fp16)
  # TAX_DATA   = .../iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # taxonomic+numeric testbed
  # BIOS_DATA  = .../iter_1/gen_art/gen_art_dataset_4/full_data_out.json   # sentiment+aspect+bias_in_bios
  # DOSSIER_M  = .../iter_1/gen_art/gen_art_research_1/research_out.json    # SAE pipeline/baseline spec
  # DOSSIER_D  = .../iter_1/gen_art/gen_art_research_2/research_out.json    # form-free absorption diagnostic
  #
  # STEP 0 — SCAFFOLD & REUSE ENGINE
  #   * Copy METHOD_SRC into THIS workspace as engine.py; import its functions rather than rewriting:
  #       load_sae, JumpReLUSAE, _find_sae_params, load_model, Encoder (adapted), encode_or_cache,
  #       run_greedy, iter3_extensions, formfree_edge_agreement, admission_check, bootstrap_ci,
  #       paired_diff_ci, fast_auc, _auc_rows, _youden_table, firing_jaccard_pos, holm, match_threshold,
  #       emit_method_out, _json_default, write_figure_csvs.
  #   * Copy the two taxonomic cache files into ./cache/ with IDENTICAL names so engine.encode_or_cache
  #     loads them (it asserts shape (15748,16384)); set CACHE_DIR=./cache. Keep CPU-fallback block intact.
  #   * Pin pyproject deps to the iter-4 versions (torch, numpy, scipy, scikit-learn, statsmodels, loguru,
  #     transformers, huggingface_hub, networkx). Install a torch wheel matching the LANDED GPU arch
  #     (cu124+; the gpu profile may fall back to A4000/L4/4090 = sm_86/89 which standard torch supports;
  #     only the 5090=sm_120 needs a newer wheel — probe CUDA once like engine.py and CPU-fall-back if a
  #     real device op raises).
  #   * Constants reused verbatim: G1_RECALL=0.60, JACCARD_MAX=0.10, SUBCTX_PREC=0.70, GAIN_MIN=0.05,
  #     PRECISION_FLOOR=0.70, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=12, SEED=20240617, D_MODEL=2304.
  #
  # ===================================================================================
  # PART 1 — SECOND IS-A HIERARCHY: bias_in_bios PROFESSIONS  (NEW, GPU encode)
  # bias_in_bios rows have NO content pairs and NO target spans -> CORPUS-ONLY adaptation.
  # Framing: parent concept = 'occupation/profession' (general); CHILDREN/sub-contexts = the 28
  # professions; absorption = a general occupation latent that fires on most bios but has profession-
  # specific recall HOLES where a mutually-exclusive specialist fires instead.
  # ===================================================================================
  #
  # 1A. LOAD & SUBSAMPLE
  #   bios = [r for r in BIOS_DATA.datasets where dataset name family=='bias_in_bios_boundary']
  #       each row: input=bio text, output=profession (e.g. 'journalist'), metadata_sub_context={'gender':..},
  #                 metadata_concept_label=profession, metadata_meta.raw_profession_int (0..27).
  #   prof = output label; gender = sub_context.gender.
  #   Keep ALL 28 professions; flag profession descriptive_only if its TOTAL bios < 2*N_MIN_ELIGIBLE
  #     (need >=150 in the diagnostic fold AFTER a 50/50 split). dataset is gender-balanced ~20,177/28~=720
  #     avg, but skewed -> some rare professions (e.g. rapper/dj/personal_trainer) may fall below.
  #   To bound GPU cost, optionally cap bios per profession at ~600 (stratified by gender, seed 20240617):
  #     total ~ min(20177, 28*600) ~= 12-16k. Record the cap in metadata.
  #
  # 1B. NEGATIVE POOL (for parent precision-gating + dense-probe baseline)
  #   neg_texts = stratified subsample ~5,000 from BIOS_DATA sentiment (movie reviews) + restaurant_aspect
  #     (CEBaB reviews) families — full texts, NON-occupation, SAME corpus file, encoded with IDENTICAL
  #     whole-text pooling so pool SIZE is held fixed (no length confound vs the single-slot taxonomic neg).
  #   CAVEAT to log + guard: a 'parent' could key on genre (bio vs review) not 'occupation'. MITIGATION:
  #     the PRIMARY per-profession AUC is ONE-VS-REST WITHIN bios (positives=prof-p bios, negatives=other-
  #     profession bios) which is genre-matched; non-bio negatives are used ONLY for parent precision-gating
  #     and the dense-probe sanity baseline. Report both negative regimes.
  #
  # 1C. ENCODE (GPU; the ONE expensive step — no cache exists)
  #   * Adapt engine.Encoder: bios have no target span, so add a pooling mode 'whole_text' ->
  #       positions = all tokens with non-zero offset width and attention_mask==1 (exclude BOS/pad).
  #       resid[gid] = mean over those token residuals (fp16); pooled_lat = MAX over those tokens' SAE
  #       latents (firing detector) -> CSR row. (Same max-pool firing rule as the rest of the method.)
  #   * MAXLEN=256 (bio char_len up to ~500 => ~120 tok; covers it). BATCH=16. Validate FVU<0.6, meanL0
  #     plausible (engine asserts). Token-alignment metric is N/A here (no target_text) -> skip that assert.
  #   * Determine layer via engine.determine_layer_idx on a 32-bio sample (expect hidden_states[13]).
  #   * SAVE cache: ./cache/lat_bias_w16384_n{N}.npz, resid_bias_w16384_n{N}.npy (so re-runs are GPU-free).
  #   * Encode neg_texts the SAME way -> lat_neg, resid_neg.
  #
  # 1D. FOLD SPLIT (mirror the method's selection/eval discipline)
  #   Split bios 50/50 train(SELECTION) / diagnostic(HELD-OUT), STRATIFIED by profession (seed 20240617).
  #   Gates, anchor recall, firing-Jaccard, subctx precision, greedy are FIT on SELECTION; AUC / hole table
  #   / router REPORTED on the disjoint HELD-OUT fold.
  #
  # 1E. PARENT (anchor) IDENTIFICATION — corpus-only (no content pairs)
  #   * 'content-responsive'/discriminative latent := firing_rate(bios_sel) - firing_rate(neg) above a
  #     LABEL-SHUFFLE null (shuffle bio/neg labels B=1000, 95th pct), AND content-style precision
  #     prec_l = firing on bios / (firing on bios + firing on neg) >= PRECISION_FLOOR(0.70).
  #   * anchor = among precision-passing discriminative latents, the one with the HIGHEST overall bio-recall
  #     (fraction of ALL selection bios where it max-fires). Firing-floor validation: anchor must fire on
  #     >5% of HELD-OUT bios (drops spurious 0%-corpus anchors, the iter-4 letter-I fix).
  #   * Also fit the dense parent probe d_p: LogisticRegression(class_weight='balanced') on mean-pooled
  #     residuals, bios(+1) vs neg(0), TRAIN fold -> non-SAE baseline direction (engine Phase 4 recipe).
  #
  # 1F. PER-PROFESSION HOLE TABLE (the headline deliverable; reported for ALL 28)
  #   For each profession p (held-out fold):
  #     recall_p   = mean(anchor fires on prof-p bios);  hole_p = 1 - recall_p
  #     specialists_p = latents with one-vs-rest subctx FIRING precision_p >= 0.70 (prof-p vs other-prof bios)
  #                     AND fire on >= GAIN_MIN of prof-p bios.
  #     best_jaccard_p = min over specialists_p of positive-only firing_jaccard(specialist, anchor)
  #     absorption_type_p = (hole_p > 0.5) AND (exists specialist with best_jaccard_p < JACCARD_MAX)
  #     n_p, eligible_p = (n_p >= N_MIN_ELIGIBLE)
  #   Emit hole_table[p] = {n, eligible, parent_recall, parent_hole, best_specialist, best_jaccard,
  #                         n_specialists, absorption_type, gender_split:{male_hole,female_hole}}.
  #   IMPORTANT: a uniform parent_recall~1.0 across professions (NO holes) is the EXPECTED boundary-null and
  #   must be emitted explicitly as 'absorption does not generalize to the profession is-a hierarchy'.
  #
  # 1G. SET-COVER + SELECTION ISOLATION (only for professions with absorption_type==True)
  #   For each qualifying profession q:
  #     * Build per-fold firing matrices over the discriminative/eligible latent pool ELIG (precision>=0.70).
  #     * anchor = parent; HOLES = prof-q bios the anchor misses; run engine.run_greedy variant='gated'
  #       (per-sub-context firing-precision gate + mutual-exclusivity J<0.10 + gain>=0.05 CI>0) AND 'weighted'.
  #     * Build det_scores via engine.iter3_extensions-style logic adapted to ONE-VS-REST (positives=prof-q
  #       held-out bios, negatives=other-profession held-out bios):
  #         unit (max-pool members), anchor, g (top-20 |mean_pos-mean_neg| marginal-attr), h (count-matched),
  #         dense_probe (one-vs-rest LR on residual), RE-k, RE-k-anchored, S_rec (top-k by bio-recall),
  #         S_prec (top-k by subctx precision), S_mag (top-k by mean firing magnitude).
  #     * AUC-diff CIs: stratified paired bootstrap B>=10,000 (resample positives & negatives separately),
  #       reuse engine._auc_rows. set_cover_established_q := unit beats S_rec_anch AND S_prec_anch AND
  #       S_mag_anch AND RE-k-anchored AND g AND h with 95% CI excluding 0 on the prof-q slice.
  #     * setcover_corroborated_q := the greedy-chosen specialist is the precision-diagnostic member (held-out
  #       subctx precision >= 0.70) AND form-free KG agreement via engine.formfree_edge_agreement (note the
  #       known precision-blindness of the magnitude oracle; report precision diagnostic as primary).
  #   If NO profession qualifies: skip set-cover, set professions verdict = 'no_absorption_signature'.
  #
  # ===================================================================================
  # PART 2 — HOMOGRAPH SCAN  (CPU; reuse taxonomic cache)
  # ===================================================================================
  # 2A. Re-run the taxonomic pipeline from the CACHE to regenerate the homograph x absorption-type
  #     cross-tab over all 52 countries (engine.analyze_hierarchy + engine.iter3_extensions, name='taxonomic',
  #     use_cache=True). Confirms absorption_type==True for EXACTLY {Georgia, Jordan} (the iter-4 result),
  #     non-homograph countries (incl. United States) NOT absorption_type. Emit homograph_crosstab cell lists.
  # 2B. Entity-token scan beyond countries: the taxonomic testbed uses country-vs-CITY and country-vs-other-
  #     proper-noun negative families, so CITY / proper-noun surface tokens are present in x_off + corpus-neg
  #     rows. Group corpus rows by surface token (metadata_target_text on negatives / city gazetteer), and for
  #     any entity surface with >= N_MIN_ELIGIBLE occurrences test the SAME signature (a general parent latent
  #     for that entity-type with recall-hole>0.5 AND a specialist with firing-Jaccard<0.1). Report each
  #     qualifying entity with its set-cover result, OR honestly that the scan surfaced NONE beyond Georgia/Jordan.
  #     (Expected: none — the testbed has per-country labels but not per-city labels, so this is a best-effort
  #      scan; log the coverage limitation explicitly so 'no new case' is not over-read as exhaustive.)
  #
  # ===================================================================================
  # PART 3 — JORDAN BESIDE GEORGIA  (CPU; reuse taxonomic cache + iter-4 numbers)
  # ===================================================================================
  # Build ONE side_by_side table from the Part-2 taxonomic re-run:
  #   row Georgia: n_pos(150), eligible=True, absorption_type=True, parent_hole(~0.80), firing_jaccard(~0.059),
  #                unit_AUC(~0.995), AUC-diff CIs vs S_rec/S_prec/S_mag/RE-k-anch/g/h/dense, set_cover_established=True
  #   row Jordan:  n_pos(124), eligible=False (DESCRIPTIVE <150), absorption_type=True, parent_hole(~0.71),
  #                firing_jaccard, unit_AUC + AUC-diff CIs, set_cover_established (report value), status='descriptive'
  #   row United States: firing_jaccard(~0.20), absorption_type=False (co-firing/splitting, NOT absorption), n_pos
  #   Annotate: affirmative non-spelling set-cover evidence is currently ONE eligible slice (Georgia),
  #   1-2 counting descriptive Jordan; US is co-firing not absorption.
  #
  # ===================================================================================
  # STEP 4 — VERDICT + EMIT
  # ===================================================================================
  #   second_case_found := (any qualifying profession with set_cover_established) OR (any new homograph entity
  #                         with set_cover_established).
  #   verdict = 'second_case_found' if second_case_found else 'absorption_remains_narrow'
  #     ('absorption is narrow / specific to suppressed-parent homograph polysemy; the profession is-a
  #       hierarchy shows uniform-high parent recall = NO absorption' — the publishable honest negative).
  #   Emit method_out.json (engine.emit_method_out signature) with:
  #     metadata.per_family = {
  #        professions: {hole_table(all 28), parent_latent, anchor_recall, eligible_professions,
  #                      qualifying_professions, setcover (per qualifying: members, edges, auc_point,
  #                      auc_diff_ci, set_cover_established, setcover_corroborated, kg_agreement),
  #                      negative_regime_notes, gender_secondary, professions_verdict},
  #        taxonomic: {homograph_crosstab, homograph_scan, side_by_side(Georgia/Jordan/US)} },
  #     metadata.verdict, metadata.sae(release/sae_id/width/hook/layer/d_model), metadata.stats,
  #     metadata.thresholds, metadata.encoding(per-family fvu/meanL0/cached), metadata.runtime_s,
  #     metadata.honest_negatives (verbatim list incl. profession boundary-null, scan coverage limit, n=1-2).
  #   datasets = [{dataset:'professions', examples: per-bio held-out predictions predict_{unit,anchor,g,h,
  #                dense_probe,rek,S_rec,S_prec,S_mag} + metadata_sub_context(profession)+gender},
  #               {dataset:'taxonomic_sidebyside', examples: per-row predictions for Georgia/Jordan/US slices}].
  #   Run aii-json: validate method_out.json against exp_gen_sol_out; generate mini_/preview_method_out.json;
  #     ensure each < 100MB (cap examples to ~6-8k held-out rows like engine.make_predictions max_rows; if the
  #     full file exceeds 100MB, follow aii-file-size-limit to split).
  #
  # DELIVERABLES: engine.py (copied+adapted method), profession_absorption.py (Part 1 driver), method_out.json +
  #   full/mini/preview_method_out.json, results/*.csv (hole_table, side_by_side, homograph_crosstab,
  #   per-prof auc_diff), cache/lat_bias_*.npz, RESULTS_SUMMARY.md.
fallback_plan: |-
  COMPUTE / ENCODING FALLBACKS (Part 1 is the only GPU-dependent part):
    (a) GPU non-functional (sm_120/5090 'no kernel image'): engine.py already probes CUDA and CPU-falls-back, but ENCODING needs a working device. First retry relies on the gpu-profile fallback ladder (A4000/L4/4090 = sm_86/89 work with standard torch). If still broken, install a cu128 nightly torch matching sm_120; if that fails, subsample bios to ~6k (>=200/profession for the top ~20 professions) and mean-pool-encode on CPU (slow but bounded; ~1-2h). Document the subsample in metadata.
    (b) Encoding OOM / slow: drop BATCH to 8, MAXLEN to 192 (bios rarely exceed), free hidden_states each batch (engine already does), checkpoint the CSR every ~2k rows so a crash resumes from cache.

  SCIENCE FALLBACKS (each is itself a publishable result, consistent with the boundary-null framing):
    (c) NO general 'occupation' parent latent exists (no precision-passing high-recall latent across professions): report 'the profession is-a hierarchy has no suppressed general parent' -> absorption test VOID for professions (a finding: the phenomenon needs a token-level general parent, which professions lack). Still emit the discriminative-latent table + the dense-probe AUC so the section is non-empty.
    (d) Uniform high parent recall, no profession hole > 0.5 (the EXPECTED boundary-null): this is the primary honest-negative SUCCESS path -> verdict='absorption_remains_narrow', emit the full 28-row hole table as the evidence. Do NOT treat this as failure.
    (e) A profession shows a hole but NO mutually-exclusive specialist (firing-Jaccard>=0.1 everywhere = co-firing/splitting, like United States): report it as 'splitting not absorption', not a second case.
    (f) A profession qualifies the signature but the unit does NOT beat S-rec/S-prec/S-mag (CIs include 0): report set_cover_established=False -> 'eligibility+pooling, not set-cover-specific selection' (the numeric-integer outcome analog).
    (g) Genre confound suspected (parent keys on bio-vs-review not occupation): rely on the one-vs-rest WITHIN-bios AUC (genre-matched) as primary and DOWNWEIGHT the non-bio-negative result; report both and flag the confound.
    (h) Homograph entity scan surfaces nothing (likely, given per-city labels are absent): report 'no new homograph case beyond Georgia/Jordan; scan limited by available per-entity labels' — honest and expected.
    (i) If Part 1 cannot run at all (no compute), still deliver Parts 2-3 (CPU cache reuse) = the homograph cross-tab + Jordan-beside-Georgia table, and mark professions 'not_run_compute'. This is a degraded but non-empty deliverable; avoid this path if any GPU is obtainable.

  OVERALL: the artifact SUCCEEDS whether it finds a second case OR honestly concludes absorption is narrow; the failure mode to avoid is an un-interpretable/empty result. Always emit the full hole table + side-by-side table with CIs.
testing_plan: |-
  Gradual scaling with confirmation signals at each rung (aii-long-running-tasks pattern):
    1. ENGINE WIRING (CPU, seconds, no model): run the copied engine in --scale smoke against the COPIED taxonomic cache. It must reproduce the iter-4 invariants: anchor latent==3792, gated unit contains Georgia specialist 16009 and NOT low-precision 4697, Georgia held-out subctx precision >= 0.70. This confirms the cache copy + reused functions are intact BEFORE touching professions.
    2. SAE/POOLING SANITY (GPU, ~1 min): encode 32 bios (2 professions) with the new whole-text pooling. Assert FVU < 0.6 (SAE/layer pipeline correct), meanL0 in (1, width*0.5), and that >0 tokens were selected per bio (no all-dropped rows). Print 3 example bios + their top firing latents (logit-lens sanity that an 'occupation'-ish latent appears).
    3. PARENT/HOLE SMOKE (GPU, ~3-5 min): encode ~2,000 bios (4 professions incl. a likely-distinct one e.g. nurse/surgeon/attorney/poet) + 1,000 negatives. Run parent identification + the per-profession hole table on this mini set. Confirm: an anchor is found with recall>0.6 + firing-floor>5%; the hole table is populated for all 4; the S-rec/S-prec/S-mag selectors + RE-k baselines + AUC-diff CIs execute without shape errors. Eyeball whether any hole>0.5 appears.
    4. PART 2/3 SMOKE (CPU, ~5 min): full taxonomic re-run from cache; assert the homograph cross-tab yields exactly {Georgia, Jordan} absorption_type==True and the side-by-side table has Georgia(eligible)/Jordan(descriptive n=124)/US(co-firing) rows with AUC-diff CIs present.
    5. FULL RUN: encode the full (or capped ~12-16k) bios + 5k negatives; run all three parts; B_auc>=10,000, B_draws=1000. Watch logs for: encode FVU/meanL0 per family, anchor recall + firing-floor, count of professions with absorption_type, any set_cover_established, and the final verdict line.
    6. OUTPUT VALIDATION: aii-json validate method_out.json vs exp_gen_sol_out; generate + validate mini/preview; confirm each file < 100MB (split per aii-file-size-limit if needed). Spot-check that per-row predict_* fields are present and the hole_table has all 28 professions.
  CONFIRMATION SIGNALS before trusting the full run: smoke invariants pass (rung 1), FVU<0.6 on bios (rung 2), hole table populated + CIs computed (rung 3), Georgia/Jordan cross-tab reproduced (rung 4). If rung-1 invariants fail, the cache copy or function reuse is broken — fix before proceeding. If FVU>=0.6 on bios, the layer/pooling is wrong — re-check determine_layer_idx and the whole-text position selection.
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
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
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

--- Dependency 4 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
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

### [2] HUMAN-USER prompt · 2026-06-18 02:12:06 UTC

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

### [3] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:12:18 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:12:18 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-18 02:14:14 UTC

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

### [6] SYSTEM-USER prompt · 2026-06-18 03:10:32 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_4/results/out.json`
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
id: gen_plan_experiment_4_idx4
type: experiment
title: >-
  M7 — Second Polysemy/Absorption Case Beyond Georgia: Profession Is-A Hierarchy + Homograph Scan + Jordan-Beside-Georgia
summary: >-
  Search for >=1 additional suppressed-parent absorption case to corroborate the non-spelling set-cover-selection result that
  is currently effectively n=1 (Georgia), 1-2 with descriptive Jordan. Three parts on the FROZEN Gemma-2-2b / Gemma-Scope
  layer_12/width_16k JumpReLU SAE: (1) NEW corpus-only test of a SECOND is-a hierarchy = bias_in_bios professions (general
  'occupation' parent suppressed on specific professions), GPU-encoded fresh; (2) HOMOGRAPH SCAN re-running the country cross-tab
  + entity-token scan on the CACHED taxonomic encodings (CPU); (3) JORDAN-BESIDE-GEORGIA side-by-side selection table with
  n + eligibility. Reuse the iter-4 precision-gated K-track + selectors + AUC-diff machinery verbatim where possible. The
  EXPECTED, fully-publishable outcome is an honest negative ('absorption is narrow / specific to homograph-polysemy, not a
  general is-a-hierarchy phenomenon'); a positive second case strengthens the paper. Emit method_out.json (exp_gen_sol_out
  schema) with full hole tables, set-cover results with CIs, the side-by-side table, a 'second-case-found' vs 'absorption-remains-narrow'
  verdict, and per-row diagnostic predictions; validate full/mini/preview < 100MB.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ===================================================================================
  # GOAL (M7): corroborate the non-spelling absorption/set-cover result beyond Georgia.
  # THREE PARTS. Part 1 (professions) is the NEW science and needs GPU encoding (no cache).
  # Parts 2-3 reuse the iter-4 taxonomic CACHE on CPU. Honest negative is the EXPECTED, publishable outcome.
  # ===================================================================================
  #
  # ---- ABSOLUTE PATHS (verified to exist by the planner) ----
  # ITER4_DIR  = /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
  # METHOD_SRC = ITER4_DIR/method.py            # 2108-line engine to COPY+adapt (do not re-derive)
  # TAX_LAT    = ITER4_DIR/cache/lat_taxonomic_w16384_n15748.npz   # cached taxonomic latents (CSR)
  # TAX_RES    = ITER4_DIR/cache/resid_taxonomic_w16384_n15748.npy # cached taxonomic residuals (fp16)
  # TAX_DATA   = .../iter_1/gen_art/gen_art_dataset_2/full_data_out.json   # taxonomic+numeric testbed
  # BIOS_DATA  = .../iter_1/gen_art/gen_art_dataset_4/full_data_out.json   # sentiment+aspect+bias_in_bios
  # DOSSIER_M  = .../iter_1/gen_art/gen_art_research_1/research_out.json    # SAE pipeline/baseline spec
  # DOSSIER_D  = .../iter_1/gen_art/gen_art_research_2/research_out.json    # form-free absorption diagnostic
  #
  # STEP 0 — SCAFFOLD & REUSE ENGINE
  #   * Copy METHOD_SRC into THIS workspace as engine.py; import its functions rather than rewriting:
  #       load_sae, JumpReLUSAE, _find_sae_params, load_model, Encoder (adapted), encode_or_cache,
  #       run_greedy, iter3_extensions, formfree_edge_agreement, admission_check, bootstrap_ci,
  #       paired_diff_ci, fast_auc, _auc_rows, _youden_table, firing_jaccard_pos, holm, match_threshold,
  #       emit_method_out, _json_default, write_figure_csvs.
  #   * Copy the two taxonomic cache files into ./cache/ with IDENTICAL names so engine.encode_or_cache
  #     loads them (it asserts shape (15748,16384)); set CACHE_DIR=./cache. Keep CPU-fallback block intact.
  #   * Pin pyproject deps to the iter-4 versions (torch, numpy, scipy, scikit-learn, statsmodels, loguru,
  #     transformers, huggingface_hub, networkx). Install a torch wheel matching the LANDED GPU arch
  #     (cu124+; the gpu profile may fall back to A4000/L4/4090 = sm_86/89 which standard torch supports;
  #     only the 5090=sm_120 needs a newer wheel — probe CUDA once like engine.py and CPU-fall-back if a
  #     real device op raises).
  #   * Constants reused verbatim: G1_RECALL=0.60, JACCARD_MAX=0.10, SUBCTX_PREC=0.70, GAIN_MIN=0.05,
  #     PRECISION_FLOOR=0.70, N_MIN_ELIGIBLE=150, GREEDY_MAX_MEMBERS=12, SEED=20240617, D_MODEL=2304.
  #
  # ===================================================================================
  # PART 1 — SECOND IS-A HIERARCHY: bias_in_bios PROFESSIONS  (NEW, GPU encode)
  # bias_in_bios rows have NO content pairs and NO target spans -> CORPUS-ONLY adaptation.
  # Framing: parent concept = 'occupation/profession' (general); CHILDREN/sub-contexts = the 28
  # professions; absorption = a general occupation latent that fires on most bios but has profession-
  # specific recall HOLES where a mutually-exclusive specialist fires instead.
  # ===================================================================================
  #
  # 1A. LOAD & SUBSAMPLE
  #   bios = [r for r in BIOS_DATA.datasets where dataset name family=='bias_in_bios_boundary']
  #       each row: input=bio text, output=profession (e.g. 'journalist'), metadata_sub_context={'gender':..},
  #                 metadata_concept_label=profession, metadata_meta.raw_profession_int (0..27).
  #   prof = output label; gender = sub_context.gender.
  #   Keep ALL 28 professions; flag profession descriptive_only if its TOTAL bios < 2*N_MIN_ELIGIBLE
  #     (need >=150 in the diagnostic fold AFTER a 50/50 split). dataset is gender-balanced ~20,177/28~=720
  #     avg, but skewed -> some rare professions (e.g. rapper/dj/personal_trainer) may fall below.
  #   To bound GPU cost, optionally cap bios per profession at ~600 (stratified by gender, seed 20240617):
  #     total ~ min(20177, 28*600) ~= 12-16k. Record the cap in metadata.
  #
  # 1B. NEGATIVE POOL (for parent precision-gating + dense-probe baseline)
  #   neg_texts = stratified subsample ~5,000 from BIOS_DATA sentiment (movie reviews) + restaurant_aspect
  #     (CEBaB reviews) families — full texts, NON-occupation, SAME corpus file, encoded with IDENTICAL
  #     whole-text pooling so pool SIZE is held fixed (no length confound vs the single-slot taxonomic neg).
  #   CAVEAT to log + guard: a 'parent' could key on genre (bio vs review) not 'occupation'. MITIGATION:
  #     the PRIMARY per-profession AUC is ONE-VS-REST WITHIN bios (positives=prof-p bios, negatives=other-
  #     profession bios) which is genre-matched; non-bio negatives are used ONLY for parent precision-gating
  #     and the dense-probe sanity baseline. Report both negative regimes.
  #
  # 1C. ENCODE (GPU; the ONE expensive step — no cache exists)
  #   * Adapt engine.Encoder: bios have no target span, so add a pooling mode 'whole_text' ->
  #       positions = all tokens with non-zero offset width and attention_mask==1 (exclude BOS/pad).
  #       resid[gid] = mean over those token residuals (fp16); pooled_lat = MAX over those tokens' SAE
  #       latents (firing detector) -> CSR row. (Same max-pool firing rule as the rest of the method.)
  #   * MAXLEN=256 (bio char_len up to ~500 => ~120 tok; covers it). BATCH=16. Validate FVU<0.6, meanL0
  #     plausible (engine asserts). Token-alignment metric is N/A here (no target_text) -> skip that assert.
  #   * Determine layer via engine.determine_layer_idx on a 32-bio sample (expect hidden_states[13]).
  #   * SAVE cache: ./cache/lat_bias_w16384_n{N}.npz, resid_bias_w16384_n{N}.npy (so re-runs are GPU-free).
  #   * Encode neg_texts the SAME way -> lat_neg, resid_neg.
  #
  # 1D. FOLD SPLIT (mirror the method's selection/eval discipline)
  #   Split bios 50/50 train(SELECTION) / diagnostic(HELD-OUT), STRATIFIED by profession (seed 20240617).
  #   Gates, anchor recall, firing-Jaccard, subctx precision, greedy are FIT on SELECTION; AUC / hole table
  #   / router REPORTED on the disjoint HELD-OUT fold.
  #
  # 1E. PARENT (anchor) IDENTIFICATION — corpus-only (no content pairs)
  #   * 'content-responsive'/discriminative latent := firing_rate(bios_sel) - firing_rate(neg) above a
  #     LABEL-SHUFFLE null (shuffle bio/neg labels B=1000, 95th pct), AND content-style precision
  #     prec_l = firing on bios / (firing on bios + firing on neg) >= PRECISION_FLOOR(0.70).
  #   * anchor = among precision-passing discriminative latents, the one with the HIGHEST overall bio-recall
  #     (fraction of ALL selection bios where it max-fires). Firing-floor validation: anchor must fire on
  #     >5% of HELD-OUT bios (drops spurious 0%-corpus anchors, the iter-4 letter-I fix).
  #   * Also fit the dense parent probe d_p: LogisticRegression(class_weight='balanced') on mean-pooled
  #     residuals, bios(+1) vs neg(0), TRAIN fold -> non-SAE baseline direction (engine Phase 4 recipe).
  #
  # 1F. PER-PROFESSION HOLE TABLE (the headline deliverable; reported for ALL 28)
  #   For each profession p (held-out fold):
  #     recall_p   = mean(anchor fires on prof-p bios);  hole_p = 1 - recall_p
  #     specialists_p = latents with one-vs-rest subctx FIRING precision_p >= 0.70 (prof-p vs other-prof bios)
  #                     AND fire on >= GAIN_MIN of prof-p bios.
  #     best_jaccard_p = min over specialists_p of positive-only firing_jaccard(specialist, anchor)
  #     absorption_type_p = (hole_p > 0.5) AND (exists specialist with best_jaccard_p < JACCARD_MAX)
  #     n_p, eligible_p = (n_p >= N_MIN_ELIGIBLE)
  #   Emit hole_table[p] = {n, eligible, parent_recall, parent_hole, best_specialist, best_jaccard,
  #                         n_specialists, absorption_type, gender_split:{male_hole,female_hole}}.
  #   IMPORTANT: a uniform parent_recall~1.0 across professions (NO holes) is the EXPECTED boundary-null and
  #   must be emitted explicitly as 'absorption does not generalize to the profession is-a hierarchy'.
  #
  # 1G. SET-COVER + SELECTION ISOLATION (only for professions with absorption_type==True)
  #   For each qualifying profession q:
  #     * Build per-fold firing matrices over the discriminative/eligible latent pool ELIG (precision>=0.70).
  #     * anchor = parent; HOLES = prof-q bios the anchor misses; run engine.run_greedy variant='gated'
  #       (per-sub-context firing-precision gate + mutual-exclusivity J<0.10 + gain>=0.05 CI>0) AND 'weighted'.
  #     * Build det_scores via engine.iter3_extensions-style logic adapted to ONE-VS-REST (positives=prof-q
  #       held-out bios, negatives=other-profession held-out bios):
  #         unit (max-pool members), anchor, g (top-20 |mean_pos-mean_neg| marginal-attr), h (count-matched),
  #         dense_probe (one-vs-rest LR on residual), RE-k, RE-k-anchored, S_rec (top-k by bio-recall),
  #         S_prec (top-k by subctx precision), S_mag (top-k by mean firing magnitude).
  #     * AUC-diff CIs: stratified paired bootstrap B>=10,000 (resample positives & negatives separately),
  #       reuse engine._auc_rows. set_cover_established_q := unit beats S_rec_anch AND S_prec_anch AND
  #       S_mag_anch AND RE-k-anchored AND g AND h with 95% CI excluding 0 on the prof-q slice.
  #     * setcover_corroborated_q := the greedy-chosen specialist is the precision-diagnostic member (held-out
  #       subctx precision >= 0.70) AND form-free KG agreement via engine.formfree_edge_agreement (note the
  #       known precision-blindness of the magnitude oracle; report precision diagnostic as primary).
  #   If NO profession qualifies: skip set-cover, set professions verdict = 'no_absorption_signature'.
  #
  # ===================================================================================
  # PART 2 — HOMOGRAPH SCAN  (CPU; reuse taxonomic cache)
  # ===================================================================================
  # 2A. Re-run the taxonomic pipeline from the CACHE to regenerate the homograph x absorption-type
  #     cross-tab over all 52 countries (engine.analyze_hierarchy + engine.iter3_extensions, name='taxonomic',
  #     use_cache=True). Confirms absorption_type==True for EXACTLY {Georgia, Jordan} (the iter-4 result),
  #     non-homograph countries (incl. United States) NOT absorption_type. Emit homograph_crosstab cell lists.
  # 2B. Entity-token scan beyond countries: the taxonomic testbed uses country-vs-CITY and country-vs-other-
  #     proper-noun negative families, so CITY / proper-noun surface tokens are present in x_off + corpus-neg
  #     rows. Group corpus rows by surface token (metadata_target_text on negatives / city gazetteer), and for
  #     any entity surface with >= N_MIN_ELIGIBLE occurrences test the SAME signature (a general parent latent
  #     for that entity-type with recall-hole>0.5 AND a specialist with firing-Jaccard<0.1). Report each
  #     qualifying entity with its set-cover result, OR honestly that the scan surfaced NONE beyond Georgia/Jordan.
  #     (Expected: none — the testbed has per-country labels but not per-city labels, so this is a best-effort
  #      scan; log the coverage limitation explicitly so 'no new case' is not over-read as exhaustive.)
  #
  # ===================================================================================
  # PART 3 — JORDAN BESIDE GEORGIA  (CPU; reuse taxonomic cache + iter-4 numbers)
  # ===================================================================================
  # Build ONE side_by_side table from the Part-2 taxonomic re-run:
  #   row Georgia: n_pos(150), eligible=True, absorption_type=True, parent_hole(~0.80), firing_jaccard(~0.059),
  #                unit_AUC(~0.995), AUC-diff CIs vs S_rec/S_prec/S_mag/RE-k-anch/g/h/dense, set_cover_established=True
  #   row Jordan:  n_pos(124), eligible=False (DESCRIPTIVE <150), absorption_type=True, parent_hole(~0.71),
  #                firing_jaccard, unit_AUC + AUC-diff CIs, set_cover_established (report value), status='descriptive'
  #   row United States: firing_jaccard(~0.20), absorption_type=False (co-firing/splitting, NOT absorption), n_pos
  #   Annotate: affirmative non-spelling set-cover evidence is currently ONE eligible slice (Georgia),
  #   1-2 counting descriptive Jordan; US is co-firing not absorption.
  #
  # ===================================================================================
  # STEP 4 — VERDICT + EMIT
  # ===================================================================================
  #   second_case_found := (any qualifying profession with set_cover_established) OR (any new homograph entity
  #                         with set_cover_established).
  #   verdict = 'second_case_found' if second_case_found else 'absorption_remains_narrow'
  #     ('absorption is narrow / specific to suppressed-parent homograph polysemy; the profession is-a
  #       hierarchy shows uniform-high parent recall = NO absorption' — the publishable honest negative).
  #   Emit method_out.json (engine.emit_method_out signature) with:
  #     metadata.per_family = {
  #        professions: {hole_table(all 28), parent_latent, anchor_recall, eligible_professions,
  #                      qualifying_professions, setcover (per qualifying: members, edges, auc_point,
  #                      auc_diff_ci, set_cover_established, setcover_corroborated, kg_agreement),
  #                      negative_regime_notes, gender_secondary, professions_verdict},
  #        taxonomic: {homograph_crosstab, homograph_scan, side_by_side(Georgia/Jordan/US)} },
  #     metadata.verdict, metadata.sae(release/sae_id/width/hook/layer/d_model), metadata.stats,
  #     metadata.thresholds, metadata.encoding(per-family fvu/meanL0/cached), metadata.runtime_s,
  #     metadata.honest_negatives (verbatim list incl. profession boundary-null, scan coverage limit, n=1-2).
  #   datasets = [{dataset:'professions', examples: per-bio held-out predictions predict_{unit,anchor,g,h,
  #                dense_probe,rek,S_rec,S_prec,S_mag} + metadata_sub_context(profession)+gender},
  #               {dataset:'taxonomic_sidebyside', examples: per-row predictions for Georgia/Jordan/US slices}].
  #   Run aii-json: validate method_out.json against exp_gen_sol_out; generate mini_/preview_method_out.json;
  #     ensure each < 100MB (cap examples to ~6-8k held-out rows like engine.make_predictions max_rows; if the
  #     full file exceeds 100MB, follow aii-file-size-limit to split).
  #
  # DELIVERABLES: engine.py (copied+adapted method), profession_absorption.py (Part 1 driver), method_out.json +
  #   full/mini/preview_method_out.json, results/*.csv (hole_table, side_by_side, homograph_crosstab,
  #   per-prof auc_diff), cache/lat_bias_*.npz, RESULTS_SUMMARY.md.
fallback_plan: |-
  COMPUTE / ENCODING FALLBACKS (Part 1 is the only GPU-dependent part):
    (a) GPU non-functional (sm_120/5090 'no kernel image'): engine.py already probes CUDA and CPU-falls-back, but ENCODING needs a working device. First retry relies on the gpu-profile fallback ladder (A4000/L4/4090 = sm_86/89 work with standard torch). If still broken, install a cu128 nightly torch matching sm_120; if that fails, subsample bios to ~6k (>=200/profession for the top ~20 professions) and mean-pool-encode on CPU (slow but bounded; ~1-2h). Document the subsample in metadata.
    (b) Encoding OOM / slow: drop BATCH to 8, MAXLEN to 192 (bios rarely exceed), free hidden_states each batch (engine already does), checkpoint the CSR every ~2k rows so a crash resumes from cache.

  SCIENCE FALLBACKS (each is itself a publishable result, consistent with the boundary-null framing):
    (c) NO general 'occupation' parent latent exists (no precision-passing high-recall latent across professions): report 'the profession is-a hierarchy has no suppressed general parent' -> absorption test VOID for professions (a finding: the phenomenon needs a token-level general parent, which professions lack). Still emit the discriminative-latent table + the dense-probe AUC so the section is non-empty.
    (d) Uniform high parent recall, no profession hole > 0.5 (the EXPECTED boundary-null): this is the primary honest-negative SUCCESS path -> verdict='absorption_remains_narrow', emit the full 28-row hole table as the evidence. Do NOT treat this as failure.
    (e) A profession shows a hole but NO mutually-exclusive specialist (firing-Jaccard>=0.1 everywhere = co-firing/splitting, like United States): report it as 'splitting not absorption', not a second case.
    (f) A profession qualifies the signature but the unit does NOT beat S-rec/S-prec/S-mag (CIs include 0): report set_cover_established=False -> 'eligibility+pooling, not set-cover-specific selection' (the numeric-integer outcome analog).
    (g) Genre confound suspected (parent keys on bio-vs-review not occupation): rely on the one-vs-rest WITHIN-bios AUC (genre-matched) as primary and DOWNWEIGHT the non-bio-negative result; report both and flag the confound.
    (h) Homograph entity scan surfaces nothing (likely, given per-city labels are absent): report 'no new homograph case beyond Georgia/Jordan; scan limited by available per-entity labels' — honest and expected.
    (i) If Part 1 cannot run at all (no compute), still deliver Parts 2-3 (CPU cache reuse) = the homograph cross-tab + Jordan-beside-Georgia table, and mark professions 'not_run_compute'. This is a degraded but non-empty deliverable; avoid this path if any GPU is obtainable.

  OVERALL: the artifact SUCCEEDS whether it finds a second case OR honestly concludes absorption is narrow; the failure mode to avoid is an un-interpretable/empty result. Always emit the full hole table + side-by-side table with CIs.
testing_plan: |-
  Gradual scaling with confirmation signals at each rung (aii-long-running-tasks pattern):
    1. ENGINE WIRING (CPU, seconds, no model): run the copied engine in --scale smoke against the COPIED taxonomic cache. It must reproduce the iter-4 invariants: anchor latent==3792, gated unit contains Georgia specialist 16009 and NOT low-precision 4697, Georgia held-out subctx precision >= 0.70. This confirms the cache copy + reused functions are intact BEFORE touching professions.
    2. SAE/POOLING SANITY (GPU, ~1 min): encode 32 bios (2 professions) with the new whole-text pooling. Assert FVU < 0.6 (SAE/layer pipeline correct), meanL0 in (1, width*0.5), and that >0 tokens were selected per bio (no all-dropped rows). Print 3 example bios + their top firing latents (logit-lens sanity that an 'occupation'-ish latent appears).
    3. PARENT/HOLE SMOKE (GPU, ~3-5 min): encode ~2,000 bios (4 professions incl. a likely-distinct one e.g. nurse/surgeon/attorney/poet) + 1,000 negatives. Run parent identification + the per-profession hole table on this mini set. Confirm: an anchor is found with recall>0.6 + firing-floor>5%; the hole table is populated for all 4; the S-rec/S-prec/S-mag selectors + RE-k baselines + AUC-diff CIs execute without shape errors. Eyeball whether any hole>0.5 appears.
    4. PART 2/3 SMOKE (CPU, ~5 min): full taxonomic re-run from cache; assert the homograph cross-tab yields exactly {Georgia, Jordan} absorption_type==True and the side-by-side table has Georgia(eligible)/Jordan(descriptive n=124)/US(co-firing) rows with AUC-diff CIs present.
    5. FULL RUN: encode the full (or capped ~12-16k) bios + 5k negatives; run all three parts; B_auc>=10,000, B_draws=1000. Watch logs for: encode FVU/meanL0 per family, anchor recall + firing-floor, count of professions with absorption_type, any set_cover_established, and the final verdict line.
    6. OUTPUT VALIDATION: aii-json validate method_out.json vs exp_gen_sol_out; generate + validate mini/preview; confirm each file < 100MB (split per aii-file-size-limit if needed). Spot-check that per-row predict_* fields are present and the hole_table has all 28 professions.
  CONFIRMATION SIGNALS before trusting the full run: smoke invariants pass (rung 1), FVU<0.6 on bios (rung 2), hole table populated + CIs computed (rung 3), Georgia/Jordan cross-tab reproduced (rung 4). If rung-1 invariants fail, the cache copy or function reuse is broken — fix before proceeding. If FVU>=0.6 on bios, the layer/pooling is wrong — re-check determine_layer_idx and the whole-text position selection.
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
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
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

--- Dependency 4 ---
id: art_21JWypIydPMX
type: dataset
title: CCRG supporting sentiment/aspect families + bias_in_bios boundary-null dataset
summary: >-
  Three REAL, human-annotated datasets standardized into the CCRG shared minimal-pair schema and emitted in the canonical
  exp_sel_data_out format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}), ONE example per text
  row, grouped by dataset, $0 LLM spend. Families (separable via metadata_family): (1) sentiment = CAD-IMDB (Kaushik et al.
  ICLR 2020), 4,880 rows / 2,440 human counterfactual content-flip pairs (positive<->negative), supporting; (2) restaurant_aspect
  = CEBaB (Abraham et al. NeurIPS 2022), 5,682 rows / 2,841 pairs (food 1,740 + service 1,101) flipping ONE aspect's sentiment
  with all four aspect majorities (food/service/ambiance/noise) + binarized review_sentiment retained as INDEPENDENT sub_context
  labels, supporting; (3) bias_in_bios_boundary = LabHC/bias_in_bios (De-Arteaga et al. 2019), 20,177 profession bios (28
  classes, gender as independent sub-context), the PRE-REGISTERED boundary-null where habitat~=label. Total 30,739 rows, 5,281
  reconstructable minimal pairs. Per row: input(text), output(canonical label), and metadata_* fields: id, family, dataset_source,
  concept(sentiment|food_sentiment|service_sentiment|profession), concept_label, sub_context(dict), pair_id, partner_id, pair_role(content_on|content_off|null),
  flip_type(content|null), is_content_pair, is_surface_pair(false for all), fold(train|dev|test), meta(raw fields incl char_len,
  token_overlap_with_partner, raw labels, subsample seed). Every (x_off,x_on) content pair is reconstructable via pair_id/partner_id
  (content_on=positive/concept-present member). is_surface_pair=false everywhere — surface flips are out of scope here (reserved
  for sibling ParaDetox/LLM artifacts); no surface pairs fabricated. NO derived statistics (MI/probes) computed — raw standardized
  data only. Every row validated against schema.json (jsonschema Draft7) AND full/mini/preview validated against exp_sel_data_out
  (aii-json). THREE plan errors were caught and corrected by empirical verification: (a) CAD-IMDB orig/<->new/ row alignment
  is FALSE (flip_rate~0.50, aligned Jaccard~=random~0.11) — authoritative pairing taken from the repo's combined/paired/*_paired.tsv
  via shared batch_id (true-pair Jaccard 0.816 vs random 0.108); (b) CEBaB edit_type is the edited ASPECT {food,service,ambiance,noise}
  and edit_goal is the target sentiment (the plan swapped them), and review_majority is a 1-5 star rating (binarized 1,2->neg
  / 4,5->pos / 3->neutral); (c) bias_in_bios ships no ClassLabel names, so the canonical 28-occupation alphabetical mapping
  (incl 'dj' at index 8) was verified empirically 17/17 by keyword hit-rate (nurse=13, attorney=2, surgeon=25, software_engineer=24,
  yoga_teacher=27), gender 0=male/1=female confirmed by pronouns; stratified (profession x gender, 56 strata) capped subsample
  with fixed seed 20240617, gender-balanced (male 10,054 / female 10,123). Licenses: CAD Apache-2.0, CEBaB CC-BY-4.0, bias_in_bios
  MIT. Reproduce all deliverables with `uv run data.py`. Downstream guidance: compute per-family bootstrap CIs as primary
  (families cleanly separated); treat any bias_in_bios null as the expected boundary outcome, not method failure; build content
  (x_off,x_on) deltas from pair_id.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_4
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

### [7] SYSTEM-USER prompt · 2026-06-18 03:12:57 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - cache/lat_bias_w16384_n13843.npz (146.6 MB)

You MUST reduce these files to under 100MB each. Use ONE of these strategies:

=== STRATEGY 1: SPLIT FILES (PREFERRED) ===
Split large files into smaller parts and update code to read them sequentially.

For data files (JSON, JSONL, CSV, Parquet):
1. Split the file into parts under 100MB each:
   - data.jsonl -> data_part_001.jsonl, data_part_002.jsonl, ...
2. Update ALL code that reads this file to handle the split parts
3. Delete the original large file after splitting

=== STRATEGY 2: COMPRESSION (FALLBACK) ===
Only use if splitting is not feasible (e.g., binary files, model weights).

1. Compress the file with gzip
2. Update ALL code to decompress before use
3. Delete the original uncompressed file

=== REQUIRED: UPDATE AND TEST CODE ===
After applying your chosen strategy, you MUST:

1. Find ALL code files that reference the modified files (use grep/search)
2. Update each file to work with the new format (split parts or compressed)
3. Run the updated code to verify it still works correctly
4. Fix any errors that occur until the code runs successfully

Do NOT skip testing - the code must actually execute without errors.

Start by listing the oversized files with `ls -lh`, then apply the appropriate strategy.
</CRITICAL_ERROR>
```

## Task: `gen_art_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:12:06 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/results/out.json`
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
  M2 — Cross-Dictionary Replication of the Auditability Spine on the 65k-Width (and a Second-Layer) Gemma-Scope SAE
summary: >-
  Re-run the headline auditability spine (homograph recall-holes, KG-repair FDR survivors, Georgia/Jordan surgical edits,
  recall-hole/firing-Jaccard router) on the 65k-width canonical Gemma-Scope SAE (layer_12, primary) and, if budget allows,
  one earlier residual layer at width-16k (secondary), on the SAME frozen gemma-2-2b model and the SAME frozen testbeds used
  at iter-4. The single most important difference vs iter-4: latent indices are dictionary-specific, so anchors AND absorbers
  MUST be re-derived on each new dictionary (the 16k IDs Georgia->16009 / Jordan->540,8347 do NOT carry over). Output is a
  per-dictionary replication table with honest deltas vs the 16k counts and a REPLICATES / PARTIAL / DICTIONARY-DEPENDENT
  verdict per piece. A partial replication de-risks generalization; a clean non-replication is itself the publishable dictionary-dependence
  finding the literature predicts (wider SAEs absorb MORE). Core run is $0 LLM (all measurement is model-internal); member-labeling
  is an optional, budget-gated extra.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  GOAL (load-bearing M2): replicate iter-4's auditability spine on >=1 SECOND SAE dictionary of the SAME model (gemma-2-2b). PRIMARY dictionary = width-65k canonical at layer 12; SECONDARY (budget-permitting) = an earlier residual layer (~6-9) at width-16k. Report honest deltas + a REPLICATES/PARTIAL/DICTIONARY-DEPENDENT verdict per spine piece.

  =================== REUSE (copy + adapt; do NOT rewrite from scratch) ===================
  The full spine is ALREADY IMPLEMENTED at iter-4/iter-3 — copy these files into the workspace and parametrize the SAE (release/width/layer):
    R1 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method.py
         -> JumpReLUSAE class, _find_sae_params(), load_sae(), gating check, determine_layer_idx(), select_positions(),
            BROAD K-track KG-repair loop (kg_absorber[X]=argmax recall over content-responsive latents, jaccard<0.10, subctx_prec>=0.70),
            random-latent control + one-sided bootstrap p, Benjamini-Hochberg FDR<=0.05 (hand-rolled + statsmodels crosscheck),
            k_localization_check (JTT), ensemble member-labeling.
    R2 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2/method.py
         -> edit operators KG-ABL (h <- h - lambda*z_l*W_dec[l], gated by latent's own firing), DENSE-ABL (h <- h - beta*(h.u)u, diff-of-means parent erasure = baseline f), RAND, KG-ADD, (k);
            forward_pos_logprobs(), behavioral_curve(), run_case(), next-token-KL on_target/collateral, SURGICAL SELECTIVITY=on_target/collateral, paired bootstrap CI (B=10000) on dense-minus-kg collateral, regime router map.
    R3 = run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py
         -> firing_jaccard(), per-sub-context parent recall-hole (recall_hole=1-parent_recall), derive_1d() threshold sweep, balanced_accuracy(), 2-signal router (jaccard<tau_j AND recall_hole>tau_h), recall_hole_router (tau_h-only).
  Pin deps from the iter-4 pyproject.toml (torch==2.6.0 cu124, transformers, numpy, scipy, statsmodels, scikit-learn, networkx, loguru). Use unsloth/gemma-2-2b mirror fallback if google/gemma-2-2b is gated.

  =================== DATASETS (frozen; same testbeds as iter-4) ===================
    taxonomic + numeric: iter_1/gen_art/gen_art_dataset_2/full_data_out.json (datasets: taxonomic_absorption, numeric_absorption; content_flip pairs, surface_flip pairs, corpus windows; sub_context labels; gemma token indices precomputed).
    spelling L/O/T/I/D:   iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first_letter_spelling_{L,O,T,I,D}; content_flip, surface_flip, corpus_context).
    toxicity (co-firing pole): iter_1/gen_art/gen_art_dataset_3/full_data_out.json (paradetox content_pair, civil_comments classification with frozen sub-context labels insult/obscene/threat/identity_attack/...).
  Flatten datasets[*].examples; filter by metadata_record_type / pair_type / role; reconstruct pairs by shared metadata_pair_id + role(on/off).

  =================== SAE CONFIG (the only thing that changes vs iter-4) ===================
  D_MODEL=2304; gemma-2-2b is 26 layers; hook at blocks.L.hook_resid_post == model.model.layers[L].forward_hook output == hidden_states[L+1].
  DICT-65K (PRIMARY): raw release 'google/gemma-scope-2b-pt-res', path 'layer_12/width_65k/average_l0_72/params.npz'. CANONICAL = avg L0 closest to 100; for layer_12/width_65k the available L0s are {21,38,72,141,297} -> 72 is canonical (VERIFIED on HF tree). Reuse _find_sae_params() but glob 'layer_12/width_65k/average_l0_*/params.npz' and pick min|L0-100|; assert resolved==72 and LOG it. (Equivalent SAELens path: release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_65k/canonical' — both resolve to the same npz; prefer the direct-npz JumpReLUSAE loader for zero new deps.) Expected d_sae=65536, W_enc[2304,65536], W_dec[65536,2304], plus b_enc,b_dec,threshold; firing=encode>0 = (pre>threshold)*relu(pre).
  DICT-L9-16K (SECONDARY): 'layer_9/width_16k/average_l0_*/params.npz' (glob closest-to-100), HOOK_LAYER=9, hidden_states idx=10; set determine_layer_idx to search (8,9,10,11). Earlier layer chosen to contrast L12 and stay inside the strict-diagnostic-valid 0-17 range (form-free diagnostic works at all layers). If layer_9 unavailable pick layer_6.
  GATING: cosine(h, decode(encode(h)))>0.9 measured on TAXONOMIC + SPELLING tokens (the gate is a GLOBAL property of the mapping). EXPECT ~0.90-0.92 at 65k. Record numeric digit-token cosine DESCRIPTIVELY (iter-4 found 16k numeric ~0.8911<0.9); do NOT gate-fail on numeric. If the GLOBAL taxonomic cosine<0.9 at 65k, that is itself a reportable reconstruction-quality delta — log it, demote 65k numeric/spelling to descriptive, continue.
  MEMORY (4x wider dict): W matrices ~1.2GB f32 fine on 20GB. The RISK is materializing dense latent matrices [N_tokens, 65536]. Use aii-use-hardware; chunk encoding (BATCH<=16, MAXLEN<=192); NEVER hold all-token x all-65536 in f32 — either (a) compute per-latent firing/recall statistics streaming over chunks, or (b) keep only the candidate-latent columns needed (anchor + top-K covering latents) as f16. Disk-cache per-(dict,layer,split) encodings under cache/ keyed by SAE id + dataset hash; EXCLUDE cache/ from upload.

  =================== EXECUTION ORDER (gradual scaling; depth-first on the highest-value slice) ===================
  STAGE 0 — SETUP & SMOKE (~10 min): load gemma-2-2b + DICT-65K; run determine_layer_idx on 32 taxonomic rows to confirm hidden_states[13]; assert gating cosine>0.9; assert d_sae==65536. Emit a tiny smoke method_out.json (gating only) and STOP if --smoke.

  STAGE 1 — 65k TAXONOMIC Georgia/Jordan (the minimal load-bearing replication; do FIRST):
    1a. Encode taxonomic content_flip pairs (x_on/x_off) + corpus windows at L12/65k. Per latent l, content-response r_l = a_l(x_on)-a_l(x_off); firing = encode>0 at the target token position (use precomputed token indices / select_positions on offset map).
    1b. RE-DERIVE the parent anchor on 65k: anchor = highest content-flip-recall content-responsive latent, with the UNSUPERVISED FIRING-FLOOR validation (anchor must fire on >= SPURIOUS_FIRE_FLOOR=0.01 of held-out corpus positives; else pick next — this is the iter-4 letter-I fix). Log the new 65k anchor latent id (will differ from 16k 3792).
    1c. (A) ROUTER SIGNALS per country: per-sub-context parent recall-hole = 1 - parent_recall on that country's positives; detector = best per-country latent; positive-only firing-Jaccard(parent,detector) (reuse R3 firing_jaccard). QUESTION: do Georgia & Jordan still satisfy recall_hole>0.5 AND jaccard<0.1? Report hole + jaccard for ALL eligible countries (>=150 diagnostic positives) and flag Jordan's n (iter-4 n=124 descriptive) next to Georgia.
    1d. (B) KG-REPAIR for Georgia & Jordan (and every eligible country): kg_absorber[X]=argmax_{l: content-responsive, l!=anchor, jaccard(l,anchor)<KG_JACCARD_MAX=0.10, subctx_prec(l,X)>=KG_PREC_MIN=0.70} recall_l(X-selection-split). ADD absorber to anchor (max-pool) and MEASURE held-out recall recovery (gain_kg) vs the RANDOM-SINGLE-LATENT control distribution (each other content-responsive latent added singly -> gain distribution); report kg_percentile_vs_random (KG gain exceeds 95th/99th pct), paired-bootstrap CI (B=10000) and one-sided p (H0: kg_gain-random_gain<=0). [M5 wording: control = random SINGLE content-responsive-latent addition, NOT a full-population max-pool.] Use HOLE_RECALL_MAX=0.60 to flag holes; N_MIN_SEL=10/N_MIN_RELAX=15/N_MIN_EVAL=30 floors.
    1e. (C) SURGICAL EDIT for the re-derived Georgia & Jordan absorbers (reuse R2 run_case): KG-ABL the absorber, DENSE-ABL the diff-of-means parent (fit on a DISJOINT diagnostic fold), RAND control, KG-ADD; next-token KL on_target (edited token) vs collateral (sibling-country tokens) over kl_prompts; SURGICAL SELECTIVITY=on_target/collateral at MATCHED on-target; paired-bootstrap CI on (dense_collateral - kg_collateral) must exclude 0 favoring KG; graded verdict (clean surgical: kg collateral not sig>0, footprint<2%, ratio>=20).

  STAGE 2 — 65k SPELLING (L/O/T/I/D) + TOXICITY co-firing pole:
    Spelling: per letter re-derive anchor (firing-floor validated) + per-word absorbers; router signals (recall_hole, jaccard); KG-repair FDR rows; ONE surgical edit on the best-precision letter absorber (iter-4 used 'large'->8463; re-derive the 65k id). Expect letters where 16k held (T/O/L words +1.0) to remain strong.
    Toxicity (NEGATIVE pole, regime contrast): parent=toxic-vs-neutral; sub-attributes insult/obscene/threat/identity_attack. Confirm the co-firing signature PERSISTS at 65k: recall_hole ~0 and firing-Jaccard high (iter-4: insult jaccard 0.878, hole 0.00). Run the insult single-latent ablation -> expect NOT clean (selectivity collapses). This anchors the absorption-vs-co-firing split on the new dictionary.
    Numeric (optional, demotable): repair-FDR rows only; remember digit-token cosine<0.9 (descriptive). iter-4 numeric survivors: date+0.68/ordinal+0.53/decimal+0.45/year+0.35/comma+0.24/currency+0.14, integer tied.

  STAGE 3 — BH FDR ACROSS ALL 65k VARIANTS (one BH family over all concepts, exactly like iter-4): assign bh_q + survives_FDR; hand-rolled BH crosschecked vs statsmodels. Report per-family survivor counts and DELTAS vs 16k counts (16k: homograph-taxonomic 6, numeric 10, spelling 14, over ~23 distinct holes). De-duplicate variants where kg_ktrack and kg_diagnostic name the SAME 65k latent (M3 honest counting); report DISTINCT-hole count as the headline number.

  STAGE 4 — ROUTER THRESHOLD TRANSFER on 65k: recompute recall_hole_max + firing_jaccard_median for the SAME derivation concept set used at iter-3/iter-4. (i) Apply the FROZEN 16k-derived thresholds (tau_h, tau_j) WITHOUT refitting and report balanced-accuracy on 65k. (ii) Re-derive 65k-optimal tau_h (recall-hole-ALONE, lead signal per M6) and tau_j (firing-Jaccard corroborating) via derive_1d; report 65k balanced-acc and whether the 65k thresholds are close to 16k (transfer = frozen 16k thresholds still give high bal-acc on 65k). Lead with recall-hole-alone (iter-4: bal-acc 1.0, no derivation counterexample); firing-Jaccard corroborating.

  STAGE 5 — SECONDARY DICTIONARY (DICT-L9-16K), only if Stages 1-4 land with budget left: repeat the MOST DIAGNOSTIC subset only — Georgia/Jordan router signals (1c) + KG-repair (1d) + surgical edit (1e). This is a second axis (layer) of the same generalization claim.

  STAGE 6 — ASSEMBLE method_out.json (exp_gen_sol_out schema):
    metadata: per-dictionary gating_check (cosine, L0, resolved average_l0, layer_idx, numeric_digit_cosine descriptive); re-derived anchors+absorber latent ids per concept (with the firing-floor validation result); a REPLICATION TABLE per dictionary with one entry per spine piece:
      {dictionary, layer, width,
       homograph_holes: {Georgia:{recall_hole, firing_jaccard, eligible, n}, Jordan:{...}, ...},
       repair_fdr: {per_family_survivors, deltas_vs_16k, distinct_hole_count, example gains+p+bh_q},
       surgical: {per_case selectivity_ratio, kg_collateral, dense_collateral, dense_minus_kg_CI, footprint, verdict, delta_vs_16k},
       router: {tau_h, tau_j, balanced_acc_recall_hole_alone, balanced_acc_combined, frozen_16k_threshold_balanced_acc, transfers:bool},
       regime_split: {absorption_mean_selectivity, cofiring_mean_selectivity}}
    PER-PIECE VERDICT logic: REPLICATES if (Georgia&Jordan holes reappear: recall_hole>0.5 & jaccard<0.1) AND (>=1 repair per replicated family survives FDR) AND (surgical selectivity ratio>=20 with dense-kg collateral CI>0) AND (router frozen-16k thresholds still bal-acc>=0.8). PARTIAL if some pieces hold and others don't (state which). DICTIONARY-DEPENDENT if holes vanish / repairs die / selectivity collapses (report as the honest, publishable wider-SAE-absorbs-more finding). Also an OVERALL verdict {cross_dictionary_replicates: full|partial|dictionary_dependent}.
    datasets: a 'cross_dictionary_replication' dataset with ONE exp_gen_sol_out example per (dictionary x piece x sub_context): input=concept/sub-context descriptor; output=verdict label or numeric prediction; metadata_* = dictionary, layer, width, recall_hole, firing_jaccard, gain_kg, one_sided_p, bh_q, survives_FDR, selectivity_ratio, dense_minus_kg_collateral, delta_vs_16k. These per-row predictions feed downstream evaluation.
    Validate with aii-json; run aii-file-size-limit; ensure full/mini/preview_method_out.json each <100MB (drop per-token arrays into cache/, keep summaries in JSON). EXCLUDE cache/ from upload.

  COST: core spine = $0 LLM (KL, recall, selectivity, router all model-internal). OPTIONAL member-labeling (M7) on 65k members uses anthropic/claude-haiku-4.5 J=3 (~$0.2, hard stop $10) — run ONLY if Stages 1-5 finish early; otherwise skip (not in the M2 headline spine).
fallback_plan: |-
  TRIAGE / DROP ORDER (first dropped first), so a clean load-bearing replication always ships: optional member-labeling -> second layer (Stage 5) -> 65k numeric -> 65k toxicity -> 65k spelling letters beyond one -> down to the NEVER-DROP minimum = 65k taxonomic Georgia/Jordan router-signals + KG-repair + surgical edit (Stage 1) with a verdict. Always emit a verdict for whatever completed.

  OOM on the 4x-wider dict: lower BATCH to 8 and MAXLEN to 128; store latents as float16; do NOT materialize [N,65536] dense — switch to streaming per-latent firing/recall accumulation over chunks, or restrict to the candidate-latent columns (anchor + top-K coverers). If still tight, subsample corpus windows to ~1000/concept and content-flip pairs to the dataset's inferential floor (>=150 positives/sub-context). The W matrices themselves (~1.2GB) are never the problem.

  params.npz / model download: 'google/gemma-scope-2b-pt-res' is the open Gemma-Scope repo (use HF_TOKEN if prompted); for the gated gemma-2-2b fall back to unsloth/gemma-2-2b mirror (vocab 256000), exactly as iter-4. Use HF_HUB_OFFLINE=1 after first cache to skip the ~140s metadata check.

  65k gating cosine<=0.9 on taxonomic tokens: first re-check the hidden_states index via determine_layer_idx over (11,12,13,14) — wrong-layer mapping is the usual cause. If the global mapping genuinely reconstructs <0.9, that is a REPORTABLE reconstruction-quality delta: demote affected families to descriptive and continue (do not abort the whole run).

  Re-derived 65k anchor is spurious (fires ~0% on corpus, the letter-I-1227 failure mode): apply SPURIOUS_FIRE_FLOOR=0.01 firing-floor validation and take the next-highest-recall validated latent; if no validated anchor exists for a concept, mark that concept 'anchor-invalid at 65k' (an honest dictionary-dependence datum), skip its repair/surgical, keep it in the report.

  No precision>=0.70 absorber found for Georgia/Jordan at 65k (wider SAE may split the country across many lower-precision specialists, or absorb it differently): this is the KEY dictionary-dependence outcome the literature predicts (wider->more absorption/more fragmentation). Report it explicitly: record the best available absorber with its precision/jaccard, mark repair/surgical as NON-REPLICATED, and write the verdict as DICTIONARY-DEPENDENT for that piece. Do NOT force a low-precision absorber to manufacture a positive.

  Surgical selectivity collapses at 65k even though a clean absorber exists: report the ratio + CI honestly; if dense-minus-kg collateral CI includes 0, that piece is PARTIAL/non-replicated. A genuine failure of the surgical replication is publishable.

  Router thresholds don't transfer (frozen 16k tau give low bal-acc on 65k): report both frozen-16k and re-fit-65k thresholds and the gap; conclude 'router thresholds are dictionary-specific' — still an honest M2 finding. Lead with recall-hole-alone either way.

  Time exhausted mid-stage: write whatever method_out.json exists with completed pieces + explicit 'not_run' flags for the rest, so the artifact is always valid and downstream can read partial replication.
testing_plan: |-
  1) IMPORT/LOAD smoke (`python method.py --smoke`, ~5-10 min): load gemma-2-2b (or unsloth mirror) + DICT-65K via the JumpReLUSAE npz loader; ASSERT resolved average_l0==72, d_sae==65536, d_model==2304; run determine_layer_idx on 32 taxonomic rows and CONFIRM best hidden_states idx==13; ASSERT gating cosine>0.9 on a small taxonomic+spelling batch. Print numeric digit-token cosine descriptively. If any assert fails, fix loader/layer mapping BEFORE proceeding. Emit a tiny gating-only method_out.json and exit.

  2) MINI pilot (`--families taxonomic --cap 40 --kl_prompts 16`, ~20-30 min): on 65k taxonomic only, RE-DERIVE the parent anchor (confirm it fires >1% on corpus, i.e. not spurious) and the Georgia absorber (confirm jaccard(absorber,anchor)<0.10 and subctx_precision>=0.70 on a held-out fold). Run ONE Georgia surgical edit and confirm KG collateral << DENSE collateral and selectivity ratio is large (directionally matching 16k's Georgia ~1722x/hole~0.8). CONFIRMATION SIGNALS to gate the full run: (a) gating passes; (b) re-derived Georgia anchor non-spurious; (c) Georgia recall_hole>0.5 & jaccard<0.1; (d) Georgia repair gain_kg>0 exceeding the random-single-latent 95th pct; (e) Georgia surgical dense-minus-kg collateral CI>0. If (c)-(e) FAIL on mini, that is the dictionary-dependence signal — still scale up to characterize it fully (don't abort), but flag it early.

  3) NUMERICAL cross-checks: hand-rolled BH q-values matched against statsmodels.stats.multitest.multipletests(method='fdr_bh') (as iter-4 did); paired bootstrap CIs reproducible under fixed SEED=1234; firing_jaccard and recall_hole recomputed on a 16k slice to confirm the copied R3 functions reproduce iter-3/iter-4 numbers before trusting them on 65k.

  4) GUARDRAILS during scaling (use aii-long-running-tasks staged pattern): run as `uv run method.py & PID=$!`; monitor logs/run.log by PID only; checkpoint after each stage (Stage1->Stage2->...) so a crash keeps completed pieces. Watch GPU memory after first 65k encode chunk; if >16GB, trigger the float16/streaming fallback before full-scale encode.

  5) FINAL validation: aii-json validate method_out.json against exp_gen_sol_out; aii-file-size-limit on full/mini/preview (<100MB each, split or push per-token arrays to cache/ if over); confirm cache/ is excluded from upload; sanity-read the replication table + per-piece verdicts for internal consistency (e.g. a piece marked REPLICATES must have its CI/threshold conditions actually satisfied in the row data).
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
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
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

--- Dependency 4 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
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

--- Dependency 5 ---
id: art_8QO7pl6Pd8UQ
type: dataset
title: 'Two-Track CCRG Toxicity Family: ParaDetox flips + civil_comments sub-contexts'
summary: >-
  A single schema-standardized TOXICITY dataset family for the Two-Track CCRG experiments (organizing SAE latents into reliable
  group-level units). 37,707 examples in the exp_sel_data_out schema, grouped into the two real source corpora and validated.
  THE BEST 2 DATASETS are the dataset groups: (1) paradetox = s-nlp/paradetox (Logacheva et al., ACL 2022; openrail++), 19,096
  rows; (2) civil_comments = google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0), 18,611 rows. Three
  role-distinct components are carried via metadata_record_type: (a) content_pair (18,853) = human toxic<->neutral parallel
  sentences, the NON-CIRCULAR content perturbation P (metadata_text_on / metadata_text_off) for per-latent content-response;
  (b) surface_pair (546) = OpenRouter gpt-4o-mini toxic->toxic paraphrases (input / metadata_text_paired), double-gated (token
  Jaccard<0.6 AND norm edit-dist>0.25 AND LLM-judge toxicity_preserved+meaning_preserved; judge pass 70.6%, refusal 1.5%,
  cost $0.060), the surface-invariance control, folded into their seed corpus's group via metadata_origin_source; (c) classification
  (18,308) = civil_comments comments with a binary metadata_toxicity_label plus FROZEN multi-label sub-context labels (severe_toxicity,
  obscene, threat, insult, identity_attack, sexual_explicit) thresholded at 0.5 from the raw annotator-fraction floats (preserved
  in metadata_subcontext_floats for re-thresholding). Power: obscene/threat/insult/identity_attack/sexual_explicit are inferential@0.5
  with >=150 positives in every eval fold; severe_toxicity is flagged descriptive_only (too rare even at 0.3) -- not silently
  dropped. data_summary.json reports per-sub-context per-fold counts at 0.5 and 0.3, the sub-attribute pairwise Jaccard co-occurrence
  matrix (insult<->obscene ~0.245 shared-support => C-track; threat/identity_attack <0.05 disjoint => K-track), generation
  stats, and 316 reconciled cross-source collisions. Leakage-safe doc-level folds (metadata_fold in train/val/test) via union-find
  over normalized text: civil_comments keeps native splits; verified 0 pair_id and 0 source_sentence_id spanning folds and
  0 normalized texts in >1 fold. Sanity baselines (TF-IDF+logistic regression, train->test): toxicity AUC 0.851/F1 0.773;
  sub-contexts AUC 0.81-0.94; content_pair mean cos 0.685 (genuine flip), surface_pair 0.355 (reworded not copied). Files:
  data.py (stdlib-only uv assembler), full/mini/preview_data_out.json (validated), data_summary.json, README.md, pyproject.toml
  (47 pinned deps), and build/ (staged pipeline: ParaDetox content-flips, civil_comments stream-filter, OpenRouter surface
  generation, assembler, verify_baseline). Downstream consumers flatten datasets[*].examples and filter metadata_record_type.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
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

### [2] HUMAN-USER prompt · 2026-06-18 02:12:06 UTC

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

### [3] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:12:38 UTC

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

### [4] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:12:38 UTC

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

### [5] SYSTEM-USER prompt · 2026-06-18 03:33:33 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_2/results/out.json`
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
  M2 — Cross-Dictionary Replication of the Auditability Spine on the 65k-Width (and a Second-Layer) Gemma-Scope SAE
summary: >-
  Re-run the headline auditability spine (homograph recall-holes, KG-repair FDR survivors, Georgia/Jordan surgical edits,
  recall-hole/firing-Jaccard router) on the 65k-width canonical Gemma-Scope SAE (layer_12, primary) and, if budget allows,
  one earlier residual layer at width-16k (secondary), on the SAME frozen gemma-2-2b model and the SAME frozen testbeds used
  at iter-4. The single most important difference vs iter-4: latent indices are dictionary-specific, so anchors AND absorbers
  MUST be re-derived on each new dictionary (the 16k IDs Georgia->16009 / Jordan->540,8347 do NOT carry over). Output is a
  per-dictionary replication table with honest deltas vs the 16k counts and a REPLICATES / PARTIAL / DICTIONARY-DEPENDENT
  verdict per piece. A partial replication de-risks generalization; a clean non-replication is itself the publishable dictionary-dependence
  finding the literature predicts (wider SAEs absorb MORE). Core run is $0 LLM (all measurement is model-internal); member-labeling
  is an optional, budget-gated extra.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  GOAL (load-bearing M2): replicate iter-4's auditability spine on >=1 SECOND SAE dictionary of the SAME model (gemma-2-2b). PRIMARY dictionary = width-65k canonical at layer 12; SECONDARY (budget-permitting) = an earlier residual layer (~6-9) at width-16k. Report honest deltas + a REPLICATES/PARTIAL/DICTIONARY-DEPENDENT verdict per spine piece.

  =================== REUSE (copy + adapt; do NOT rewrite from scratch) ===================
  The full spine is ALREADY IMPLEMENTED at iter-4/iter-3 — copy these files into the workspace and parametrize the SAE (release/width/layer):
    R1 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/method.py
         -> JumpReLUSAE class, _find_sae_params(), load_sae(), gating check, determine_layer_idx(), select_positions(),
            BROAD K-track KG-repair loop (kg_absorber[X]=argmax recall over content-responsive latents, jaccard<0.10, subctx_prec>=0.70),
            random-latent control + one-sided bootstrap p, Benjamini-Hochberg FDR<=0.05 (hand-rolled + statsmodels crosscheck),
            k_localization_check (JTT), ensemble member-labeling.
    R2 = run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_experiment_2/method.py
         -> edit operators KG-ABL (h <- h - lambda*z_l*W_dec[l], gated by latent's own firing), DENSE-ABL (h <- h - beta*(h.u)u, diff-of-means parent erasure = baseline f), RAND, KG-ADD, (k);
            forward_pos_logprobs(), behavioral_curve(), run_case(), next-token-KL on_target/collateral, SURGICAL SELECTIVITY=on_target/collateral, paired bootstrap CI (B=10000) on dense-minus-kg collateral, regime router map.
    R3 = run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_experiment_4/method.py
         -> firing_jaccard(), per-sub-context parent recall-hole (recall_hole=1-parent_recall), derive_1d() threshold sweep, balanced_accuracy(), 2-signal router (jaccard<tau_j AND recall_hole>tau_h), recall_hole_router (tau_h-only).
  Pin deps from the iter-4 pyproject.toml (torch==2.6.0 cu124, transformers, numpy, scipy, statsmodels, scikit-learn, networkx, loguru). Use unsloth/gemma-2-2b mirror fallback if google/gemma-2-2b is gated.

  =================== DATASETS (frozen; same testbeds as iter-4) ===================
    taxonomic + numeric: iter_1/gen_art/gen_art_dataset_2/full_data_out.json (datasets: taxonomic_absorption, numeric_absorption; content_flip pairs, surface_flip pairs, corpus windows; sub_context labels; gemma token indices precomputed).
    spelling L/O/T/I/D:   iter_1/gen_art/gen_art_dataset_1/full_data_out.json (first_letter_spelling_{L,O,T,I,D}; content_flip, surface_flip, corpus_context).
    toxicity (co-firing pole): iter_1/gen_art/gen_art_dataset_3/full_data_out.json (paradetox content_pair, civil_comments classification with frozen sub-context labels insult/obscene/threat/identity_attack/...).
  Flatten datasets[*].examples; filter by metadata_record_type / pair_type / role; reconstruct pairs by shared metadata_pair_id + role(on/off).

  =================== SAE CONFIG (the only thing that changes vs iter-4) ===================
  D_MODEL=2304; gemma-2-2b is 26 layers; hook at blocks.L.hook_resid_post == model.model.layers[L].forward_hook output == hidden_states[L+1].
  DICT-65K (PRIMARY): raw release 'google/gemma-scope-2b-pt-res', path 'layer_12/width_65k/average_l0_72/params.npz'. CANONICAL = avg L0 closest to 100; for layer_12/width_65k the available L0s are {21,38,72,141,297} -> 72 is canonical (VERIFIED on HF tree). Reuse _find_sae_params() but glob 'layer_12/width_65k/average_l0_*/params.npz' and pick min|L0-100|; assert resolved==72 and LOG it. (Equivalent SAELens path: release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_65k/canonical' — both resolve to the same npz; prefer the direct-npz JumpReLUSAE loader for zero new deps.) Expected d_sae=65536, W_enc[2304,65536], W_dec[65536,2304], plus b_enc,b_dec,threshold; firing=encode>0 = (pre>threshold)*relu(pre).
  DICT-L9-16K (SECONDARY): 'layer_9/width_16k/average_l0_*/params.npz' (glob closest-to-100), HOOK_LAYER=9, hidden_states idx=10; set determine_layer_idx to search (8,9,10,11). Earlier layer chosen to contrast L12 and stay inside the strict-diagnostic-valid 0-17 range (form-free diagnostic works at all layers). If layer_9 unavailable pick layer_6.
  GATING: cosine(h, decode(encode(h)))>0.9 measured on TAXONOMIC + SPELLING tokens (the gate is a GLOBAL property of the mapping). EXPECT ~0.90-0.92 at 65k. Record numeric digit-token cosine DESCRIPTIVELY (iter-4 found 16k numeric ~0.8911<0.9); do NOT gate-fail on numeric. If the GLOBAL taxonomic cosine<0.9 at 65k, that is itself a reportable reconstruction-quality delta — log it, demote 65k numeric/spelling to descriptive, continue.
  MEMORY (4x wider dict): W matrices ~1.2GB f32 fine on 20GB. The RISK is materializing dense latent matrices [N_tokens, 65536]. Use aii-use-hardware; chunk encoding (BATCH<=16, MAXLEN<=192); NEVER hold all-token x all-65536 in f32 — either (a) compute per-latent firing/recall statistics streaming over chunks, or (b) keep only the candidate-latent columns needed (anchor + top-K covering latents) as f16. Disk-cache per-(dict,layer,split) encodings under cache/ keyed by SAE id + dataset hash; EXCLUDE cache/ from upload.

  =================== EXECUTION ORDER (gradual scaling; depth-first on the highest-value slice) ===================
  STAGE 0 — SETUP & SMOKE (~10 min): load gemma-2-2b + DICT-65K; run determine_layer_idx on 32 taxonomic rows to confirm hidden_states[13]; assert gating cosine>0.9; assert d_sae==65536. Emit a tiny smoke method_out.json (gating only) and STOP if --smoke.

  STAGE 1 — 65k TAXONOMIC Georgia/Jordan (the minimal load-bearing replication; do FIRST):
    1a. Encode taxonomic content_flip pairs (x_on/x_off) + corpus windows at L12/65k. Per latent l, content-response r_l = a_l(x_on)-a_l(x_off); firing = encode>0 at the target token position (use precomputed token indices / select_positions on offset map).
    1b. RE-DERIVE the parent anchor on 65k: anchor = highest content-flip-recall content-responsive latent, with the UNSUPERVISED FIRING-FLOOR validation (anchor must fire on >= SPURIOUS_FIRE_FLOOR=0.01 of held-out corpus positives; else pick next — this is the iter-4 letter-I fix). Log the new 65k anchor latent id (will differ from 16k 3792).
    1c. (A) ROUTER SIGNALS per country: per-sub-context parent recall-hole = 1 - parent_recall on that country's positives; detector = best per-country latent; positive-only firing-Jaccard(parent,detector) (reuse R3 firing_jaccard). QUESTION: do Georgia & Jordan still satisfy recall_hole>0.5 AND jaccard<0.1? Report hole + jaccard for ALL eligible countries (>=150 diagnostic positives) and flag Jordan's n (iter-4 n=124 descriptive) next to Georgia.
    1d. (B) KG-REPAIR for Georgia & Jordan (and every eligible country): kg_absorber[X]=argmax_{l: content-responsive, l!=anchor, jaccard(l,anchor)<KG_JACCARD_MAX=0.10, subctx_prec(l,X)>=KG_PREC_MIN=0.70} recall_l(X-selection-split). ADD absorber to anchor (max-pool) and MEASURE held-out recall recovery (gain_kg) vs the RANDOM-SINGLE-LATENT control distribution (each other content-responsive latent added singly -> gain distribution); report kg_percentile_vs_random (KG gain exceeds 95th/99th pct), paired-bootstrap CI (B=10000) and one-sided p (H0: kg_gain-random_gain<=0). [M5 wording: control = random SINGLE content-responsive-latent addition, NOT a full-population max-pool.] Use HOLE_RECALL_MAX=0.60 to flag holes; N_MIN_SEL=10/N_MIN_RELAX=15/N_MIN_EVAL=30 floors.
    1e. (C) SURGICAL EDIT for the re-derived Georgia & Jordan absorbers (reuse R2 run_case): KG-ABL the absorber, DENSE-ABL the diff-of-means parent (fit on a DISJOINT diagnostic fold), RAND control, KG-ADD; next-token KL on_target (edited token) vs collateral (sibling-country tokens) over kl_prompts; SURGICAL SELECTIVITY=on_target/collateral at MATCHED on-target; paired-bootstrap CI on (dense_collateral - kg_collateral) must exclude 0 favoring KG; graded verdict (clean surgical: kg collateral not sig>0, footprint<2%, ratio>=20).

  STAGE 2 — 65k SPELLING (L/O/T/I/D) + TOXICITY co-firing pole:
    Spelling: per letter re-derive anchor (firing-floor validated) + per-word absorbers; router signals (recall_hole, jaccard); KG-repair FDR rows; ONE surgical edit on the best-precision letter absorber (iter-4 used 'large'->8463; re-derive the 65k id). Expect letters where 16k held (T/O/L words +1.0) to remain strong.
    Toxicity (NEGATIVE pole, regime contrast): parent=toxic-vs-neutral; sub-attributes insult/obscene/threat/identity_attack. Confirm the co-firing signature PERSISTS at 65k: recall_hole ~0 and firing-Jaccard high (iter-4: insult jaccard 0.878, hole 0.00). Run the insult single-latent ablation -> expect NOT clean (selectivity collapses). This anchors the absorption-vs-co-firing split on the new dictionary.
    Numeric (optional, demotable): repair-FDR rows only; remember digit-token cosine<0.9 (descriptive). iter-4 numeric survivors: date+0.68/ordinal+0.53/decimal+0.45/year+0.35/comma+0.24/currency+0.14, integer tied.

  STAGE 3 — BH FDR ACROSS ALL 65k VARIANTS (one BH family over all concepts, exactly like iter-4): assign bh_q + survives_FDR; hand-rolled BH crosschecked vs statsmodels. Report per-family survivor counts and DELTAS vs 16k counts (16k: homograph-taxonomic 6, numeric 10, spelling 14, over ~23 distinct holes). De-duplicate variants where kg_ktrack and kg_diagnostic name the SAME 65k latent (M3 honest counting); report DISTINCT-hole count as the headline number.

  STAGE 4 — ROUTER THRESHOLD TRANSFER on 65k: recompute recall_hole_max + firing_jaccard_median for the SAME derivation concept set used at iter-3/iter-4. (i) Apply the FROZEN 16k-derived thresholds (tau_h, tau_j) WITHOUT refitting and report balanced-accuracy on 65k. (ii) Re-derive 65k-optimal tau_h (recall-hole-ALONE, lead signal per M6) and tau_j (firing-Jaccard corroborating) via derive_1d; report 65k balanced-acc and whether the 65k thresholds are close to 16k (transfer = frozen 16k thresholds still give high bal-acc on 65k). Lead with recall-hole-alone (iter-4: bal-acc 1.0, no derivation counterexample); firing-Jaccard corroborating.

  STAGE 5 — SECONDARY DICTIONARY (DICT-L9-16K), only if Stages 1-4 land with budget left: repeat the MOST DIAGNOSTIC subset only — Georgia/Jordan router signals (1c) + KG-repair (1d) + surgical edit (1e). This is a second axis (layer) of the same generalization claim.

  STAGE 6 — ASSEMBLE method_out.json (exp_gen_sol_out schema):
    metadata: per-dictionary gating_check (cosine, L0, resolved average_l0, layer_idx, numeric_digit_cosine descriptive); re-derived anchors+absorber latent ids per concept (with the firing-floor validation result); a REPLICATION TABLE per dictionary with one entry per spine piece:
      {dictionary, layer, width,
       homograph_holes: {Georgia:{recall_hole, firing_jaccard, eligible, n}, Jordan:{...}, ...},
       repair_fdr: {per_family_survivors, deltas_vs_16k, distinct_hole_count, example gains+p+bh_q},
       surgical: {per_case selectivity_ratio, kg_collateral, dense_collateral, dense_minus_kg_CI, footprint, verdict, delta_vs_16k},
       router: {tau_h, tau_j, balanced_acc_recall_hole_alone, balanced_acc_combined, frozen_16k_threshold_balanced_acc, transfers:bool},
       regime_split: {absorption_mean_selectivity, cofiring_mean_selectivity}}
    PER-PIECE VERDICT logic: REPLICATES if (Georgia&Jordan holes reappear: recall_hole>0.5 & jaccard<0.1) AND (>=1 repair per replicated family survives FDR) AND (surgical selectivity ratio>=20 with dense-kg collateral CI>0) AND (router frozen-16k thresholds still bal-acc>=0.8). PARTIAL if some pieces hold and others don't (state which). DICTIONARY-DEPENDENT if holes vanish / repairs die / selectivity collapses (report as the honest, publishable wider-SAE-absorbs-more finding). Also an OVERALL verdict {cross_dictionary_replicates: full|partial|dictionary_dependent}.
    datasets: a 'cross_dictionary_replication' dataset with ONE exp_gen_sol_out example per (dictionary x piece x sub_context): input=concept/sub-context descriptor; output=verdict label or numeric prediction; metadata_* = dictionary, layer, width, recall_hole, firing_jaccard, gain_kg, one_sided_p, bh_q, survives_FDR, selectivity_ratio, dense_minus_kg_collateral, delta_vs_16k. These per-row predictions feed downstream evaluation.
    Validate with aii-json; run aii-file-size-limit; ensure full/mini/preview_method_out.json each <100MB (drop per-token arrays into cache/, keep summaries in JSON). EXCLUDE cache/ from upload.

  COST: core spine = $0 LLM (KL, recall, selectivity, router all model-internal). OPTIONAL member-labeling (M7) on 65k members uses anthropic/claude-haiku-4.5 J=3 (~$0.2, hard stop $10) — run ONLY if Stages 1-5 finish early; otherwise skip (not in the M2 headline spine).
fallback_plan: |-
  TRIAGE / DROP ORDER (first dropped first), so a clean load-bearing replication always ships: optional member-labeling -> second layer (Stage 5) -> 65k numeric -> 65k toxicity -> 65k spelling letters beyond one -> down to the NEVER-DROP minimum = 65k taxonomic Georgia/Jordan router-signals + KG-repair + surgical edit (Stage 1) with a verdict. Always emit a verdict for whatever completed.

  OOM on the 4x-wider dict: lower BATCH to 8 and MAXLEN to 128; store latents as float16; do NOT materialize [N,65536] dense — switch to streaming per-latent firing/recall accumulation over chunks, or restrict to the candidate-latent columns (anchor + top-K coverers). If still tight, subsample corpus windows to ~1000/concept and content-flip pairs to the dataset's inferential floor (>=150 positives/sub-context). The W matrices themselves (~1.2GB) are never the problem.

  params.npz / model download: 'google/gemma-scope-2b-pt-res' is the open Gemma-Scope repo (use HF_TOKEN if prompted); for the gated gemma-2-2b fall back to unsloth/gemma-2-2b mirror (vocab 256000), exactly as iter-4. Use HF_HUB_OFFLINE=1 after first cache to skip the ~140s metadata check.

  65k gating cosine<=0.9 on taxonomic tokens: first re-check the hidden_states index via determine_layer_idx over (11,12,13,14) — wrong-layer mapping is the usual cause. If the global mapping genuinely reconstructs <0.9, that is a REPORTABLE reconstruction-quality delta: demote affected families to descriptive and continue (do not abort the whole run).

  Re-derived 65k anchor is spurious (fires ~0% on corpus, the letter-I-1227 failure mode): apply SPURIOUS_FIRE_FLOOR=0.01 firing-floor validation and take the next-highest-recall validated latent; if no validated anchor exists for a concept, mark that concept 'anchor-invalid at 65k' (an honest dictionary-dependence datum), skip its repair/surgical, keep it in the report.

  No precision>=0.70 absorber found for Georgia/Jordan at 65k (wider SAE may split the country across many lower-precision specialists, or absorb it differently): this is the KEY dictionary-dependence outcome the literature predicts (wider->more absorption/more fragmentation). Report it explicitly: record the best available absorber with its precision/jaccard, mark repair/surgical as NON-REPLICATED, and write the verdict as DICTIONARY-DEPENDENT for that piece. Do NOT force a low-precision absorber to manufacture a positive.

  Surgical selectivity collapses at 65k even though a clean absorber exists: report the ratio + CI honestly; if dense-minus-kg collateral CI includes 0, that piece is PARTIAL/non-replicated. A genuine failure of the surgical replication is publishable.

  Router thresholds don't transfer (frozen 16k tau give low bal-acc on 65k): report both frozen-16k and re-fit-65k thresholds and the gap; conclude 'router thresholds are dictionary-specific' — still an honest M2 finding. Lead with recall-hole-alone either way.

  Time exhausted mid-stage: write whatever method_out.json exists with completed pieces + explicit 'not_run' flags for the rest, so the artifact is always valid and downstream can read partial replication.
testing_plan: |-
  1) IMPORT/LOAD smoke (`python method.py --smoke`, ~5-10 min): load gemma-2-2b (or unsloth mirror) + DICT-65K via the JumpReLUSAE npz loader; ASSERT resolved average_l0==72, d_sae==65536, d_model==2304; run determine_layer_idx on 32 taxonomic rows and CONFIRM best hidden_states idx==13; ASSERT gating cosine>0.9 on a small taxonomic+spelling batch. Print numeric digit-token cosine descriptively. If any assert fails, fix loader/layer mapping BEFORE proceeding. Emit a tiny gating-only method_out.json and exit.

  2) MINI pilot (`--families taxonomic --cap 40 --kl_prompts 16`, ~20-30 min): on 65k taxonomic only, RE-DERIVE the parent anchor (confirm it fires >1% on corpus, i.e. not spurious) and the Georgia absorber (confirm jaccard(absorber,anchor)<0.10 and subctx_precision>=0.70 on a held-out fold). Run ONE Georgia surgical edit and confirm KG collateral << DENSE collateral and selectivity ratio is large (directionally matching 16k's Georgia ~1722x/hole~0.8). CONFIRMATION SIGNALS to gate the full run: (a) gating passes; (b) re-derived Georgia anchor non-spurious; (c) Georgia recall_hole>0.5 & jaccard<0.1; (d) Georgia repair gain_kg>0 exceeding the random-single-latent 95th pct; (e) Georgia surgical dense-minus-kg collateral CI>0. If (c)-(e) FAIL on mini, that is the dictionary-dependence signal — still scale up to characterize it fully (don't abort), but flag it early.

  3) NUMERICAL cross-checks: hand-rolled BH q-values matched against statsmodels.stats.multitest.multipletests(method='fdr_bh') (as iter-4 did); paired bootstrap CIs reproducible under fixed SEED=1234; firing_jaccard and recall_hole recomputed on a 16k slice to confirm the copied R3 functions reproduce iter-3/iter-4 numbers before trusting them on 65k.

  4) GUARDRAILS during scaling (use aii-long-running-tasks staged pattern): run as `uv run method.py & PID=$!`; monitor logs/run.log by PID only; checkpoint after each stage (Stage1->Stage2->...) so a crash keeps completed pieces. Watch GPU memory after first 65k encode chunk; if >16GB, trigger the float16/streaming fallback before full-scale encode.

  5) FINAL validation: aii-json validate method_out.json against exp_gen_sol_out; aii-file-size-limit on full/mini/preview (<100MB each, split or push per-token arrays to cache/ if over); confirm cache/ is excluded from upload; sanity-read the replication table + per-piece verdicts for internal consistency (e.g. a piece marked REPLICATES must have its CI/threshold conditions actually satisfied in the row data).
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
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
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

--- Dependency 4 ---
id: art_t2uUbjSwpd3t
type: dataset
title: 'Non-Spelling SAE Absorption Testbed: Numeric & Taxonomic Hierarchies'
summary: |-
  TEXT-ONLY dataset (no SAE/model/activation computation here) for testing whether SAE feature absorption — documented almost exclusively on first-letter spelling — generalizes to two NON-spelling parent concepts. It is the never-dropped C3-spine testbed for the Counterfactual Co-Response Grouping hypothesis. Output is the AII exp_sel_data_out schema (one example per data row; per-row metadata flattened to metadata_* keys, since nested objects are disallowed), grouped into exactly two datasets:
  • numeric_absorption (8,380 examples): parent = 'token is numeric (a digit / part of a number)'; absorber sub-contexts = year, percent, currency, date, decimal, integer, comma_number, ordinal (year/percent/currency/date are the primary candidates).
  • taxonomic_absorption (15,748 examples): parent = 'token is part of a country name'; absorber sub-contexts = individual countries.

  Each hierarchy ships three coordinated components: (A) content-flip minimal pairs — x_on contains the concept, x_off a surface-matched non-concept word at the same slot (taxonomic uses country-vs-city and country-vs-other-proper-noun negative families); (B) surface-flip pairs — same concept token in two different carrier sentences, for the unit-level surface-invariance admission check; (C) a frozen pile-uncopyrighted (rev 3be90335b66f24456a5d6659d9c8d208c0357119) diagnostic corpus of real natural-text windows labelled by frozen sub-context, plus matched negatives (no-digit, city-mention, no-country), so iter-2 can train a parent linear probe and run the per-sub-context false-negative (parent-hole) search.

  Every row marks the exact target span (target_text + char_start/char_end) and carries precomputed google/gemma-2-2b token indices (100% coverage; the tokenizer splits numbers into individual digit tokens). Sub-context labels are assigned purely from surface form / regex / gazetteer (pycountry + geonamescache) — independent of any SAE latent or model behaviour — so the degenerate-construction guard holds and the same labelled corpus equally supports the honest 'absorption is spelling-specific' null (uniform high parent-probe recall across sub-contexts). Frozen folds (seed 20240617): pairs split train/test 70/30 by pair_id (stratified by sub_context); corpus splits train/diagnostic 50/50 (stratified). absorption_readiness in manifest.json: ALL 8 numeric sub-contexts and 20 countries reach ≥150 diagnostic-fold positives (eligible for the inferential test); rarer sub-contexts/countries are kept and flagged descriptive_only. Content-flip (≥240) and surface-flip (≥120) per-hierarchy floors are exceeded. A deterministic templated backbone is supplemented by openai/gpt-4o-mini generation, with every content/surface pair (LLM-generated + 20% templated spot-check) LLM-judged on content_flipped/surface_preserved/grammatical — 100% pass at $0.0104 total spend (hard cap $4, ceiling $10). Ambiguous homographs (Georgia, Turkey, Chile, Jordan) and multi-word countries are flagged via metadata_notes / metadata_multi_token.

  Deliverables: data.py (canonical builder), pipeline.py + build_dataset.py (logic modules), full/mini/preview_data_out.json, schema.json (JSON Schema + logical nested view), manifest.json (per-sub-context counts, fold counts, pass rates, spend, pile revision, readiness), and pyproject.toml with pinned dependency versions. Reproduce with `python3 data.py --scale full`. iter-2 consumes this to run the Tier-0 non-triviality pre-check (does a high-recall parent latent exist AND have specialist-filled holes?), the form-free absorption diagnostic as oracle, and the K-track anchored greedy set-cover proposal step — with numeric as the primary novelty test and taxonomic as the pre-registered alternative.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2
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

--- Dependency 5 ---
id: art_8QO7pl6Pd8UQ
type: dataset
title: 'Two-Track CCRG Toxicity Family: ParaDetox flips + civil_comments sub-contexts'
summary: >-
  A single schema-standardized TOXICITY dataset family for the Two-Track CCRG experiments (organizing SAE latents into reliable
  group-level units). 37,707 examples in the exp_sel_data_out schema, grouped into the two real source corpora and validated.
  THE BEST 2 DATASETS are the dataset groups: (1) paradetox = s-nlp/paradetox (Logacheva et al., ACL 2022; openrail++), 19,096
  rows; (2) civil_comments = google/civil_comments (Jigsaw Unintended Bias, Borkan et al. 2019; CC0 1.0), 18,611 rows. Three
  role-distinct components are carried via metadata_record_type: (a) content_pair (18,853) = human toxic<->neutral parallel
  sentences, the NON-CIRCULAR content perturbation P (metadata_text_on / metadata_text_off) for per-latent content-response;
  (b) surface_pair (546) = OpenRouter gpt-4o-mini toxic->toxic paraphrases (input / metadata_text_paired), double-gated (token
  Jaccard<0.6 AND norm edit-dist>0.25 AND LLM-judge toxicity_preserved+meaning_preserved; judge pass 70.6%, refusal 1.5%,
  cost $0.060), the surface-invariance control, folded into their seed corpus's group via metadata_origin_source; (c) classification
  (18,308) = civil_comments comments with a binary metadata_toxicity_label plus FROZEN multi-label sub-context labels (severe_toxicity,
  obscene, threat, insult, identity_attack, sexual_explicit) thresholded at 0.5 from the raw annotator-fraction floats (preserved
  in metadata_subcontext_floats for re-thresholding). Power: obscene/threat/insult/identity_attack/sexual_explicit are inferential@0.5
  with >=150 positives in every eval fold; severe_toxicity is flagged descriptive_only (too rare even at 0.3) -- not silently
  dropped. data_summary.json reports per-sub-context per-fold counts at 0.5 and 0.3, the sub-attribute pairwise Jaccard co-occurrence
  matrix (insult<->obscene ~0.245 shared-support => C-track; threat/identity_attack <0.05 disjoint => K-track), generation
  stats, and 316 reconciled cross-source collisions. Leakage-safe doc-level folds (metadata_fold in train/val/test) via union-find
  over normalized text: civil_comments keeps native splits; verified 0 pair_id and 0 source_sentence_id spanning folds and
  0 normalized texts in >1 fold. Sanity baselines (TF-IDF+logistic regression, train->test): toxicity AUC 0.851/F1 0.773;
  sub-contexts AUC 0.81-0.94; content_pair mean cos 0.685 (genuine flip), surface_pair 0.355 (reworded not copied). Files:
  data.py (stdlib-only uv assembler), full/mini/preview_data_out.json (validated), data_summary.json, README.md, pyproject.toml
  (47 pinned deps), and build/ (staged pipeline: ParaDetox content-flips, civil_comments stream-filter, OpenRouter surface
  generation, assembler, verify_baseline). Downstream consumers flatten datasets[*].examples and filter metadata_record_type.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_3
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

### [6] SYSTEM-USER prompt · 2026-06-18 03:35:54 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - cache/enc_65k_layer_12_width_65k_average_l0_72_tox_cap400_4800_ws1_bbcfc809ad48.npz (106.2 MB)

You MUST reduce these files to under 100MB each. Use ONE of these strategies:

=== STRATEGY 1: SPLIT FILES (PREFERRED) ===
Split large files into smaller parts and update code to read them sequentially.

For data files (JSON, JSONL, CSV, Parquet):
1. Split the file into parts under 100MB each:
   - data.jsonl -> data_part_001.jsonl, data_part_002.jsonl, ...
2. Update ALL code that reads this file to handle the split parts
3. Delete the original large file after splitting

=== STRATEGY 2: COMPRESSION (FALLBACK) ===
Only use if splitting is not feasible (e.g., binary files, model weights).

1. Compress the file with gzip
2. Update ALL code to decompress before use
3. Delete the original uncompressed file

=== REQUIRED: UPDATE AND TEST CODE ===
After applying your chosen strategy, you MUST:

1. Find ALL code files that reference the modified files (use grep/search)
2. Update each file to work with the new format (split parts or compressed)
3. Run the updated code to verify it still works correctly
4. Fix any errors that occur until the code runs successfully

Do NOT skip testing - the code must actually execute without errors.

Start by listing the oversized files with `ls -lh`, then apply the appropriate strategy.
</CRITICAL_ERROR>
```

## Task: `gen_art_experiment_3` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:12:10 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 53674 chars total]
```

### [2] HUMAN-USER prompt · 2026-06-18 02:12:10 UTC

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

### [3] SKILL-INPUT — aii-json · 2026-06-18 02:32:40 UTC

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

### [4] SYSTEM-USER prompt · 2026-06-18 02:40:19 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3/`:
... [truncated, 53616 chars total]
```

### [5] SYSTEM-USER prompt · 2026-06-18 02:43:02 UTC

```
<task-notification>
<task-id>bc7o3elt3</task-id>
<summary>Monitor event: "full run: FROZEN thresholds + key milestones + errors"</summary>
<event>2026-06-18 02:42:56.921 | INFO     | __main__:gating_check:308 - GATING recon_cos_mean=0.9269 recon_cos_min=0.4453 L0 mean=170.2 median=70</event>
</task-notification>
```

### [6] SYSTEM-USER prompt · 2026-06-18 02:44:15 UTC

```
<validation-feedback>
Attempt 2 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [7] SYSTEM-USER prompt · 2026-06-18 02:45:43 UTC

```
<validation-feedback>
Attempt 3 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [8] SYSTEM-USER prompt · 2026-06-18 02:48:06 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 59593 chars total]
```

### [9] HUMAN-USER prompt · 2026-06-18 02:48:06 UTC

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

### [10] SYSTEM-USER prompt · 2026-06-18 02:59:58 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_experiment_3/`:
... [truncated, 53616 chars total]
```

### [11] SYSTEM-USER prompt · 2026-06-18 03:05:16 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:26:06 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_research_1/results/out.json`
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
id: art_i-tkvFCKneA-
type: research
title: >-
  CCRG Citation Audit: Chanin NeurIPS-2025 Fix, Muchane Resolved, Winnicki Contrast
summary: >-
  Closes the iteration-3 M8 novelty/citation minors for the two-track CCRG paper (pure web research). THREE DELIVERABLES.
  (A) A drop-in Winnicki-2026 contrast: arXiv:2604.23829 (Winnicki, Gnanasekaran, Darve; Stanford ICME; arXiv preprint, no
  venue) builds feature-level KG edges PURELY OBSERVATIONALLY (corpus co-occurrence graph weighted by Jaccard over binary
  presence matrices + transcoder cross-layer mechanism graph of source->target sparse latent pathways); a full-text grep finds
  ZERO occurrences of 'interventional/counterfactual/intervention', so it provably cannot draw CCRG's interventional anchor-205
  -> absorber-3069('list') edge (firing-Jaccard<0.1, never co-fire) nor the taxonomic 3792 -> Georgia/Jordan edges (diagnostic
  KG-agreement 0.318 vs 0.002 null; Jordan 0.99). 2-3 sentence + long paragraph versions provided. (B) Corrected citation
  table. CRITICAL FIX: Chanin 'A is for Absorption' (2409.14507) = NeurIPS 2025 ORAL (Dec 4 2025; forum R73ybUciQF; 6 authors
  incl. Golechha), NOT the dossier's 'NeurIPS 2024' (which is the separate NeurIPS-2024 Workshop version, forum Wzav8fesTL,
  5 authors, '...in Spelling Tasks'). Muchane2025 RESOLVES to arXiv:2506.01197 (Muchane/Richardson/Park/Veitch) -- no removal
  needed. Benchmark audit 2605.18229 is SOLE-authored by David Chanin (key 'Chanin2026' VALID). SASA 2606.06333 confirmed
  (Dalili & Mahdavi). AxBench 2501.17148 = ICML 2025 (not ICLR); SAEBench 2503.09532 = ICML 2025; CanonicalUnits 2502.04878
  = ICLR 2025; MindTheGAP 2403.09869 = AISTATS 2024. DPE 2505.23027 and SCR/TPP 2411.18895 have NO venue in arXiv metadata
  -> cite as preprints. SparseCoactivation 2506.18141 title is now '...Causal Semantic Modules...' (was 'Composable'). Full
  table + corrections diff + BibTeX in research_report.md. (C) Three-axis novelty confirmation -- interventional co-response
  grouping, set-cover-for-SAE-grouping, a-priori firing-structure router -- ALL HOLD, with cite-and-distinguish one-liners
  for the four near-misses (Winnicki 2604.23829; Deng 2506.18141 observational coactivation; CDLC 2505.07073 vision/diffusion
  analog; Kantamneni 2502.16681 post-hoc, not a-priori). Outputs: research_out.json {answer, sources(19), follow_up_questions(5)}
  + research_report.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 2 ---
id: art_QBxBPF-9Ldxe
type: research
title: >-
  CCRG iter-4: Homograph-Absorption Novelty, KG-Surgical-Edit Distinctness, Locked Citations
summary: >-
  Finalizes positioning + citations for the auditability-first CCRG (Counterfactual Co-Response Grouping) paper, building
  on the iter-3 audit (art_i-tkvFCKneA-) without re-doing settled entries. FOUR deliverables (pure web research, $0): (A)
  Homograph/polysemy absorption framing = NOVEL: documented feature absorption is empirically first-letter-spelling-only (Chanin
  2409.14507 'short'/'starts-with-S'; SAEBench 2503.09532 absorption metric is built on Chanin's first-letter task) and mechanistically
  tied to sparsity+hierarchy+dictionary-size (Chanin; Matryoshka 2503.17547), NOT to homograph/polysemous tokens with a suppressed
  parent on a semantic hierarchy. The key near-miss PS-Eval (Minegishi et al., 2501.06254, ICLR 2025) evaluates SAE word-SENSE
  separation and a full-text grep finds it NEVER mentions absorption/recall-hole/router/spelling/suppressed-parent (only hit
  = JumpReLU 'suppresses small activations'). Provides short+long positioning paragraphs + a one-line PS-Eval cite-and-distinguish;
  framing guardrail = 'absorption recurs on polysemous tokens, predicted by the recall-hole signal' NOT 'broad taxonomic generalization'.
  (B) KG-localized single-absorber surgical sub-concept edit = DISTINCT: no SAE/LLM steering/erasure method edits a single
  absorber latent NAMED by an interventional feature-KG edge to change/recover ONE sub-context while preserving the parent,
  measured as recall-recovery vs random-addition control + side-effect KL. SAE-TS (2411.02193) and SRS (2503.16851) select
  a CONCEPT feature (effect-approximator / contrastive-KL) with a coefficient; SALVE (2512.15938) is VISION (ResNet-18/ViT-B/16);
  LEACE (2306.03819, NeurIPS 2023) is dense whole-concept erasure that cannot localize to a sub-context; SAeUron/SAEmnesia/SNCE
  are text-to-image DIFFUSION erasure (modality distinguisher). AxBench (2501.17148, ICML 2025) is the side-effect/fluency
  LLM-judge eval bar AND the honest concession (diff-of-means beats SAEs on aggregate steering) -> CCRG scopes the edit as
  an auditability DEMONSTRATION. Cite-and-distinguish table + M1 positioning paragraph + honest-scope note provided. (C) Locked
  2025/2026 citation table: PS-Eval=ICLR2025; SALVE=ICLR2026 Trustworthy-AI Workshop(vision); SAE-TS=arXiv2024; SRS=arXiv2025;
  LEACE=NeurIPS2023; SAeUron=ICML2025(diffusion); SAEmnesia/SNCE=2025 preprints(diffusion). TWO upgrades vs iter-3: DPE 2505.23027
  -> ICML 2025 (poster 43937/OpenReview qUTiOeM57J); SCR/TPP 2411.18895 -> NeurIPS 2024 ATTRIB Workshop. BibTeX block + corrections
  diff + unresolved flags (SAEmnesia/SNCE author lists to verify at bib-time; do not invent). (D) Presentation-strip checklist
  for GEN_PAPER_TEXT (strip iteration/rebuttal/infra scaffolding; move SAE-IDs/seeds/env to appendix; lead with measured auditability;
  dedicated honest-negatives subsection; use locked table). Outputs research_out.json {title, summary, answer, 23 sources,
  4 follow_ups} + research_report.md (sections A-D with drop-in paragraphs, full table, BibTeX, checklist). Both novelty claims
  HOLD; adversarial disprove-searches found no precedent.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_research_1
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
id: gen_plan_research_1_idx6
type: research
title: >-
  M1 Selective-Unlearning + M2 Cross-Dictionary Positioning and Locked Citations for the Auditability-First CCRG Paper
summary: >-
  Pure web-research plan (no code, $0) that POSITIONS the two new iteration-5 results of the Counterfactual Co-Response Grouping
  (CCRG) paper against the right literatures and FINALIZES the citation/venue table for GEN_PAPER_TEXT. Workstream 1 positions
  M1 (a KG-named single-absorber edit that BEATS a dense diff-of-means/erasure baseline on a joint on-target/collateral/fluency
  metric) against the machine-unlearning-with-utility-preservation and selective/targeted concept-removal literature (SAE-unlearning:
  Farrell/Lau/Conmy 2410.19278; CRISP; Conditional-SAE-Clamping; SAUCE; SRMU; the framing-threat 'Use SAEs to Discover Unknown
  Concepts, Not to Act on Known Concepts' 2506.23845; benchmarks WMDP/TOFU/MUSE/RWKU; SHRED Pareto frontier; survey 2601.13264)
  plus the already-settled steering/erasure side-effect bar (AxBench/SAE-TS/SRS/LEACE). Workstream 2 positions M2 (cross-dictionary
  replication on 65k-width and/or a second layer) against the documented width/dictionary-size/layer dependence of absorption
  (SAEBench 2503.09532 'absorption increases with width', Chanin 2409.14507, Matryoshka 2503.17547, Feature Hedging 2505.11756),
  so a replicate-or-dictionary-dependence result lands as a literature-predicted test. Workstream 3 carries forward all iter-3/iter-4
  venue locks verbatim, adds the new M1/M2 cites with verified IDs/venues/authors (flagging unresolved author lists, never
  inventing), and emits a corrected BibTeX-ready table + corrections diff + a presentation-strip checklist. Outputs research_out.json
  {answer, sources, follow_up_questions} + research_report.md with the M1 cite-and-distinguish block, the M2 dictionary-dependence
  framing, the locked table + BibTeX, and the strip checklist.
runpod_compute_profile: cpu_light
question: >-
  How should the iteration-5 CCRG paper POSITION its two new load-bearing results so the next draft frames them correctly
  and novelly, and what is the finalized, venue-locked citation set? Specifically: (M1) Against the machine-unlearning-with-utility-preservation,
  selective/targeted concept-removal, SAE-feature steering/erasure, and AxBench side-effect/fluency literature, is CCRG's
  claim distinct and correctly framed -- that a KNOWLEDGE-GRAPH-NAMED single ABSORBER edit produces a measurably BETTER selective-editing
  outcome (lower sibling+parent collateral AND preserved fluency at matched on-target / forget-quality) than a dense diff-of-means
  / whole-concept erasure baseline, i.e. a targeted-edit Pareto-dominance in the regime where single-sub-context removal with
  parent preservation is the goal a dense direction structurally over-shoots -- and what is the cite-and-distinguish set plus
  the honest concession (AxBench/Farrell: simple/dense baselines beat SAE methods on AGGREGATE steering/unlearning)? (M2)
  What is the documented evidence that feature absorption depends on SAE dictionary width / dictionary size / layer, so that
  re-running the headline spine on the 65k-width and a second-layer Gemma-Scope SAE is the literature-PREDICTED robustness
  axis, and a replication-OR-dictionary-dependence outcome is a deliberate test rather than an afterthought? (M9) Which 2025/2026
  venues are now locked (carrying forward iter-3/iter-4), which new M1/M2 cites need IDs/venues/authors verified, which author
  lists remain unresolved, and what is the final BibTeX table + presentation-strip checklist for GEN_PAPER_TEXT?
research_plan: |-
  PURE WEB RESEARCH (aii-web-tools: web search -> web fetch -> fetch_grep). NO code, NO downloads, NO compute. Budget $0 (no LLM API calls needed). Compute: cpu_light. Honesty rules throughout: (i) cite-and-distinguish, never assert novelty in a vacuum -- every novelty claim must name the nearest precedent and the one-line differentiator; (ii) NEVER invent a bibliographic field (author, venue, year) -- if unresolved, FLAG it; (iii) every factual claim traceable to a fetched URL; (iv) run an adversarial DISPROVE search for each novelty claim and report the closest hit even if it weakens the claim.

  === STEP 0 -- INGEST PRIOR AUDITS, DO NOT RE-DO SETTLED ENTRIES (~15 min) ===
  Read the two dependency files first:
    - art_QBxBPF-9Ldxe (iter-4): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_4/gen_art/gen_art_research_1/research_out.json AND research_report.md
    - art_i-tkvFCKneA- (iter-3): /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_3/gen_art/gen_art_research_1/research_out.json AND research_report.md
  Extract the CARRY-FORWARD LOCK LIST and treat as SETTLED (do NOT re-verify unless an upgrade is plausible): Chanin 'A is for Absorption' 2409.14507 = NeurIPS 2025 ORAL (forum R73ybUciQF, 6 authors incl. Golechha; the NeurIPS-2024 Workshop variant forum Wzav8fesTL is a DISTINCT '...in Spelling Tasks' 5-author paper); AxBench 2501.17148 = ICML 2025; SAEBench 2503.09532 = ICML 2025; Matryoshka 2503.17547 = ICML 2025; SAeUron 2501.18052 = ICML 2025 (diffusion); DPE 2505.23027 = ICML 2025 (poster 43937); CanonicalUnits 2502.04878 = ICLR 2025; PS-Eval 2501.06254 = ICLR 2025; SALVE 2512.15938 = ICLR 2026 Trustworthy-AI Workshop (VISION); SCR/TPP 2411.18895 = NeurIPS 2024 ATTRIB WORKSHOP (not main proceedings); LEACE 2306.03819 = NeurIPS 2023; Mind-the-GAP 2403.09869 = AISTATS 2024; SAE-TS 2411.02193 = arXiv 2024 preprint; SRS 2503.16851 = arXiv 2025 preprint; Feature Hedging 2505.11756 = arXiv 2025 preprint; Muchane 2506.01197, SASA 2606.06333 (Dalili & Mahdavi), Winnicki 2604.23829, Deng 2506.18141 ('Causal Semantic Modules'), Kantamneni 2502.16681, CDLC 2505.07073, Chanin-benchmark-audit 2605.18229 = preprints; SAEmnesia 2509.21379 + SNCE 2509.21008 = 2025 diffusion preprints with UNVERIFIED author lists (flag, do not invent). Also carry the settled VERDICTS: homograph/polysemy-absorption framing = NOVEL (PS-Eval is the cite-and-distinguish near-miss; framing guardrail = 'absorption recurs on polysemous tokens, predicted by the recall-hole signal,' NOT 'broad taxonomic generalization'); KG-localized surgical sub-concept edit = DISTINCT vs SAE-TS/SRS/SALVE/LEACE/diffusion-erasure-cluster. The NEW work below is what iter-5 adds; everything above is INPUT, not output.

  === STEP 1 -- M1 POSITIONING: SELECTIVE-UNLEARNING / TARGETED-EDIT-BEATS-DENSE (~55 min, the largest NEW block) ===
  The iter-5 pivot: M1 is no longer merely 'a capability a probe lacks' (iter-4 audit B) but a claimed DOWNSTREAM WIN -- the KG-named single-absorber edit achieves LOWER sibling+parent collateral AND BETTER preserved fluency than a dense diff-of-means / whole-concept erasure baseline at MATCHED on-target effect (difference-CI excluding 0), framed as a selective-editing / targeted-UNLEARNING Pareto-dominance in the regime where single-sub-context removal with parent preservation is the goal the dense direction structurally over-shoots. Position this against FOUR literatures the prior audits did NOT cover:

  (1A) SAE-BASED UNLEARNING PRECEDENTS (the direct comparators + the honest concession). Fetch + fetch_grep:
    - Farrell, Lau, Conmy 'Applying sparse autoencoders to unlearn knowledge in language models' arXiv:2410.19278 (OpenReview ZtvRqm6oBu). THE canonical SAE-unlearning paper. Extract verbatim: WMDP-Bio subset, gemma-2b-it / gemma-2-2b-it; finding that 'negative scaling of feature activations is necessary, zero-ablation ineffective'; that multi-feature intervention unlearns multiple topics but with 'similar or larger unwanted side-effects than RMU (Representation Misdirection for Unlearning)'; and the concession 'SAE quality / intervention techniques would need to improve to make SAE-based unlearning comparable to fine-tuning-based techniques.' This paper is BOTH the nearest precedent AND a key honest concession (raw-SAE unlearning >= RMU side-effects). The distinguisher: Farrell ablates whole biology TOPICS via attribution-selected features; CCRG edits ONE KG-NAMED ABSORBER for ONE sub-context while PRESERVING the parent, and claims a WIN only in the single-sub-context-with-parent-preservation regime.
    - CRISP 'Persistent Concept Unlearning via Sparse Autoencoders' arXiv:2508.13650 -- extract method (which SAE features, persistence, utility metric).
    - 'Model Unlearning via Sparse Autoencoder Subspace Guided Projections' (OpenReview MIlqM98o9I; find arXiv id if present) -- SAE-subspace projection unlearning.
    - 'Don't Forget It! Conditional Sparse Autoencoder Clamping Works for Unlearning' arXiv:2503.11127 -- conditional clamping; extract utility-preservation result.
    - 'Feature-Selective Representation Misdirection for Machine Unlearning' (SRMU) arXiv:2512.16297 -- feature-aware directional perturbation preserving benign utility; extract Pareto/utility claim.
    - SAUCE 'Selective Concept Unlearning in Vision-Language Models with Sparse Autoencoders' arXiv:2503.14530 (ICCV 2025) -- the closest 'selective + SAE + concept unlearning' but VISION-LANGUAGE (modality + unit distinguisher); confirm venue ICCV 2025 + that it suppresses a concept while preserving unrelated info, NO KG-named absorber, NO LLM sub-context-with-parent-preservation.
    - 'Use Sparse Autoencoders to Discover Unknown Concepts, Not to Act on Known Concepts' arXiv:2506.23845 -- TREAT AS THE KEY FRAMING-THREAT. Read carefully: it argues SAEs are good for DISCOVERY but NOT for acting on already-known concepts (where dense baselines win). CCRG must rebut/align: CCRG's edit target is DISCOVERED by the two-track grouping + KG (an absorber the practitioner does NOT know a priori), and the WIN is scoped to the selective sub-context regime, not a claim that SAEs beat dense on known whole-concepts. Draft the explicit reconciliation paragraph.
  Deliverable 1A: a cite-and-distinguish table row per paper {paper, what it does, why CCRG's M1 differs} + the Farrell honest-concession sentence.

  (1B) MACHINE-UNLEARNING-WITH-UTILITY-PRESERVATION BENCHMARKS + THE PARETO FRAMING (grounds CCRG's joint metric in established eval conventions). Fetch + fetch_grep:
    - WMDP (Weapons of Mass Destruction Proxy) -- find canonical arXiv id (Li et al. 2403.03218) + venue; the forget-domain / retain-utility split.
    - TOFU (Task of Fictitious Unlearning) -- arXiv 2401.06121 + venue; forget-quality vs model-utility metric.
    - MUSE 'Machine Unlearning Six-Way Evaluation' arXiv:2407.06460 -- the six properties incl. UTILITY PRESERVATION on the retain set; extract the metric definitions.
    - RWKU (Real-World Knowledge Unlearning) -- find id/venue.
    - SHRED 'Retain-Set-Free Unlearning via Self-Distillation with Logit Demotion' arXiv:2605.07482 -- extract its explicit 'new Pareto frontier on the forgetting-utility tradeoff across four LLM unlearning benchmarks' claim; this is the canonical statement of the forget-vs-utility Pareto frame CCRG borrows.
    - Survey 'Unlearning in LLMs: Methods, Evaluation, and Open Challenges' arXiv:2601.13264 -- extract the standard metric triad (forget quality / retain utility / fluency-or-generation-quality) and the 'stubborn forget-utility trade-off' framing.
  Deliverable 1B: a short paragraph mapping CCRG's joint M1 metric (on-target effect <-> forget-quality; sibling+parent collateral <-> retain-utility / neighbor-concept preservation; fluency/LLM-judge <-> AxBench Concept/Instruct/Fluency + unlearning generation-quality) onto these established axes, so the reviewer reads M1 as a Pareto-dominance claim in a recognized evaluation frame, not an ad-hoc metric.

  (1C) STEERING/ERASURE SIDE-EFFECT BAR (mostly carry-forward; re-anchor only the fluency component). Reuse the iter-4 cite-and-distinguish for SAE-TS 2411.02193, SRS 2503.16851, SALVE 2512.15938 (vision), LEACE 2306.03819 (dense whole-concept erasure that CANNOT localize to a sub-context -- the primary dense comparator), and the diffusion-erasure cluster (SAeUron/SAEmnesia/SNCE, modality distinguisher). Re-anchor AxBench 2501.17148 as BOTH the side-effect/fluency LLM-judge protocol (harmonic mean of Concept/Instruct/Fluency, 0/1/2) AND the honest concession (diff-of-means beats SAEs on aggregate steering). Do NOT re-verify their venues (locked); only confirm the LEACE 'dense single hyperplane removes the WHOLE concept direction, structurally cannot localize a sub-context' distinguisher is stated crisply, since LEACE/diff-of-means IS the M1 decisive comparator.

  (1D) DISTINCTNESS + ADVERSARIAL DISPROVE SEARCH. Run targeted searches to find ANY prior method that edits/unlearns a SINGLE SUB-CONCEPT / single word-sense / homograph-sense / sub-context of a concept in an LLM SAE while PRESERVING the parent AND BEATS a dense/diff-of-means baseline on a JOINT collateral+fluency metric. Suggested queries: 'sub-concept unlearning preserve parent concept SAE language model'; 'word sense unlearning beat dense baseline collateral fluency'; 'targeted SAE feature edit lower side-effect than diff-of-means LLM'; 'knowledge graph guided single feature edit unlearning'; 'selective sense disambiguation steering preserve general concept'. Report the closest hit and whether it defeats, weakens, or leaves intact CCRG's M1 novelty. EXPECTED outcome (state explicitly if confirmed): precedents either (i) remove a WHOLE concept/topic (Farrell, LEACE, CRISP), (ii) are vision (SAUCE, SALVE), (iii) select a concept feature by attribution/coefficient not a KG-named absorber (SAE-TS, SRS), or (iv) argue against acting on known concepts (2506.23845) -- so the parent-preserving, KG-named, single-absorber, beat-dense-on-joint-metric claim is DISTINCT. If a genuine precedent IS found, FLAG it loudly and recommend reframing M1 from 'novel win' to 'parity/cite-and-distinguish.'
  Deliverable 1D: M1 positioning paragraph (short 2-3 sentence + long 1-paragraph drop-in versions) + the AxBench/Farrell honest-concession note + a one-line scope guardrail ('the win is claimed only in the single-sub-context-with-parent-preservation regime where dense erasure structurally over-shoots; CCRG does NOT claim to beat dense on aggregate whole-concept steering/unlearning').

  === STEP 2 -- M2 POSITIONING: WIDTH / DICTIONARY-SIZE / LAYER DEPENDENCE OF ABSORPTION (~30 min) ===
  Goal: assemble the literature that PREDICTS cross-dictionary variation in absorption, so re-running the spine on the 65k-width and/or a second layer reads as a deliberate, literature-grounded robustness test, and BOTH outcomes (replicate-with-deltas OR dictionary-dependence) are framed in advance.
  (2A) Quantitative width/size dependence. Fetch + fetch_grep:
    - SAEBench 2503.09532 -- grep for 'absorption' + 'width' to extract the verbatim statement that absorption RATE INCREASES WITH HIGHER SAE WIDTH (and higher sparsity), and the width-sweep design (widths 4k / 16k / 65k; 6 sparsities; layer 8 Pythia-160M + LAYER 12 Gemma-2-2B). This is the single strongest quantitative anchor.
    - Chanin 2409.14507 -- grep for the mechanistic account (absorption from sparsity + hierarchical co-occurrence; how width/sparsity modulate it).
    - Matryoshka 2503.17547 -- grep for absorption tied to dictionary size / nesting / abstraction level (the mitigation line that exists BECAUSE absorption scales with size).
    - Feature Hedging 2505.11756 -- grep for the TWO-SIDED width dependence: absorption WORSE at WIDER SAEs vs hedging WORSE at NARROWER SAEs. (This is the crisp prediction that the 16k->65k move should change absorption, in a known direction.)
    - OPTIONAL corroboration: 'Measuring Sparse Autoencoder Feature Sensitivity' arXiv:2509.23717; 'Toy Models of Feature Absorption in SAEs' (LessWrong) -- only if time permits.
  (2B) Gemma-Scope dictionary availability (feasibility grounding for the experiment, not the experiment itself). Confirm via the Gemma Scope paper / HuggingFace / Neuronpedia docs that public canonical Gemma-2-2b residual-stream SAEs exist at LAYER 12 with width 65k (in addition to the 16k used so far), and that other LAYERS are available -- so '65k-width and/or a second layer' is a real drop-in. Report the exact available (layer, width) options you can confirm. (Do NOT download anything; documentation read only.)
  (2C) Layer dependence. Grep SAEBench / Gemma-Scope for any evidence that absorption / feature structure varies by LAYER (layer-12 vs others), to justify the 'second layer' arm.
  (2D) Numeric-digit-token reconstruction caveat. Note the hypothesis flag that the numeric family reconstructs <0.9 in isolation; search for any literature on SAE reconstruction quality on digit/number tokens that bears on whether the numeric absorption arm transfers across widths -- so the M2 framing can pre-empt the digit-reconstruction confound.
  Deliverable 2: a short M2 framing paragraph covering BOTH outcomes -- (i) replication-with-honest-deltas = generality of the auditability spine CONFIRMED; (ii) non-replication = DICTIONARY-DEPENDENCE OF ABSORPTION, which the literature explicitly predicts (wider SAEs absorb MORE; Matryoshka/H-SAE/SASA exist precisely to fix this), and is itself a clean, publishable finding -- plus a one-line lead-in stating cross-dictionary replication is the literature-PREDICTED robustness axis, and the numeric-digit caveat gate.

  === STEP 3 -- CITATION FINALIZATION, BIBTEX, STRIP CHECKLIST (~25 min) ===
  (3A) Carry forward ALL iter-3/iter-4 locks verbatim (the STEP-0 list) into the final table -- do not re-verify.
  (3B) For each NEW M1/M2 cite (Farrell 2410.19278; CRISP 2508.13650; SAE-subspace-projection MIlqM98o9I; Conditional-Clamping 2503.11127; SRMU 2512.16297; SAUCE 2503.14530; 'Discover-not-act' 2506.23845; WMDP 2403.03218; TOFU 2401.06121; MUSE 2407.06460; RWKU; SHRED 2605.07482; survey 2601.13264; Sensitivity 2509.23717): FETCH the arXiv abstract page to confirm (i) the arXiv ID resolves, (ii) the exact title, (iii) the full author list, (iv) any venue in metadata (else 'arXiv preprint <year>'). Because several IDs are future-dated (2512.*, 2601.*, 2602.*, 2605.*, 2606.*) -- plausible given the June-2026 date -- VERIFY each by fetch and NEVER invent fields; if an author list or venue cannot be confirmed, mark it 'UNRESOLVED -- verify at bib-time.' Confirm SAUCE = ICCV 2025 specifically (CVF open-access page).
  (3C) Upgrade re-check (cheap): for the still-preprint carry-forwards most likely to have been accepted by now (Muchane 2506.01197, SASA 2606.06333, Winnicki 2604.23829, Deng 2506.18141, DPE 2505.23027 camera-ready, SCR/TPP 2411.18895 camera-ready, Feature Hedging 2505.11756), do ONE search each for a 2026 venue; upgrade ONLY on an authoritative venue page, else keep as preprint. Do NOT spend more than a few minutes here.
  (3D) Emit the final BibTeX-ready table: columns {citation-key, title, authors (or UNRESOLVED), venue+year, arXiv-id, one-line role-in-paper}. Include a CORRECTIONS DIFF vs the iter-4 table (what is ADDED for M1/M2, what venue UPGRADED, what remains unresolved). Provide a copy-pasteable BibTeX block for the new entries (verified fields only).
  (3E) PRESENTATION-STRIP CHECKLIST for GEN_PAPER_TEXT (extend the iter-4 checklist): (i) strip ALL iteration/rebuttal/infra scaffolding (iter-1..5, 'previous draft', 're-run', 'review MAJOR/MINOR', M1..M9 labels, 'verdict reconciliation', art_<id>, torch/CUDA/pod/version strings, ITERATION-STATUS/MANDATE headers); (ii) move reproducibility/infra (SAE IDs, layer/width, seeds, gating thresholds, judge model IDs, hardware) to an appendix; (iii) LEAD with the M1 downstream selective-edit WIN over dense + the M2 cross-dictionary replication as the two headline contributions, with measured auditability (KG-repair FDR, surgical edits, member-labeling) as the spine; classification/selection SUPPORTING and within-SAE; (iv) one dedicated HONEST-NEGATIVES subsection that now MUST include the NEW possible negatives: M1 may fail to beat dense everywhere ('localization buys auditability but not a better outcome'), M2 may not replicate ('dictionary-dependence'), plus the carry-forward negatives (no dense-probe out-classification; per-letter joint 2/5 I,D; non-spelling affirmative selection n=1-2 Georgia/Jordan; numeric diagnostic-unconfirmed; toxicity co-firing negative; model-diffing confound-bounded null; steering surgical only on L,D); (v) use the locked table + the cite-and-distinguish one-liners (M1: Farrell/CRISP/SAUCE/SRMU/'discover-not-act'/SAE-TS/SRS/LEACE/AxBench; M2: SAEBench/Chanin/Matryoshka/Feature-Hedging; carry-forward: PS-Eval, Winnicki, Kantamneni).

  === STEP 4 -- ASSEMBLE OUTPUTS ===
  Write research_report.md with sections: (A) M1 positioning -- cite-and-distinguish table + short/long positioning paragraphs + unlearning-Pareto win-condition framing + AxBench/Farrell honest-concession note + scope guardrail; (B) M2 positioning -- width/dictionary-size/layer dependence evidence + both-outcome framing paragraph + Gemma-Scope (layer,width) availability + numeric-digit caveat; (C) locked citation table + corrections diff + BibTeX; (D) presentation-strip checklist. Write research_out.json = {answer: a tight executive synthesis of the M1 verdict (distinct + correctly framed, with the honest concession), the M2 framing (literature-predicted robustness axis, both outcomes covered), and the citation status (locked + new + unresolved); sources: >=25 entries each a markdown link with a 1-line annotation of what it establishes; follow_up_questions: 3-5 genuinely open items, e.g. whether to additionally run a small WMDP-style sub-domain unlearning demo to make M1 land in a recognized benchmark, whether '2506.23845 discover-not-act' warrants a dedicated rebuttal paragraph, and which of the future-dated IDs still need author-list resolution at bib-time}.

  FAILURE / CONTINGENCY HANDLING: (a) If a genuine precedent for 'KG-named single-absorber sub-context edit beating dense on a joint collateral+fluency metric' is found -> do NOT suppress it; report prominently and recommend M1 be reframed as parity/cite-and-distinguish, and note this caps the contribution. (b) If 2506.23845 ('discover-not-act') is a strong philosophical threat -> draft the explicit reconciliation (CCRG DISCOVERS the absorber via grouping; does not act on a pre-known concept; win is regime-scoped). (c) If no public 65k or alternate-layer Gemma-2-2b SAE can be confirmed -> state the constraint explicitly and recommend the M2 experiment plan flag it (note: 65k canonical at layer 12 is expected to exist per SAEBench/Gemma-Scope; report the exact confirmable options). (d) If a future-dated arXiv ID does NOT resolve -> mark UNRESOLVED, do not fabricate, and add to follow-ups. (e) Keep derivation/exposition strictly cite-and-distinguish; do not overclaim broad taxonomic generalization (guardrail carried from iter-4).
explanation: >-
  This is the M9 + new-task-positioning research artifact for iteration 5. The iter-4 reviewer made two MAJORS load-bearing:
  M1 (the KG-localized single-absorber edit must BEAT a dense baseline on an outcome that matters) and M2 (the spine must
  replicate across SAE dictionaries). Those are EXPERIMENTS, but their paper-framing decides whether the next GEN_PAPER_TEXT
  draft reads as a deliberate, literature-grounded contribution or an afterthought -- and the prior audits (iter-3, iter-4)
  explicitly did NOT cover the two literatures these new results live in. M1 is fundamentally a SELECTIVE / TARGETED machine-unlearning-with-utility-preservation
  claim (lower neighbor collateral + preserved fluency at matched forget-quality = a Pareto-dominance), so it must be positioned
  against the SAE-unlearning line (Farrell/Lau/Conmy 2410.19278 is both the nearest precedent and the honest concession that
  raw-SAE unlearning >= RMU side-effects), the unlearning benchmark/metric conventions (WMDP/TOFU/MUSE/RWKU/SHRED), the framing-threat
  that SAEs should be used to discover-not-act (2506.23845), and the already-settled steering/erasure side-effect bar (AxBench/SAE-TS/SRS/LEACE).
  M2 must be grounded in the documented WIDTH/dictionary-size/layer dependence of absorption (SAEBench's explicit 'absorption
  increases with width', Chanin, Matryoshka, Feature Hedging's two-sided width effect), so a cross-dictionary replicate-or-dependence
  result is the literature-PREDICTED robustness axis. Finalizing the venue-locked citation table + BibTeX + presentation-strip
  checklist (carrying forward every iter-3/iter-4 lock, adding the new M1/M2 cites with verified IDs/authors, flagging unresolved
  future-dated author lists rather than inventing them) gives GEN_PAPER_TEXT a clean, honest, drop-in foundation. The work
  is pure web research ($0, no code), correctly scoped to a RESEARCH executor, and builds directly on the two dependency audits
  without re-doing settled entries.
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

### [2] HUMAN-USER prompt · 2026-06-18 02:26:06 UTC

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

### [3] SKILL-INPUT — aii-web-tools · 2026-06-18 02:26:12 UTC

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

## Task: `gen_art_dataset_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-18 02:40:33 UTC

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
Find, evaluate, and prepare high-quality datasets for the research experiment.
Adapt your search strategy based on the hypothesis and domain requirements.
</task>

<common_mistakes_to_avoid>
Critical pitfalls from past runs. MUST check for and avoid each one.

**1. Picking Obscure or Unusable Datasets**
Do NOT select datasets just because they match a keyword. Red flags: very few downloads (<100), no documentation (dataset card, paper, or GitHub page). Prefer well-used datasets (not necessarily popular or widely known) with clear documentation.
CHECK: >100 downloads? Has documentation? If any "no" → find a better dataset.

**2. Fabricating Dataset Provenance**
Do NOT invent justifications for why a dataset is relevant. If a dataset name contains a number (e.g., "797"), do NOT assume it refers to a specific benchmark suite, OpenML ID, or paper without verification. In past runs, an agent assumed "797" referred to "OpenML benchmark suite 797" with zero evidence, then fabricated a rationale. This was completely false.
CHECK: Can you cite a specific, verifiable source (paper, benchmark page, dataset card) confirming this dataset is what you claim? If not, do not make provenance claims.

**3. Not Verifying Dataset Usefulness**
Always sanity-check that a dataset is actually suitable for the task before committing. Download a sample, inspect the features, and run a quick baseline appropriate for the domain. If the dataset lacks signal or structure for the hypothesis being tested, the entire experiment is wasted.

**4. Settling for the Only Search Result**
If your search returns only 1-2 results, your search terms are too narrow. Broaden your queries, try different keyword combinations, or search for well-known benchmark datasets in the domain. A single obscure result from a narrow query should never be your final choice.
CHECK: Fewer than 5 candidate datasets? Run additional searches with broader or different terms before making a selection.
</common_mistakes_to_avoid>

<critical_requirements>
- Keep final response under 300 characters
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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx7
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands) — Forward M7 Building Block
summary: >-
  A pure CPU/data artifact that builds a multi-hierarchy homograph/polysemy entity testbed as a drop-in extension of the iter-1
  non-spelling absorption testbed (art_t2uUbjSwpd3t). It adds FOUR entity is-a hierarchies whose surface tokens carry strong
  competing non-target senses (city homographs e.g. Phoenix/Mobile/Reading/Bath/Nice/Buffalo; month-names-that-are-given-names
  May/March/August/April/June; given-names-that-are-common-words Grace/Hope/Mark/Bill/Will/Rose/Frank; and one additional
  documented-homograph hierarchy = brand/company names that are common words e.g. Apple/Amazon/Shell/Gap/Dove/Target/Orange/Subway).
  Each hierarchy ships the SAME three coordinated components as dataset_2 — (A) content-flip minimal pairs, (B) surface-flip
  pairs, (C) a frozen pile-uncopyrighted (pinned rev) diagnostic corpus labelled by frozen, model-independent sub-context
  — plus a NEW homograph-competitor negative family (the same surface token in its non-target sense) that is the matched hard
  control making suppressed-parent absorption visible. Output is the AII exp_sel_data_out schema, one `dataset` per hierarchy,
  with per-entity absorption_readiness counts so next iteration knows which entities are inferentially powered (>=150 diagnostic-fold
  positives). Explicitly a next-iteration building block: NOT consumed by this iteration's parallel experiments.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  GOAL. Provide breadth of homograph/polysemy entity CANDIDATES so the persistent single-slice taxonomic critique (Georgia-only, Jordan descriptive n=124) can be answered next iteration with many suppressed-parent cases rather than re-arguing one country. Each candidate entity must be a token whose dominant training-distribution sense is NOT the target is-a sense (that competition is exactly what produces a suppressed-parent recall hole / feature absorption), AND must be frequent enough in TARGET sense in the pile to reach >=150 diagnostic-fold positives (eligible) or be honestly flagged descriptive_only.

  STRUCTURE. Must be a strict structural drop-in for the iter-1 non-spelling testbed (workspace 3_invention_loop/iter_1/gen_art/gen_art_dataset_2, artifact art_t2uUbjSwpd3t): same exp_sel_data_out on-disk format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}, FLAT metadata_* keys, no nested objects), same three components per hierarchy, same fold semantics (pairs train/test by pair_id stratified by sub_context; corpus train/diagnostic by doc), same gemma-2-2b token-index anchoring, same pinned pile revision, same readiness manifest. The downstream K-track + form-free absorption diagnostic pipeline must run on it unchanged except for the new entity-type/neg-family enum values.

  FOUR HIERARCHIES (one `dataset` each):
    1. city_homograph_absorption  — parent concept = 'is a city/place name'; sub_context = a specific homograph city.
    2. month_name_absorption      — parent concept = 'is a calendar month'; sub_context = one of the 12 months (homograph-strong: May/March/August/April/June; rest included for completeness).
    3. given_name_absorption      — parent concept = 'is a person/given name'; sub_context = a specific given name that is also a common word.
    4. brand_homograph_absorption — parent concept = 'is a company/brand name'; sub_context = a specific brand that is also a common word.

  PER ENTITY we want, frozen and model-independent: (i) the entity surface form; (ii) its competitor (non-target) sense in plain words; (iii) a homograph-strength score (Zipf frequency of the lowercase common-word competitor via the `wordfreq` package — higher = stronger competing sense = more likely to absorb the parent); (iv) >=150 diagnostic-fold TARGET-SENSE corpus positives where eligible.

  SIZE/FORMAT. Text-only, no SAE/model/activation computation. Each of full/mini/preview_data_out.json < 100 MB (target full ~20-80 MB). UTF-8 JSON. Real natural text from monology/pile-uncopyrighted at the SAME pinned commit 3be90335b66f24456a5d6659d9c8d208c0357119 for component C; deterministic templated + small LLM-augmented sentences for components A/B. Frozen seed for full reproducibility. Sub-context and target/competitor sense labels assigned PURELY from surface form / regex / gazetteer / disambiguating local context — never from any model — so the degenerate-construction guard holds and absorption presence/absence remains an empirical finding, not baked into the data.
dataset_search_plan: |-
  Read this whole plan first. The fastest correct path is to COPY the three iter-1 scripts and adapt them; do not rewrite from scratch.

  ========================================================================
  STEP 0 — REUSE THE ITER-1 SCAFFOLD (do this first)
  ========================================================================
  Read the iter-1 workspace /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/ (artifact art_t2uUbjSwpd3t). Copy build_dataset.py, pipeline.py, data.py, schema.json, pyproject.toml into this workspace and adapt them. Preserve verbatim the machinery that already works: pile-uncopyrighted streaming via requests + zstandard.ZstdDecompressor().stream_reader over shards train/00..29.jsonl.zst at PILE_REV=3be90335b66f24456a5d6659d9c8d208c0357119; windows_from_text (sentence-split, <=400 char windows, alpha-fraction>=0.4 filter, dedup by hash); make_row(...) flat-metadata builder; build_content_pair / build_surface_pair; add_token_indices (AutoTokenizer offset_mapping, add_special_tokens=False, batch 512); assign_folds (pairs 70/30 train/test by pair_id stratified by (hierarchy,sub_context,row_type); corpus 50/50 train/diagnostic stratified by (hierarchy,sub_context|neg_family,output)); the async OpenRouter call_llm + generate/judge pattern; run_asserts; write_outputs (manifest + absorption_readiness); data.py orchestration (build -> aii-json format mini/preview -> validate exp_sel_data_out). Use the gemma tokenizer mirror unsloth/gemma-2-2b (gated google/gemma-2-2b may 401; the iter-1 manifest used 'google/gemma-2-2b' with HF_TOKEN — try that first, fall back to unsloth mirror). Use python3 (NOT `uv run`) exactly as data.py documents. Implement a --scale smoke path (tiny caps, ~1 min) to validate logic before the full run.

  ========================================================================
  STEP 1 — CURATE THE FOUR HOMOGRAPH GAZETTEERS (replace the country/numeric gazetteers)
  ========================================================================
  For EACH entity store a dict: {surface, target_type, competitor_sense_word(s), competitor_gloss, homograph_strength}. homograph_strength = wordfreq.zipf_frequency(lowercase_competitor, 'en') (add `wordfreq` to deps; if unavailable, fall back to a hardcoded high/med/low tag). Prefer entities with HIGH competitor Zipf (strong competing sense) AND expected target-sense pile frequency high enough for >=150 diagnostic positives.

  1A. CITIES (city_homograph_absorption). Source candidates with geonamescache: `gc = geonamescache.GeonamesCache(min_city_population=15000); gc.get_cities()` -> records with 'name','population','countrycode'. Intersect city names with a common-English-word list (use the `wordfreq` top-N English words, or nltk.corpus.words, or a small builtin set) to surface collisions, then CURATE to a clean list of well-documented homograph cities with strong competitors. Seed list (verify/extend): Phoenix (mythical bird/comeback/Joaquin Phoenix), Mobile (adjective/phone), Reading (gerund 'reading'), Bath (bathtub), Nice (adjective 'nice'), Buffalo (the animal), Hull (ship hull), Cork (bottle cork), Split (verb 'split'), Bend (verb), Worth (preposition/noun), Mercury (planet/element/Freddie Mercury), Jackson (surname/Michael Jackson), Columbus (Christopher Columbus), Cleveland (surname/Grover Cleveland), Florence (given name), Sydney (given name), Sandy (adjective/given name), Surprise (noun), Hollywood (the film industry), Paris (Greek myth/Paris Hilton), Jordan (river/Michael Jordan — place sense via West Jordan etc.), Cologne (perfume). Include ~20-28 cities; prioritize the higher-frequency ones (Phoenix, Paris, Mobile, Reading, Mercury, Jackson, Columbus, Cleveland, Buffalo, Florence) for eligibility; flag rarer ones (Hull, Cork, Split, Worth, Cologne) as likely descriptive_only.

  1B. MONTHS (month_name_absorption). Use `calendar.month_name[1:13]` for all 12. Homograph-strong: May (modal verb 'may'), March (verb 'march/marched/marching'), August (adjective 'august'=distinguished), April & June (given names), plus minor: 'Mayday', 'Marching'. All 12 are frequent in target sense (date contexts) -> all should reach eligible easily; the absorption signal of interest concentrates on May/March/August.

  1C. GIVEN NAMES (given_name_absorption). Curate names that ARE common English words with strong competitors (virtue/word names): Grace (gracefulness), Hope (hope), Faith (faith), Joy (joy), Mark (mark/to mark), Bill (invoice/bird beak), Will (modal verb 'will'/testament), Rose (flower/past tense of rise), Frank (adjective 'frank'/franking), Pat (to pat), Dawn (daybreak), Summer (season), Autumn (season), Crystal (crystal), Daisy/Lily/Violet/Ivy/Holly/Rosemary (plants), Pearl (gem), Ruby (gem/color), Art (art), Earl (nobility rank), Jack (to jack/playing card), Drew (past tense of draw), Sky (the sky), Reed (a reed), Chase (to chase), Wade (to wade), Cliff (a cliff), Dean (academic dean), Robin (the bird), Carol (a carol/to sing). Include ~25-35; prioritize high-frequency competitors (Grace, Hope, Mark, Bill, Will, Rose, Frank, Faith, Joy, Dawn, Jack, Drew, Sky, Art) for eligibility.

  1D. BRANDS (brand_homograph_absorption — the additional documented-homograph is-a hierarchy). Curate brands/companies that are common words with strong competitors: Apple (fruit), Amazon (river/rainforest/warrior), Shell (seashell), Gap (a gap), Dove (bird/past tense of dive), Target (a target/to aim), Orange (fruit/color/telecom), Subway (underground train), Tide (ocean tide), Corona (crown/sun corona), Visa (travel document), Polo (the sport), Puma/Jaguar (animals), Caterpillar (the insect), Dawn (daybreak — dish soap), Sprint (to sprint), Chase (to chase — bank), Square (a square), Oracle (a prophet), Monster (a monster), Patagonia (the region), Java (the island/coffee), Python (the snake — borderline brand/lang). Include ~22-30; prioritize Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java for eligibility.

  MERGE-SAFETY across hierarchies: some tokens recur (Dawn name vs brand; Jordan city vs prior country dataset). Keep them per-hierarchy with the hierarchy-appropriate target sense; record the cross-hierarchy collision in metadata_notes. Do NOT include pure country names already covered by dataset_2 except where the city/place sense is the target (e.g. Jordan-as-place).

  ========================================================================
  STEP 2 — COMPONENT A: CONTENT-FLIP MINIMAL PAIRS (per hierarchy)
  ========================================================================
  Mirror build_content_pair: x_on = template.replace('{S}', entity) (output=positive, target sense), x_off = template.replace('{S}', off_filler) (output=negative, parent concept absent), surface-matched within the pair. CRITICAL: the carrier template must DISAMBIGUATE x_on to the TARGET sense so the positive genuinely carries the parent concept. Provide ~8-12 carriers per hierarchy whose syntax forces the target reading:
    - city: place-frame carriers — 'She flew to {S} for the conference.', 'They drove from {S} to the coast.', 'The mayor of {S} gave a speech.', 'He grew up in {S}.', '{S} is the largest city in the region.' off_filler pool = (a) NON-city places: country names / generic 'the coast','the capital','the countryside'; (b) person/company names; (c) generic noun. neg_family in {other_place, other_entity, easy}.
    - month: time-frame carriers — 'The event is scheduled for {S}.', 'They got married in {S}.', 'It happened back in {S} of that year.', 'The deadline falls in early {S}.', 'We met on {S} 14th.' off_filler pool = NON-month time words ('spring','winter','the weekend','Monday','noon','the holidays') and generic words. neg_family in {other_time, easy}.
    - given_name: person-frame carriers — '{S} smiled and waved.', 'My friend {S} just called.', 'Mr. {S} signed the form.', 'They named the baby {S}.', '{S} asked a thoughtful question.' off_filler pool = generic person references ('the teacher','my neighbor','the stranger') and non-name nouns. neg_family in {other_person_ref, easy}.
    - brand: company-frame carriers — '{S} announced a new product today.', 'Shares of {S} rose after earnings.', 'She works at {S}.', '{S} opened a new store downtown.', 'The {S} logo is famous.' off_filler pool = generic company refs ('the startup','the firm','a competitor') and non-brand nouns. neg_family in {other_company_ref, easy}.
  Build deterministically (templated) first; record metadata_template_id. Anchor target span at the {S} slot (x_on real span; x_off zero-width slot start), exactly like build_content_pair. Set metadata_sub_context = entity for x_on (positive), null for x_off (negative). Aim ~30-60 content pairs per hierarchy from templates before LLM augmentation.

  ========================================================================
  STEP 3 — COMPONENT B: SURFACE-FLIP PAIRS (per hierarchy)
  ========================================================================
  Mirror build_surface_pair: same entity in target sense, two different carriers, BOTH positive, for the unit-level surface-invariance admission check. Provide ~6 surface carriers per hierarchy (target-sense-forcing, distinct from the content carriers), pair disjoint frames per entity. Aim ~20-40 surface pairs per hierarchy.

  ========================================================================
  STEP 4 — COMPONENT C: FROZEN PILE DIAGNOSTIC CORPUS + HOMOGRAPH DISAMBIGUATION (the key new machinery)
  ========================================================================
  Stream pile-uncopyrighted exactly as iter-1 (stream_pile_corpus). For each candidate window run, per hierarchy, a high-PRECISION sense classifier that assigns ONE of: TARGET-SENSE positive (sub_context=entity), HOMOGRAPH-COMPETITOR negative (same surface token, non-target sense — the matched hard control), OTHER-ENTITY negative (a different-type entity), or EASY negative (no entity). Precision over recall: when the entity appears but NO disambiguating cue fires, EXCLUDE the window (do not mislabel). Concrete cue rules (extend as needed; all case-aware):
    - MONTH target-sense (high precision): /(?:\b(?:in|on|since|until|by|during|early|late|mid|of)\s+)(Month)\b/, /(Month)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?/, /\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(Month)\b/, /(Month)\s+\d{4}/, /(?:last|next|this)\s+(Month)/. MONTH competitor: May modal /\bMay\s+(?:I|we|you|he|she|it|they|the|not|have|be|or|well)\b/; March verb /\b[Mm]arch(?:ed|ing|es)?\b/ when NOT preceded by a date/preposition cue; August adjective /\baugust\s+(?:body|assembly|presence|institution|gathering)\b/.
    - CITY target-sense: /(?:\b(?:in|at|to|from|near|outside|downtown|visited?|toured?)\s+)(City)\b/, /(City),\s+[A-Z][a-z]+/ (City, State/Country), /(City)\s+(?:City|Airport|Station|County|metro|residents|suburb|downtown)/, /the\s+city\s+of\s+(City)/. CITY competitor: lowercase common-word hit (e.g. 'mobile','reading','bath','nice','buffalo','cork','split','worth') OR capitalized in a clearly non-place frame (e.g. 'Joaquin Phoenix', 'rise.{0,15}from the ashes', 'Mercury' + element/planet cue).
    - GIVEN-NAME target-sense: /(?:\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Lady|President|Senator|Aunt|Uncle|Saint|St)\.?\s+)(Name)\b/, /(Name)\s+[A-Z][a-z]+/ (Name + likely surname), /(?:named|called)\s+(Name)\b/, /(Name)'s\b/, /(Name)\s+(?:said|asked|replied|smiled|nodded|wrote|added)\b/. GIVEN-NAME competitor: lowercase common-word hit ('grace','hope','mark','bill','will','rose','frank','faith','joy','dawn','art','jack','drew','sky','reed','chase').
    - BRAND target-sense: /(Brand)\s+(?:Inc|Corp|Co|Ltd|announced|released|launched|unveiled|reported|shares?|stock|CEO|earnings|products?|store)/, /(Brand)'s\s+(?:new|latest|CEO|stock|shares|products|earnings)/, /(?:at|from|by|for)\s+(Brand)\s+(?:Inc|Corp|store|today)/. BRAND competitor: lowercase common-word hit ('apple','amazon','shell','gap','dove','target','orange','subway','tide','corona','visa','polo','puma','jaguar','square','java','python','monster').
  Negatives priority/abundance handled like iter-1 (positives have absolute priority; negatives fill from leftover docs). Per-entity TARGET-SENSE positive cap ~300 (=> ~150 diagnostic-fold after the 50/50 split). Set max_records high (start ~900k like iter-1; raise toward all 30 shards if eligibility is short) and an overall wall-clock guard. Use the prefer-rarest (spread across entities) priority for target positives so as many entities as possible reach the cap; collect a balanced pool of homograph_competitor + easy negatives (target a few hundred to ~2-3k each per hierarchy).
  VALIDATE THE LABELLER: after building the corpus, LLM-judge a stratified SAMPLE (~150-250 windows across hierarchies/entities) for sense-correctness and report target-sense precision per hierarchy in the manifest (this MEASURES the heuristic precision; it does NOT relabel the corpus). If sampled precision < ~0.9 for a hierarchy, TIGHTEN that hierarchy's cues (require a stronger cue / add exclusions) and rebuild — do not ship low-precision target labels.

  ========================================================================
  STEP 5 — TOKEN ANCHORING, LLM AUGMENT+JUDGE, FOLDS
  ========================================================================
  Token indices: reuse add_token_indices unchanged (gemma-2-2b offset mapping; null if tokenizer unavailable, with token_indices_present=false in manifest).
  LLM augment + judge (OpenRouter only, hard $10 cap, TARGET < $3 — iter-1 spent $0.01): reuse the async pattern. Generator = openai/gpt-4o-mini (cheap, 100% pass in iter-1) or google/gemini-3.1-flash-lite per the dossier; judge = same or anthropic/claude-haiku-4.5. EXTEND the judge rubric with a NEW boolean `sense_correct` (true iff the entity in x_on is unambiguously in its TARGET is-a sense — city/month/name/brand — given the carrier); keep content_flipped, surface_preserved, grammatical, score. metadata_llm_judge_pass = content_flipped AND surface_preserved AND grammatical AND sense_correct. Generate a modest number of diverse extra carriers per hierarchy (~20-40 each) and spot-judge ~20% of templated pairs + 100% of LLM-generated pairs; report pass rate and spend in the manifest. Track COST['usd'] after every call and STOP at the budget guard.
  Folds: reuse assign_folds unchanged (pairs by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified). The diagnostic fold is where next iteration's parent-probe recall-hole search runs.

  ========================================================================
  STEP 6 — SCHEMA, MANIFEST, OUTPUTS, VALIDATION
  ========================================================================
  Update schema.json from the iter-1 copy: `dataset` enum = ['city_homograph_absorption','month_name_absorption','given_name_absorption','brand_homograph_absorption']; add metadata_hierarchy enum ['city','month','given_name','brand']; expand metadata_neg_family enum to include 'homograph_competitor','other_place','other_entity','other_time','other_person_ref','other_company_ref','easy'; ADD fields metadata_target_sense (e.g. 'city'|'month'|'given_name'|'brand'|'competitor'|null), metadata_competitor_sense (string, the competing word/gloss), metadata_homograph_strength (number, lowercase-competitor Zipf), metadata_entity (string canonical entity). Keep all other metadata_* keys identical to iter-1 (flat, no nested objects; patternProperties ^metadata_). Keep the logical_row_schema mirror and a top-level list of the homograph entities per hierarchy.
  Manifest (reuse write_outputs, extend): per-hierarchy templated/surface/corpus counts; corpus_positive_counts_by_sub (per entity); source_counts; pile_set_name_counts; llm_pair_pass_rate; llm sense-precision sample results per hierarchy; llm_cost_breakdown; and the absorption_readiness block: for EACH (hierarchy, entity) the diagnostic_positives count and status ('eligible' if >=150 else 'descriptive_only'). Add a design_note that labels are surface/regex/gazetteer-derived and absorption presence/absence is a future-iteration empirical finding (this corpus equally supports the spelling-specific null and a positive homograph-absorption finding). Add a prominent note: 'NEXT-ITERATION BUILDING BLOCK — not consumed by this iteration's parallel experiments.'
  Outputs via data.py: full_data_out.json + manifest.json, then aii-json format script -> full/mini/preview_data_out.json (rename), then validate against exp_sel_data_out. Run run_asserts (output<->concept_present consistency; pair role integrity x_on/x_off & surface_a/surface_b; positives have real spans; sub_context null on x_off/pure negatives; positive-input uniqueness within (row_type,hierarchy); (pair_id,role) uniqueness; target_text == input[start:end]). Use aii-file-size-limit skill to confirm each variant < 100 MB; if full exceeds, lower per-entity corpus caps or window count (do NOT silently truncate the schema). Deliver: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, full/mini/preview_data_out.json, pyproject.toml (pin requests, zstandard, transformers, loguru, aiohttp, geonamescache, wordfreq, and python-version).

  ========================================================================
  FAILURE SCENARIOS & FALLBACKS
  ========================================================================
  - An entity is too rare in TARGET sense to reach 150 diagnostic positives: flag descriptive_only and keep it (breadth for candidate search is still valuable); ensure EACH hierarchy has >=3-5 ELIGIBLE entities (months are guaranteed; pick the highest-frequency cities/names/brands). If a whole hierarchy cannot field >=3 eligible entities after scanning more shards, report that honestly in the manifest and keep it descriptive.
  - Disambiguation precision low for a hierarchy (LLM sample < ~0.9): tighten cues / add exclusions and rebuild that hierarchy; given_name and brand are the hardest — bias toward stronger cues (titles+surnames for names; corporate tokens for brands) and accept lower recall.
  - pile shard fetch fails: continue to next shard (iter-1 already handles this); ensure at least a few shards succeed.
  - gemma tokenizer gated/unavailable: set token_indices=null and token_indices_present=false; downstream can re-tokenize.
  - wordfreq unavailable: fall back to a hardcoded high/med/low homograph_strength tag per entity.
  - LLM budget pressure: skip generation, keep templated A/B pairs and the (cheap) precision-validation judge sample only; never exceed the $10 cap (stop at the internal guard).
  - Cross-hierarchy token collisions (Dawn, Jordan, Mercury): keep per-hierarchy with the correct target sense and note the collision.
target_num_datasets: 4
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
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
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 32 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 16 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 8 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
```

### [2] HUMAN-USER prompt · 2026-06-18 02:40:33 UTC

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

### [3] SKILL-INPUT — aii-python · 2026-06-18 02:40:55 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-06-18 02:40:55 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-06-18 02:41:13 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-06-18 02:41:13 UTC

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

### [7] SKILL-INPUT — aii-use-hardware · 2026-06-18 02:41:13 UTC

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

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-18 02:41:13 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SYSTEM-USER prompt · 2026-06-18 03:43:31 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx7
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands) — Forward M7 Building Block
summary: >-
  A pure CPU/data artifact that builds a multi-hierarchy homograph/polysemy entity testbed as a drop-in extension of the iter-1
  non-spelling absorption testbed (art_t2uUbjSwpd3t). It adds FOUR entity is-a hierarchies whose surface tokens carry strong
  competing non-target senses (city homographs e.g. Phoenix/Mobile/Reading/Bath/Nice/Buffalo; month-names-that-are-given-names
  May/March/August/April/June; given-names-that-are-common-words Grace/Hope/Mark/Bill/Will/Rose/Frank; and one additional
  documented-homograph hierarchy = brand/company names that are common words e.g. Apple/Amazon/Shell/Gap/Dove/Target/Orange/Subway).
  Each hierarchy ships the SAME three coordinated components as dataset_2 — (A) content-flip minimal pairs, (B) surface-flip
  pairs, (C) a frozen pile-uncopyrighted (pinned rev) diagnostic corpus labelled by frozen, model-independent sub-context
  — plus a NEW homograph-competitor negative family (the same surface token in its non-target sense) that is the matched hard
  control making suppressed-parent absorption visible. Output is the AII exp_sel_data_out schema, one `dataset` per hierarchy,
  with per-entity absorption_readiness counts so next iteration knows which entities are inferentially powered (>=150 diagnostic-fold
  positives). Explicitly a next-iteration building block: NOT consumed by this iteration's parallel experiments.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  GOAL. Provide breadth of homograph/polysemy entity CANDIDATES so the persistent single-slice taxonomic critique (Georgia-only, Jordan descriptive n=124) can be answered next iteration with many suppressed-parent cases rather than re-arguing one country. Each candidate entity must be a token whose dominant training-distribution sense is NOT the target is-a sense (that competition is exactly what produces a suppressed-parent recall hole / feature absorption), AND must be frequent enough in TARGET sense in the pile to reach >=150 diagnostic-fold positives (eligible) or be honestly flagged descriptive_only.

  STRUCTURE. Must be a strict structural drop-in for the iter-1 non-spelling testbed (workspace 3_invention_loop/iter_1/gen_art/gen_art_dataset_2, artifact art_t2uUbjSwpd3t): same exp_sel_data_out on-disk format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}, FLAT metadata_* keys, no nested objects), same three components per hierarchy, same fold semantics (pairs train/test by pair_id stratified by sub_context; corpus train/diagnostic by doc), same gemma-2-2b token-index anchoring, same pinned pile revision, same readiness manifest. The downstream K-track + form-free absorption diagnostic pipeline must run on it unchanged except for the new entity-type/neg-family enum values.

  FOUR HIERARCHIES (one `dataset` each):
    1. city_homograph_absorption  — parent concept = 'is a city/place name'; sub_context = a specific homograph city.
    2. month_name_absorption      — parent concept = 'is a calendar month'; sub_context = one of the 12 months (homograph-strong: May/March/August/April/June; rest included for completeness).
    3. given_name_absorption      — parent concept = 'is a person/given name'; sub_context = a specific given name that is also a common word.
    4. brand_homograph_absorption — parent concept = 'is a company/brand name'; sub_context = a specific brand that is also a common word.

  PER ENTITY we want, frozen and model-independent: (i) the entity surface form; (ii) its competitor (non-target) sense in plain words; (iii) a homograph-strength score (Zipf frequency of the lowercase common-word competitor via the `wordfreq` package — higher = stronger competing sense = more likely to absorb the parent); (iv) >=150 diagnostic-fold TARGET-SENSE corpus positives where eligible.

  SIZE/FORMAT. Text-only, no SAE/model/activation computation. Each of full/mini/preview_data_out.json < 100 MB (target full ~20-80 MB). UTF-8 JSON. Real natural text from monology/pile-uncopyrighted at the SAME pinned commit 3be90335b66f24456a5d6659d9c8d208c0357119 for component C; deterministic templated + small LLM-augmented sentences for components A/B. Frozen seed for full reproducibility. Sub-context and target/competitor sense labels assigned PURELY from surface form / regex / gazetteer / disambiguating local context — never from any model — so the degenerate-construction guard holds and absorption presence/absence remains an empirical finding, not baked into the data.
dataset_search_plan: |-
  Read this whole plan first. The fastest correct path is to COPY the three iter-1 scripts and adapt them; do not rewrite from scratch.

  ========================================================================
  STEP 0 — REUSE THE ITER-1 SCAFFOLD (do this first)
  ========================================================================
  Read the iter-1 workspace /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/ (artifact art_t2uUbjSwpd3t). Copy build_dataset.py, pipeline.py, data.py, schema.json, pyproject.toml into this workspace and adapt them. Preserve verbatim the machinery that already works: pile-uncopyrighted streaming via requests + zstandard.ZstdDecompressor().stream_reader over shards train/00..29.jsonl.zst at PILE_REV=3be90335b66f24456a5d6659d9c8d208c0357119; windows_from_text (sentence-split, <=400 char windows, alpha-fraction>=0.4 filter, dedup by hash); make_row(...) flat-metadata builder; build_content_pair / build_surface_pair; add_token_indices (AutoTokenizer offset_mapping, add_special_tokens=False, batch 512); assign_folds (pairs 70/30 train/test by pair_id stratified by (hierarchy,sub_context,row_type); corpus 50/50 train/diagnostic stratified by (hierarchy,sub_context|neg_family,output)); the async OpenRouter call_llm + generate/judge pattern; run_asserts; write_outputs (manifest + absorption_readiness); data.py orchestration (build -> aii-json format mini/preview -> validate exp_sel_data_out). Use the gemma tokenizer mirror unsloth/gemma-2-2b (gated google/gemma-2-2b may 401; the iter-1 manifest used 'google/gemma-2-2b' with HF_TOKEN — try that first, fall back to unsloth mirror). Use python3 (NOT `uv run`) exactly as data.py documents. Implement a --scale smoke path (tiny caps, ~1 min) to validate logic before the full run.

  ========================================================================
  STEP 1 — CURATE THE FOUR HOMOGRAPH GAZETTEERS (replace the country/numeric gazetteers)
  ========================================================================
  For EACH entity store a dict: {surface, target_type, competitor_sense_word(s), competitor_gloss, homograph_strength}. homograph_strength = wordfreq.zipf_frequency(lowercase_competitor, 'en') (add `wordfreq` to deps; if unavailable, fall back to a hardcoded high/med/low tag). Prefer entities with HIGH competitor Zipf (strong competing sense) AND expected target-sense pile frequency high enough for >=150 diagnostic positives.

  1A. CITIES (city_homograph_absorption). Source candidates with geonamescache: `gc = geonamescache.GeonamesCache(min_city_population=15000); gc.get_cities()` -> records with 'name','population','countrycode'. Intersect city names with a common-English-word list (use the `wordfreq` top-N English words, or nltk.corpus.words, or a small builtin set) to surface collisions, then CURATE to a clean list of well-documented homograph cities with strong competitors. Seed list (verify/extend): Phoenix (mythical bird/comeback/Joaquin Phoenix), Mobile (adjective/phone), Reading (gerund 'reading'), Bath (bathtub), Nice (adjective 'nice'), Buffalo (the animal), Hull (ship hull), Cork (bottle cork), Split (verb 'split'), Bend (verb), Worth (preposition/noun), Mercury (planet/element/Freddie Mercury), Jackson (surname/Michael Jackson), Columbus (Christopher Columbus), Cleveland (surname/Grover Cleveland), Florence (given name), Sydney (given name), Sandy (adjective/given name), Surprise (noun), Hollywood (the film industry), Paris (Greek myth/Paris Hilton), Jordan (river/Michael Jordan — place sense via West Jordan etc.), Cologne (perfume). Include ~20-28 cities; prioritize the higher-frequency ones (Phoenix, Paris, Mobile, Reading, Mercury, Jackson, Columbus, Cleveland, Buffalo, Florence) for eligibility; flag rarer ones (Hull, Cork, Split, Worth, Cologne) as likely descriptive_only.

  1B. MONTHS (month_name_absorption). Use `calendar.month_name[1:13]` for all 12. Homograph-strong: May (modal verb 'may'), March (verb 'march/marched/marching'), August (adjective 'august'=distinguished), April & June (given names), plus minor: 'Mayday', 'Marching'. All 12 are frequent in target sense (date contexts) -> all should reach eligible easily; the absorption signal of interest concentrates on May/March/August.

  1C. GIVEN NAMES (given_name_absorption). Curate names that ARE common English words with strong competitors (virtue/word names): Grace (gracefulness), Hope (hope), Faith (faith), Joy (joy), Mark (mark/to mark), Bill (invoice/bird beak), Will (modal verb 'will'/testament), Rose (flower/past tense of rise), Frank (adjective 'frank'/franking), Pat (to pat), Dawn (daybreak), Summer (season), Autumn (season), Crystal (crystal), Daisy/Lily/Violet/Ivy/Holly/Rosemary (plants), Pearl (gem), Ruby (gem/color), Art (art), Earl (nobility rank), Jack (to jack/playing card), Drew (past tense of draw), Sky (the sky), Reed (a reed), Chase (to chase), Wade (to wade), Cliff (a cliff), Dean (academic dean), Robin (the bird), Carol (a carol/to sing). Include ~25-35; prioritize high-frequency competitors (Grace, Hope, Mark, Bill, Will, Rose, Frank, Faith, Joy, Dawn, Jack, Drew, Sky, Art) for eligibility.

  1D. BRANDS (brand_homograph_absorption — the additional documented-homograph is-a hierarchy). Curate brands/companies that are common words with strong competitors: Apple (fruit), Amazon (river/rainforest/warrior), Shell (seashell), Gap (a gap), Dove (bird/past tense of dive), Target (a target/to aim), Orange (fruit/color/telecom), Subway (underground train), Tide (ocean tide), Corona (crown/sun corona), Visa (travel document), Polo (the sport), Puma/Jaguar (animals), Caterpillar (the insect), Dawn (daybreak — dish soap), Sprint (to sprint), Chase (to chase — bank), Square (a square), Oracle (a prophet), Monster (a monster), Patagonia (the region), Java (the island/coffee), Python (the snake — borderline brand/lang). Include ~22-30; prioritize Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java for eligibility.

  MERGE-SAFETY across hierarchies: some tokens recur (Dawn name vs brand; Jordan city vs prior country dataset). Keep them per-hierarchy with the hierarchy-appropriate target sense; record the cross-hierarchy collision in metadata_notes. Do NOT include pure country names already covered by dataset_2 except where the city/place sense is the target (e.g. Jordan-as-place).

  ========================================================================
  STEP 2 — COMPONENT A: CONTENT-FLIP MINIMAL PAIRS (per hierarchy)
  ========================================================================
  Mirror build_content_pair: x_on = template.replace('{S}', entity) (output=positive, target sense), x_off = template.replace('{S}', off_filler) (output=negative, parent concept absent), surface-matched within the pair. CRITICAL: the carrier template must DISAMBIGUATE x_on to the TARGET sense so the positive genuinely carries the parent concept. Provide ~8-12 carriers per hierarchy whose syntax forces the target reading:
    - city: place-frame carriers — 'She flew to {S} for the conference.', 'They drove from {S} to the coast.', 'The mayor of {S} gave a speech.', 'He grew up in {S}.', '{S} is the largest city in the region.' off_filler pool = (a) NON-city places: country names / generic 'the coast','the capital','the countryside'; (b) person/company names; (c) generic noun. neg_family in {other_place, other_entity, easy}.
    - month: time-frame carriers — 'The event is scheduled for {S}.', 'They got married in {S}.', 'It happened back in {S} of that year.', 'The deadline falls in early {S}.', 'We met on {S} 14th.' off_filler pool = NON-month time words ('spring','winter','the weekend','Monday','noon','the holidays') and generic words. neg_family in {other_time, easy}.
    - given_name: person-frame carriers — '{S} smiled and waved.', 'My friend {S} just called.', 'Mr. {S} signed the form.', 'They named the baby {S}.', '{S} asked a thoughtful question.' off_filler pool = generic person references ('the teacher','my neighbor','the stranger') and non-name nouns. neg_family in {other_person_ref, easy}.
    - brand: company-frame carriers — '{S} announced a new product today.', 'Shares of {S} rose after earnings.', 'She works at {S}.', '{S} opened a new store downtown.', 'The {S} logo is famous.' off_filler pool = generic company refs ('the startup','the firm','a competitor') and non-brand nouns. neg_family in {other_company_ref, easy}.
  Build deterministically (templated) first; record metadata_template_id. Anchor target span at the {S} slot (x_on real span; x_off zero-width slot start), exactly like build_content_pair. Set metadata_sub_context = entity for x_on (positive), null for x_off (negative). Aim ~30-60 content pairs per hierarchy from templates before LLM augmentation.

  ========================================================================
  STEP 3 — COMPONENT B: SURFACE-FLIP PAIRS (per hierarchy)
  ========================================================================
  Mirror build_surface_pair: same entity in target sense, two different carriers, BOTH positive, for the unit-level surface-invariance admission check. Provide ~6 surface carriers per hierarchy (target-sense-forcing, distinct from the content carriers), pair disjoint frames per entity. Aim ~20-40 surface pairs per hierarchy.

  ========================================================================
  STEP 4 — COMPONENT C: FROZEN PILE DIAGNOSTIC CORPUS + HOMOGRAPH DISAMBIGUATION (the key new machinery)
  ========================================================================
  Stream pile-uncopyrighted exactly as iter-1 (stream_pile_corpus). For each candidate window run, per hierarchy, a high-PRECISION sense classifier that assigns ONE of: TARGET-SENSE positive (sub_context=entity), HOMOGRAPH-COMPETITOR negative (same surface token, non-target sense — the matched hard control), OTHER-ENTITY negative (a different-type entity), or EASY negative (no entity). Precision over recall: when the entity appears but NO disambiguating cue fires, EXCLUDE the window (do not mislabel). Concrete cue rules (extend as needed; all case-aware):
    - MONTH target-sense (high precision): /(?:\b(?:in|on|since|until|by|during|early|late|mid|of)\s+)(Month)\b/, /(Month)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?/, /\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(Month)\b/, /(Month)\s+\d{4}/, /(?:last|next|this)\s+(Month)/. MONTH competitor: May modal /\bMay\s+(?:I|we|you|he|she|it|they|the|not|have|be|or|well)\b/; March verb /\b[Mm]arch(?:ed|ing|es)?\b/ when NOT preceded by a date/preposition cue; August adjective /\baugust\s+(?:body|assembly|presence|institution|gathering)\b/.
    - CITY target-sense: /(?:\b(?:in|at|to|from|near|outside|downtown|visited?|toured?)\s+)(City)\b/, /(City),\s+[A-Z][a-z]+/ (City, State/Country), /(City)\s+(?:City|Airport|Station|County|metro|residents|suburb|downtown)/, /the\s+city\s+of\s+(City)/. CITY competitor: lowercase common-word hit (e.g. 'mobile','reading','bath','nice','buffalo','cork','split','worth') OR capitalized in a clearly non-place frame (e.g. 'Joaquin Phoenix', 'rise.{0,15}from the ashes', 'Mercury' + element/planet cue).
    - GIVEN-NAME target-sense: /(?:\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Lady|President|Senator|Aunt|Uncle|Saint|St)\.?\s+)(Name)\b/, /(Name)\s+[A-Z][a-z]+/ (Name + likely surname), /(?:named|called)\s+(Name)\b/, /(Name)'s\b/, /(Name)\s+(?:said|asked|replied|smiled|nodded|wrote|added)\b/. GIVEN-NAME competitor: lowercase common-word hit ('grace','hope','mark','bill','will','rose','frank','faith','joy','dawn','art','jack','drew','sky','reed','chase').
    - BRAND target-sense: /(Brand)\s+(?:Inc|Corp|Co|Ltd|announced|released|launched|unveiled|reported|shares?|stock|CEO|earnings|products?|store)/, /(Brand)'s\s+(?:new|latest|CEO|stock|shares|products|earnings)/, /(?:at|from|by|for)\s+(Brand)\s+(?:Inc|Corp|store|today)/. BRAND competitor: lowercase common-word hit ('apple','amazon','shell','gap','dove','target','orange','subway','tide','corona','visa','polo','puma','jaguar','square','java','python','monster').
  Negatives priority/abundance handled like iter-1 (positives have absolute priority; negatives fill from leftover docs). Per-entity TARGET-SENSE positive cap ~300 (=> ~150 diagnostic-fold after the 50/50 split). Set max_records high (start ~900k like iter-1; raise toward all 30 shards if eligibility is short) and an overall wall-clock guard. Use the prefer-rarest (spread across entities) priority for target positives so as many entities as possible reach the cap; collect a balanced pool of homograph_competitor + easy negatives (target a few hundred to ~2-3k each per hierarchy).
  VALIDATE THE LABELLER: after building the corpus, LLM-judge a stratified SAMPLE (~150-250 windows across hierarchies/entities) for sense-correctness and report target-sense precision per hierarchy in the manifest (this MEASURES the heuristic precision; it does NOT relabel the corpus). If sampled precision < ~0.9 for a hierarchy, TIGHTEN that hierarchy's cues (require a stronger cue / add exclusions) and rebuild — do not ship low-precision target labels.

  ========================================================================
  STEP 5 — TOKEN ANCHORING, LLM AUGMENT+JUDGE, FOLDS
  ========================================================================
  Token indices: reuse add_token_indices unchanged (gemma-2-2b offset mapping; null if tokenizer unavailable, with token_indices_present=false in manifest).
  LLM augment + judge (OpenRouter only, hard $10 cap, TARGET < $3 — iter-1 spent $0.01): reuse the async pattern. Generator = openai/gpt-4o-mini (cheap, 100% pass in iter-1) or google/gemini-3.1-flash-lite per the dossier; judge = same or anthropic/claude-haiku-4.5. EXTEND the judge rubric with a NEW boolean `sense_correct` (true iff the entity in x_on is unambiguously in its TARGET is-a sense — city/month/name/brand — given the carrier); keep content_flipped, surface_preserved, grammatical, score. metadata_llm_judge_pass = content_flipped AND surface_preserved AND grammatical AND sense_correct. Generate a modest number of diverse extra carriers per hierarchy (~20-40 each) and spot-judge ~20% of templated pairs + 100% of LLM-generated pairs; report pass rate and spend in the manifest. Track COST['usd'] after every call and STOP at the budget guard.
  Folds: reuse assign_folds unchanged (pairs by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified). The diagnostic fold is where next iteration's parent-probe recall-hole search runs.

  ========================================================================
  STEP 6 — SCHEMA, MANIFEST, OUTPUTS, VALIDATION
  ========================================================================
  Update schema.json from the iter-1 copy: `dataset` enum = ['city_homograph_absorption','month_name_absorption','given_name_absorption','brand_homograph_absorption']; add metadata_hierarchy enum ['city','month','given_name','brand']; expand metadata_neg_family enum to include 'homograph_competitor','other_place','other_entity','other_time','other_person_ref','other_company_ref','easy'; ADD fields metadata_target_sense (e.g. 'city'|'month'|'given_name'|'brand'|'competitor'|null), metadata_competitor_sense (string, the competing word/gloss), metadata_homograph_strength (number, lowercase-competitor Zipf), metadata_entity (string canonical entity). Keep all other metadata_* keys identical to iter-1 (flat, no nested objects; patternProperties ^metadata_). Keep the logical_row_schema mirror and a top-level list of the homograph entities per hierarchy.
  Manifest (reuse write_outputs, extend): per-hierarchy templated/surface/corpus counts; corpus_positive_counts_by_sub (per entity); source_counts; pile_set_name_counts; llm_pair_pass_rate; llm sense-precision sample results per hierarchy; llm_cost_breakdown; and the absorption_readiness block: for EACH (hierarchy, entity) the diagnostic_positives count and status ('eligible' if >=150 else 'descriptive_only'). Add a design_note that labels are surface/regex/gazetteer-derived and absorption presence/absence is a future-iteration empirical finding (this corpus equally supports the spelling-specific null and a positive homograph-absorption finding). Add a prominent note: 'NEXT-ITERATION BUILDING BLOCK — not consumed by this iteration's parallel experiments.'
  Outputs via data.py: full_data_out.json + manifest.json, then aii-json format script -> full/mini/preview_data_out.json (rename), then validate against exp_sel_data_out. Run run_asserts (output<->concept_present consistency; pair role integrity x_on/x_off & surface_a/surface_b; positives have real spans; sub_context null on x_off/pure negatives; positive-input uniqueness within (row_type,hierarchy); (pair_id,role) uniqueness; target_text == input[start:end]). Use aii-file-size-limit skill to confirm each variant < 100 MB; if full exceeds, lower per-entity corpus caps or window count (do NOT silently truncate the schema). Deliver: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, full/mini/preview_data_out.json, pyproject.toml (pin requests, zstandard, transformers, loguru, aiohttp, geonamescache, wordfreq, and python-version).

  ========================================================================
  FAILURE SCENARIOS & FALLBACKS
  ========================================================================
  - An entity is too rare in TARGET sense to reach 150 diagnostic positives: flag descriptive_only and keep it (breadth for candidate search is still valuable); ensure EACH hierarchy has >=3-5 ELIGIBLE entities (months are guaranteed; pick the highest-frequency cities/names/brands). If a whole hierarchy cannot field >=3 eligible entities after scanning more shards, report that honestly in the manifest and keep it descriptive.
  - Disambiguation precision low for a hierarchy (LLM sample < ~0.9): tighten cues / add exclusions and rebuild that hierarchy; given_name and brand are the hardest — bias toward stronger cues (titles+surnames for names; corporate tokens for brands) and accept lower recall.
  - pile shard fetch fails: continue to next shard (iter-1 already handles this); ensure at least a few shards succeed.
  - gemma tokenizer gated/unavailable: set token_indices=null and token_indices_present=false; downstream can re-tokenize.
  - wordfreq unavailable: fall back to a hardcoded high/med/low homograph_strength tag per entity.
  - LLM budget pressure: skip generation, keep templated A/B pairs and the (cheap) precision-validation judge sample only; never exceed the $10 cap (stop at the internal guard).
  - Cross-hierarchy token collisions (Dawn, Jordan, Mercury): keep per-hierarchy with the correct target sense and note the collision.
target_num_datasets: 4
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
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
TODO 1. For the top 8 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

Each data ROW must be a separate example — do NOT create one example per dataset or per fold. Each data point (row, sample, instance) = one example. 500 rows → 500 examples. The output is GROUPED BY DATASET:
```json
{
  "datasets": [
    {
      "dataset": "iris",
      "examples": [
        {"input": "...", "output": "...", "metadata_fold": 2, "metadata_feature_names": [...]},
        ...
      ]
    },
    {
      "dataset": "adult_census",
      "examples": [...]
    }
  ]
}
```
Per-example required fields:
- `input`: input features/text (tabular: JSON string of feature values)
- `output`: target/label (as string)
Per-example optional metadata via `metadata_<name>` fields (flat, not nested object):
- `metadata_fold`: fold assignment (int), `metadata_feature_names`: feature name list, `metadata_task_type`: "classification"/"regression", `metadata_n_classes`: number of classes, `metadata_row_index`: original row index, etc.
Do NOT use `split`, `dataset`, or `context` as per-example fields. Dataset name goes at the group level, metadata goes in `metadata_*` fields.
TODO 2. Run 'uv run data.py' and fix errors. Validate full_data_out.json against exp_sel_data_out.json schema (aii-json skill) — fix errors. Generate preview, mini, full versions with aii-json skill's format script.
TODO 3. Read preview to inspect examples. Choose THE BEST 4 DATASETS based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [10] SYSTEM-USER prompt · 2026-06-18 03:48:43 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_5/gen_art/gen_art_dataset_1/results/out.json`
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
id: gen_plan_dataset_1_idx7
type: dataset
title: >-
  Homograph/Polysemy Entity Absorption Testbed (cities, months, given-names, brands) — Forward M7 Building Block
summary: >-
  A pure CPU/data artifact that builds a multi-hierarchy homograph/polysemy entity testbed as a drop-in extension of the iter-1
  non-spelling absorption testbed (art_t2uUbjSwpd3t). It adds FOUR entity is-a hierarchies whose surface tokens carry strong
  competing non-target senses (city homographs e.g. Phoenix/Mobile/Reading/Bath/Nice/Buffalo; month-names-that-are-given-names
  May/March/August/April/June; given-names-that-are-common-words Grace/Hope/Mark/Bill/Will/Rose/Frank; and one additional
  documented-homograph hierarchy = brand/company names that are common words e.g. Apple/Amazon/Shell/Gap/Dove/Target/Orange/Subway).
  Each hierarchy ships the SAME three coordinated components as dataset_2 — (A) content-flip minimal pairs, (B) surface-flip
  pairs, (C) a frozen pile-uncopyrighted (pinned rev) diagnostic corpus labelled by frozen, model-independent sub-context
  — plus a NEW homograph-competitor negative family (the same surface token in its non-target sense) that is the matched hard
  control making suppressed-parent absorption visible. Output is the AII exp_sel_data_out schema, one `dataset` per hierarchy,
  with per-entity absorption_readiness counts so next iteration knows which entities are inferentially powered (>=150 diagnostic-fold
  positives). Explicitly a next-iteration building block: NOT consumed by this iteration's parallel experiments.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  GOAL. Provide breadth of homograph/polysemy entity CANDIDATES so the persistent single-slice taxonomic critique (Georgia-only, Jordan descriptive n=124) can be answered next iteration with many suppressed-parent cases rather than re-arguing one country. Each candidate entity must be a token whose dominant training-distribution sense is NOT the target is-a sense (that competition is exactly what produces a suppressed-parent recall hole / feature absorption), AND must be frequent enough in TARGET sense in the pile to reach >=150 diagnostic-fold positives (eligible) or be honestly flagged descriptive_only.

  STRUCTURE. Must be a strict structural drop-in for the iter-1 non-spelling testbed (workspace 3_invention_loop/iter_1/gen_art/gen_art_dataset_2, artifact art_t2uUbjSwpd3t): same exp_sel_data_out on-disk format ({metadata, datasets:[{dataset, examples:[{input, output, metadata_*}]}]}, FLAT metadata_* keys, no nested objects), same three components per hierarchy, same fold semantics (pairs train/test by pair_id stratified by sub_context; corpus train/diagnostic by doc), same gemma-2-2b token-index anchoring, same pinned pile revision, same readiness manifest. The downstream K-track + form-free absorption diagnostic pipeline must run on it unchanged except for the new entity-type/neg-family enum values.

  FOUR HIERARCHIES (one `dataset` each):
    1. city_homograph_absorption  — parent concept = 'is a city/place name'; sub_context = a specific homograph city.
    2. month_name_absorption      — parent concept = 'is a calendar month'; sub_context = one of the 12 months (homograph-strong: May/March/August/April/June; rest included for completeness).
    3. given_name_absorption      — parent concept = 'is a person/given name'; sub_context = a specific given name that is also a common word.
    4. brand_homograph_absorption — parent concept = 'is a company/brand name'; sub_context = a specific brand that is also a common word.

  PER ENTITY we want, frozen and model-independent: (i) the entity surface form; (ii) its competitor (non-target) sense in plain words; (iii) a homograph-strength score (Zipf frequency of the lowercase common-word competitor via the `wordfreq` package — higher = stronger competing sense = more likely to absorb the parent); (iv) >=150 diagnostic-fold TARGET-SENSE corpus positives where eligible.

  SIZE/FORMAT. Text-only, no SAE/model/activation computation. Each of full/mini/preview_data_out.json < 100 MB (target full ~20-80 MB). UTF-8 JSON. Real natural text from monology/pile-uncopyrighted at the SAME pinned commit 3be90335b66f24456a5d6659d9c8d208c0357119 for component C; deterministic templated + small LLM-augmented sentences for components A/B. Frozen seed for full reproducibility. Sub-context and target/competitor sense labels assigned PURELY from surface form / regex / gazetteer / disambiguating local context — never from any model — so the degenerate-construction guard holds and absorption presence/absence remains an empirical finding, not baked into the data.
dataset_search_plan: |-
  Read this whole plan first. The fastest correct path is to COPY the three iter-1 scripts and adapt them; do not rewrite from scratch.

  ========================================================================
  STEP 0 — REUSE THE ITER-1 SCAFFOLD (do this first)
  ========================================================================
  Read the iter-1 workspace /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_dataset_2/ (artifact art_t2uUbjSwpd3t). Copy build_dataset.py, pipeline.py, data.py, schema.json, pyproject.toml into this workspace and adapt them. Preserve verbatim the machinery that already works: pile-uncopyrighted streaming via requests + zstandard.ZstdDecompressor().stream_reader over shards train/00..29.jsonl.zst at PILE_REV=3be90335b66f24456a5d6659d9c8d208c0357119; windows_from_text (sentence-split, <=400 char windows, alpha-fraction>=0.4 filter, dedup by hash); make_row(...) flat-metadata builder; build_content_pair / build_surface_pair; add_token_indices (AutoTokenizer offset_mapping, add_special_tokens=False, batch 512); assign_folds (pairs 70/30 train/test by pair_id stratified by (hierarchy,sub_context,row_type); corpus 50/50 train/diagnostic stratified by (hierarchy,sub_context|neg_family,output)); the async OpenRouter call_llm + generate/judge pattern; run_asserts; write_outputs (manifest + absorption_readiness); data.py orchestration (build -> aii-json format mini/preview -> validate exp_sel_data_out). Use the gemma tokenizer mirror unsloth/gemma-2-2b (gated google/gemma-2-2b may 401; the iter-1 manifest used 'google/gemma-2-2b' with HF_TOKEN — try that first, fall back to unsloth mirror). Use python3 (NOT `uv run`) exactly as data.py documents. Implement a --scale smoke path (tiny caps, ~1 min) to validate logic before the full run.

  ========================================================================
  STEP 1 — CURATE THE FOUR HOMOGRAPH GAZETTEERS (replace the country/numeric gazetteers)
  ========================================================================
  For EACH entity store a dict: {surface, target_type, competitor_sense_word(s), competitor_gloss, homograph_strength}. homograph_strength = wordfreq.zipf_frequency(lowercase_competitor, 'en') (add `wordfreq` to deps; if unavailable, fall back to a hardcoded high/med/low tag). Prefer entities with HIGH competitor Zipf (strong competing sense) AND expected target-sense pile frequency high enough for >=150 diagnostic positives.

  1A. CITIES (city_homograph_absorption). Source candidates with geonamescache: `gc = geonamescache.GeonamesCache(min_city_population=15000); gc.get_cities()` -> records with 'name','population','countrycode'. Intersect city names with a common-English-word list (use the `wordfreq` top-N English words, or nltk.corpus.words, or a small builtin set) to surface collisions, then CURATE to a clean list of well-documented homograph cities with strong competitors. Seed list (verify/extend): Phoenix (mythical bird/comeback/Joaquin Phoenix), Mobile (adjective/phone), Reading (gerund 'reading'), Bath (bathtub), Nice (adjective 'nice'), Buffalo (the animal), Hull (ship hull), Cork (bottle cork), Split (verb 'split'), Bend (verb), Worth (preposition/noun), Mercury (planet/element/Freddie Mercury), Jackson (surname/Michael Jackson), Columbus (Christopher Columbus), Cleveland (surname/Grover Cleveland), Florence (given name), Sydney (given name), Sandy (adjective/given name), Surprise (noun), Hollywood (the film industry), Paris (Greek myth/Paris Hilton), Jordan (river/Michael Jordan — place sense via West Jordan etc.), Cologne (perfume). Include ~20-28 cities; prioritize the higher-frequency ones (Phoenix, Paris, Mobile, Reading, Mercury, Jackson, Columbus, Cleveland, Buffalo, Florence) for eligibility; flag rarer ones (Hull, Cork, Split, Worth, Cologne) as likely descriptive_only.

  1B. MONTHS (month_name_absorption). Use `calendar.month_name[1:13]` for all 12. Homograph-strong: May (modal verb 'may'), March (verb 'march/marched/marching'), August (adjective 'august'=distinguished), April & June (given names), plus minor: 'Mayday', 'Marching'. All 12 are frequent in target sense (date contexts) -> all should reach eligible easily; the absorption signal of interest concentrates on May/March/August.

  1C. GIVEN NAMES (given_name_absorption). Curate names that ARE common English words with strong competitors (virtue/word names): Grace (gracefulness), Hope (hope), Faith (faith), Joy (joy), Mark (mark/to mark), Bill (invoice/bird beak), Will (modal verb 'will'/testament), Rose (flower/past tense of rise), Frank (adjective 'frank'/franking), Pat (to pat), Dawn (daybreak), Summer (season), Autumn (season), Crystal (crystal), Daisy/Lily/Violet/Ivy/Holly/Rosemary (plants), Pearl (gem), Ruby (gem/color), Art (art), Earl (nobility rank), Jack (to jack/playing card), Drew (past tense of draw), Sky (the sky), Reed (a reed), Chase (to chase), Wade (to wade), Cliff (a cliff), Dean (academic dean), Robin (the bird), Carol (a carol/to sing). Include ~25-35; prioritize high-frequency competitors (Grace, Hope, Mark, Bill, Will, Rose, Frank, Faith, Joy, Dawn, Jack, Drew, Sky, Art) for eligibility.

  1D. BRANDS (brand_homograph_absorption — the additional documented-homograph is-a hierarchy). Curate brands/companies that are common words with strong competitors: Apple (fruit), Amazon (river/rainforest/warrior), Shell (seashell), Gap (a gap), Dove (bird/past tense of dive), Target (a target/to aim), Orange (fruit/color/telecom), Subway (underground train), Tide (ocean tide), Corona (crown/sun corona), Visa (travel document), Polo (the sport), Puma/Jaguar (animals), Caterpillar (the insect), Dawn (daybreak — dish soap), Sprint (to sprint), Chase (to chase — bank), Square (a square), Oracle (a prophet), Monster (a monster), Patagonia (the region), Java (the island/coffee), Python (the snake — borderline brand/lang). Include ~22-30; prioritize Apple, Amazon, Shell, Target, Orange, Gap, Tide, Visa, Subway, Java for eligibility.

  MERGE-SAFETY across hierarchies: some tokens recur (Dawn name vs brand; Jordan city vs prior country dataset). Keep them per-hierarchy with the hierarchy-appropriate target sense; record the cross-hierarchy collision in metadata_notes. Do NOT include pure country names already covered by dataset_2 except where the city/place sense is the target (e.g. Jordan-as-place).

  ========================================================================
  STEP 2 — COMPONENT A: CONTENT-FLIP MINIMAL PAIRS (per hierarchy)
  ========================================================================
  Mirror build_content_pair: x_on = template.replace('{S}', entity) (output=positive, target sense), x_off = template.replace('{S}', off_filler) (output=negative, parent concept absent), surface-matched within the pair. CRITICAL: the carrier template must DISAMBIGUATE x_on to the TARGET sense so the positive genuinely carries the parent concept. Provide ~8-12 carriers per hierarchy whose syntax forces the target reading:
    - city: place-frame carriers — 'She flew to {S} for the conference.', 'They drove from {S} to the coast.', 'The mayor of {S} gave a speech.', 'He grew up in {S}.', '{S} is the largest city in the region.' off_filler pool = (a) NON-city places: country names / generic 'the coast','the capital','the countryside'; (b) person/company names; (c) generic noun. neg_family in {other_place, other_entity, easy}.
    - month: time-frame carriers — 'The event is scheduled for {S}.', 'They got married in {S}.', 'It happened back in {S} of that year.', 'The deadline falls in early {S}.', 'We met on {S} 14th.' off_filler pool = NON-month time words ('spring','winter','the weekend','Monday','noon','the holidays') and generic words. neg_family in {other_time, easy}.
    - given_name: person-frame carriers — '{S} smiled and waved.', 'My friend {S} just called.', 'Mr. {S} signed the form.', 'They named the baby {S}.', '{S} asked a thoughtful question.' off_filler pool = generic person references ('the teacher','my neighbor','the stranger') and non-name nouns. neg_family in {other_person_ref, easy}.
    - brand: company-frame carriers — '{S} announced a new product today.', 'Shares of {S} rose after earnings.', 'She works at {S}.', '{S} opened a new store downtown.', 'The {S} logo is famous.' off_filler pool = generic company refs ('the startup','the firm','a competitor') and non-brand nouns. neg_family in {other_company_ref, easy}.
  Build deterministically (templated) first; record metadata_template_id. Anchor target span at the {S} slot (x_on real span; x_off zero-width slot start), exactly like build_content_pair. Set metadata_sub_context = entity for x_on (positive), null for x_off (negative). Aim ~30-60 content pairs per hierarchy from templates before LLM augmentation.

  ========================================================================
  STEP 3 — COMPONENT B: SURFACE-FLIP PAIRS (per hierarchy)
  ========================================================================
  Mirror build_surface_pair: same entity in target sense, two different carriers, BOTH positive, for the unit-level surface-invariance admission check. Provide ~6 surface carriers per hierarchy (target-sense-forcing, distinct from the content carriers), pair disjoint frames per entity. Aim ~20-40 surface pairs per hierarchy.

  ========================================================================
  STEP 4 — COMPONENT C: FROZEN PILE DIAGNOSTIC CORPUS + HOMOGRAPH DISAMBIGUATION (the key new machinery)
  ========================================================================
  Stream pile-uncopyrighted exactly as iter-1 (stream_pile_corpus). For each candidate window run, per hierarchy, a high-PRECISION sense classifier that assigns ONE of: TARGET-SENSE positive (sub_context=entity), HOMOGRAPH-COMPETITOR negative (same surface token, non-target sense — the matched hard control), OTHER-ENTITY negative (a different-type entity), or EASY negative (no entity). Precision over recall: when the entity appears but NO disambiguating cue fires, EXCLUDE the window (do not mislabel). Concrete cue rules (extend as needed; all case-aware):
    - MONTH target-sense (high precision): /(?:\b(?:in|on|since|until|by|during|early|late|mid|of)\s+)(Month)\b/, /(Month)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?/, /\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(Month)\b/, /(Month)\s+\d{4}/, /(?:last|next|this)\s+(Month)/. MONTH competitor: May modal /\bMay\s+(?:I|we|you|he|she|it|they|the|not|have|be|or|well)\b/; March verb /\b[Mm]arch(?:ed|ing|es)?\b/ when NOT preceded by a date/preposition cue; August adjective /\baugust\s+(?:body|assembly|presence|institution|gathering)\b/.
    - CITY target-sense: /(?:\b(?:in|at|to|from|near|outside|downtown|visited?|toured?)\s+)(City)\b/, /(City),\s+[A-Z][a-z]+/ (City, State/Country), /(City)\s+(?:City|Airport|Station|County|metro|residents|suburb|downtown)/, /the\s+city\s+of\s+(City)/. CITY competitor: lowercase common-word hit (e.g. 'mobile','reading','bath','nice','buffalo','cork','split','worth') OR capitalized in a clearly non-place frame (e.g. 'Joaquin Phoenix', 'rise.{0,15}from the ashes', 'Mercury' + element/planet cue).
    - GIVEN-NAME target-sense: /(?:\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Lady|President|Senator|Aunt|Uncle|Saint|St)\.?\s+)(Name)\b/, /(Name)\s+[A-Z][a-z]+/ (Name + likely surname), /(?:named|called)\s+(Name)\b/, /(Name)'s\b/, /(Name)\s+(?:said|asked|replied|smiled|nodded|wrote|added)\b/. GIVEN-NAME competitor: lowercase common-word hit ('grace','hope','mark','bill','will','rose','frank','faith','joy','dawn','art','jack','drew','sky','reed','chase').
    - BRAND target-sense: /(Brand)\s+(?:Inc|Corp|Co|Ltd|announced|released|launched|unveiled|reported|shares?|stock|CEO|earnings|products?|store)/, /(Brand)'s\s+(?:new|latest|CEO|stock|shares|products|earnings)/, /(?:at|from|by|for)\s+(Brand)\s+(?:Inc|Corp|store|today)/. BRAND competitor: lowercase common-word hit ('apple','amazon','shell','gap','dove','target','orange','subway','tide','corona','visa','polo','puma','jaguar','square','java','python','monster').
  Negatives priority/abundance handled like iter-1 (positives have absolute priority; negatives fill from leftover docs). Per-entity TARGET-SENSE positive cap ~300 (=> ~150 diagnostic-fold after the 50/50 split). Set max_records high (start ~900k like iter-1; raise toward all 30 shards if eligibility is short) and an overall wall-clock guard. Use the prefer-rarest (spread across entities) priority for target positives so as many entities as possible reach the cap; collect a balanced pool of homograph_competitor + easy negatives (target a few hundred to ~2-3k each per hierarchy).
  VALIDATE THE LABELLER: after building the corpus, LLM-judge a stratified SAMPLE (~150-250 windows across hierarchies/entities) for sense-correctness and report target-sense precision per hierarchy in the manifest (this MEASURES the heuristic precision; it does NOT relabel the corpus). If sampled precision < ~0.9 for a hierarchy, TIGHTEN that hierarchy's cues (require a stronger cue / add exclusions) and rebuild — do not ship low-precision target labels.

  ========================================================================
  STEP 5 — TOKEN ANCHORING, LLM AUGMENT+JUDGE, FOLDS
  ========================================================================
  Token indices: reuse add_token_indices unchanged (gemma-2-2b offset mapping; null if tokenizer unavailable, with token_indices_present=false in manifest).
  LLM augment + judge (OpenRouter only, hard $10 cap, TARGET < $3 — iter-1 spent $0.01): reuse the async pattern. Generator = openai/gpt-4o-mini (cheap, 100% pass in iter-1) or google/gemini-3.1-flash-lite per the dossier; judge = same or anthropic/claude-haiku-4.5. EXTEND the judge rubric with a NEW boolean `sense_correct` (true iff the entity in x_on is unambiguously in its TARGET is-a sense — city/month/name/brand — given the carrier); keep content_flipped, surface_preserved, grammatical, score. metadata_llm_judge_pass = content_flipped AND surface_preserved AND grammatical AND sense_correct. Generate a modest number of diverse extra carriers per hierarchy (~20-40 each) and spot-judge ~20% of templated pairs + 100% of LLM-generated pairs; report pass rate and spend in the manifest. Track COST['usd'] after every call and STOP at the budget guard.
  Folds: reuse assign_folds unchanged (pairs by pair_id stratified by sub_context; corpus 50/50 train/diagnostic stratified). The diagnostic fold is where next iteration's parent-probe recall-hole search runs.

  ========================================================================
  STEP 6 — SCHEMA, MANIFEST, OUTPUTS, VALIDATION
  ========================================================================
  Update schema.json from the iter-1 copy: `dataset` enum = ['city_homograph_absorption','month_name_absorption','given_name_absorption','brand_homograph_absorption']; add metadata_hierarchy enum ['city','month','given_name','brand']; expand metadata_neg_family enum to include 'homograph_competitor','other_place','other_entity','other_time','other_person_ref','other_company_ref','easy'; ADD fields metadata_target_sense (e.g. 'city'|'month'|'given_name'|'brand'|'competitor'|null), metadata_competitor_sense (string, the competing word/gloss), metadata_homograph_strength (number, lowercase-competitor Zipf), metadata_entity (string canonical entity). Keep all other metadata_* keys identical to iter-1 (flat, no nested objects; patternProperties ^metadata_). Keep the logical_row_schema mirror and a top-level list of the homograph entities per hierarchy.
  Manifest (reuse write_outputs, extend): per-hierarchy templated/surface/corpus counts; corpus_positive_counts_by_sub (per entity); source_counts; pile_set_name_counts; llm_pair_pass_rate; llm sense-precision sample results per hierarchy; llm_cost_breakdown; and the absorption_readiness block: for EACH (hierarchy, entity) the diagnostic_positives count and status ('eligible' if >=150 else 'descriptive_only'). Add a design_note that labels are surface/regex/gazetteer-derived and absorption presence/absence is a future-iteration empirical finding (this corpus equally supports the spelling-specific null and a positive homograph-absorption finding). Add a prominent note: 'NEXT-ITERATION BUILDING BLOCK — not consumed by this iteration's parallel experiments.'
  Outputs via data.py: full_data_out.json + manifest.json, then aii-json format script -> full/mini/preview_data_out.json (rename), then validate against exp_sel_data_out. Run run_asserts (output<->concept_present consistency; pair role integrity x_on/x_off & surface_a/surface_b; positives have real spans; sub_context null on x_off/pure negatives; positive-input uniqueness within (row_type,hierarchy); (pair_id,role) uniqueness; target_text == input[start:end]). Use aii-file-size-limit skill to confirm each variant < 100 MB; if full exceeds, lower per-entity corpus caps or window count (do NOT silently truncate the schema). Deliver: data.py, build_dataset.py, pipeline.py, schema.json, manifest.json, full/mini/preview_data_out.json, pyproject.toml (pin requests, zstandard, transformers, loguru, aiohttp, geonamescache, wordfreq, and python-version).

  ========================================================================
  FAILURE SCENARIOS & FALLBACKS
  ========================================================================
  - An entity is too rare in TARGET sense to reach 150 diagnostic positives: flag descriptive_only and keep it (breadth for candidate search is still valuable); ensure EACH hierarchy has >=3-5 ELIGIBLE entities (months are guaranteed; pick the highest-frequency cities/names/brands). If a whole hierarchy cannot field >=3 eligible entities after scanning more shards, report that honestly in the manifest and keep it descriptive.
  - Disambiguation precision low for a hierarchy (LLM sample < ~0.9): tighten cues / add exclusions and rebuild that hierarchy; given_name and brand are the hardest — bias toward stronger cues (titles+surnames for names; corporate tokens for brands) and accept lower recall.
  - pile shard fetch fails: continue to next shard (iter-1 already handles this); ensure at least a few shards succeed.
  - gemma tokenizer gated/unavailable: set token_indices=null and token_indices_present=false; downstream can re-tokenize.
  - wordfreq unavailable: fall back to a hardcoded high/med/low homograph_strength tag per entity.
  - LLM budget pressure: skip generation, keep templated A/B pairs and the (cheap) precision-validation judge sample only; never exceed the $10 cap (stop at the internal guard).
  - Cross-hierarchy token collisions (Dawn, Jordan, Mercury): keep per-hierarchy with the correct target sense and note the collision.
target_num_datasets: 4
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_I2MrezW41iQo
type: research
title: Absorption Diagnostic + Pinned Datasets Dossier for Two-Track SAE Grouping
summary: >-
  Executor-ready dossier de-risking the C3 absorption spine and pinning every data/infra build for the two-track co-response
  SAE-grouping experiment. WP1 extracts the Chanin 2409.14507 absorption diagnostic verified against the lasr-spelling/sae-spelling
  code: parent latent = max ENCODER-cosine with an LR probe (+ k-sparse splits at f1-jump 0.03); absorber = largest-negative
  integrated-gradients ablation (IG steps=6) on the first-letter logit-diff m=g[y]-mean(g[incorrect]); decision thresholds
  probe_cos_sim_threshold=0.025 computed on the DECODER (sae.W_dec), ablation_delta_threshold=1.0, EPS=1e-8, 200-FN cap, topk=10;
  absorption_rate=num_absorptions/lr_probe_true_positives; valid only layers 0-17. It also supplies the strictly non-circular
  FORM-FREE version the paper itself gives in Appendix A.13 (and SAEBench implements as absorption_fraction): latent l absorbs
  iff tau_c < (a_hat_l . d_p)/(a . d_p) with a_hat_l = enc_act*W_dec[l] and d_p the parent-concept LR-probe direction trained
  on data DISJOINT from clustering -- works at all layers, no output logit needed, never used to form units. WP2 confirms
  absorption is empirically documented ONLY on first-letter spelling (LessWrong toy-models post; SAEBench eval id 'absorption_first_letter';
  Matryoshka/H-SAE only mitigate via the spelling metric), making Testbed-2 both a generality test and a novel empirical test;
  numeric-quantity hierarchy is recommended primary (taxonomic country alternative) with concrete non-triviality gates (parent
  recall >=0.60; >=1 absorber with firing-Jaccard<0.10, sub-context precision>=0.70, hole-coverage gain>=0.05 with bootstrap
  CI excluding 0) and an honest-null fallback that scopes C3 to spelling and routes generality through C1. WP3 pins HF datasets:
  s-nlp/paradetox (en_toxic_comment/en_neutral_comment, 19,744 rows, openrail++); google/civil_comments (text + 7 float32
  sub-attrs, 1.8M/97k/97k, CC0, 414.95MB -> subsample); tasksource/counterfactually-augmented-imdb (Text/Sentiment, no pair-ids
  -> acmi-lab GitHub for pairing, license unknown); CEBaB/CEBaB (full aspect-majority schema, license NOT on card = TODO);
  LabHC/bias_in_bios (hard_text/profession-int64-0-27/gender, 257k/39.6k/99.1k, 266MB, MIT, full alphabetical profession map).
  WP4 gives generation prompts + an independent LLM-judge rubric and verified June-2026 OpenRouter prices (generator google/gemini-3.1-flash-lite
  $0.25/$1.50 or deepseek/deepseek-v4-flash $0.09/$0.18; judge anthropic/claude-haiku-4.5 $1.00/$5.00), totalling ~$5.9-7.6
  for ~5,000 pairs with a hard $10 stop. WP5 captures sae-spelling get_alpha_tokens (convert_tokens_to_string then strip one
  leading space then all-alpha) and prompt template '{word} has the first letter:'; pins pile-uncopyrighted rev 3be9033 (2023-08-31,
  non-streaming); and SAE.from_pretrained(release='gemma-scope-2b-pt-res-canonical', sae_id='layer_12/width_16k/canonical',
  d_model=2304) + the 65k variant. CRITICAL model-diffing finding: NO gemma-scope-2b-it SAE exists anywhere (Google IT residual
  SAEs only for 9B) -> use the SHARED pt SAE on both gemma-2-2b and gemma-2-2b-it activations; both Google models are gated,
  use unsloth/gemma-2-2b(-it) mirrors. Full detail in research_report.md; every pinned fact and citation is in research_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run__C1-INh1YNGn/3_invention_loop/iter_1/gen_art/gen_art_research_2
out_dependency_files:
  file_list:
  - research_out.json

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

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
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
TODO 1. Update data.py to only include the chosen 4 datasets and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
TODO 2. Verify full_data_out.json, preview_data_out.json, and mini_data_out.json exist in your workspace (see <workspace>) and contain correct data.
TODO 3. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to full_data_out.json.
TODO 4. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DatasetExpectedFiles": {
      "description": "All expected output files from dataset artifact.",
      "properties": {
        "script": {
          "description": "Path to data.py script. Example: 'data.py'",
          "title": "Script",
          "type": "string"
        },
        "datasets": {
          "description": "Dataset file groups \u2014 one per dataset, each with full/mini/preview variants",
          "items": {
            "$ref": "#/$defs/DatasetFileSet"
          },
          "title": "Datasets",
          "type": "array"
        }
      },
      "required": [
        "script",
        "datasets"
      ],
      "title": "DatasetExpectedFiles",
      "type": "object"
    },
    "DatasetFileSet": {
      "description": "One dataset's three required output variants.",
      "properties": {
        "full": {
          "description": "Full dataset JSON file(s). Single file or split files. Example: ['full_data_out.json'] or ['full_data_out/full_data_out_1.json', 'full_data_out/full_data_out_2.json']",
          "items": {
            "type": "string"
          },
          "title": "Full",
          "type": "array"
        },
        "mini": {
          "description": "Mini dataset JSON file path (3 examples). Example: 'mini_data_out.json'",
          "title": "Mini",
          "type": "string"
        },
        "preview": {
          "description": "Preview dataset JSON file path (10 examples). Example: 'preview_data_out.json'",
          "title": "Preview",
          "type": "string"
        }
      },
      "required": [
        "full",
        "mini",
        "preview"
      ],
      "title": "DatasetFileSet",
      "type": "object"
    }
  },
  "description": "Dataset artifact \u2014 structured output + file metadata.\n\nFinds, evaluates, and prepares datasets for research experiments.\nProduces data.py and full_data_out.json files.",
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
      "$ref": "#/$defs/DatasetExpectedFiles",
      "description": "All output files you created. Must include data.py script plus dataset file groups (full/mini/preview variants)."
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
  "title": "DatasetArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [11] SYSTEM-USER prompt · 2026-06-18 03:51:53 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.terminal_claude_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.terminal_claude_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [12] SYSTEM-USER prompt · 2026-06-18 03:55:45 UTC

```
<verification_failed>
Your dataset output failed verification (attempt 1/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_data_out.json
  - Missing file: mini_data_out.json
  - Missing file: preview_data_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Use 'ls' to check what files exist, then create the missing ones.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files (data.py, full_data_out.json, preview_data_out.json, mini_data_out.json)

After making changes, verify:
- 'ls -la' shows all required files
- JSON files are valid (use aii-json skill validation)
- full_data_out.json has at least 50 examples
</task>
```

### [13] SYSTEM-USER prompt · 2026-06-18 04:00:41 UTC

```
<verification_failed>
Your dataset output failed verification (attempt 2/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_data_out.json
  - Missing file: mini_data_out.json
  - Missing file: preview_data_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Use 'ls' to check what files exist, then create the missing ones.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files (data.py, full_data_out.json, preview_data_out.json, mini_data_out.json)

After making changes, verify:
- 'ls -la' shows all required files
- JSON files are valid (use aii-json skill validation)
- full_data_out.json has at least 50 examples
</task>
```

### [14] SYSTEM-USER prompt · 2026-06-18 04:03:39 UTC

```
<verification_failed>
Your dataset output failed verification (attempt 3/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_data_out.json
  - Missing file: mini_data_out.json
  - Missing file: preview_data_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Use 'ls' to check what files exist, then create the missing ones.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files (data.py, full_data_out.json, preview_data_out.json, mini_data_out.json)

After making changes, verify:
- 'ls -la' shows all required files
- JSON files are valid (use aii-json skill validation)
- full_data_out.json has at least 50 examples
</task>
```
