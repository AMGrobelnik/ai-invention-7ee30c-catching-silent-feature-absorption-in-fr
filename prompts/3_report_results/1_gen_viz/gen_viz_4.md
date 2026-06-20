# gen_viz_4 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `run__C1-INh1YNGn` — Catching Silent Feature Absorption in Frozen Sparse Autoencoders: Label-Free Loc
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_viz_4` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-06-19 03:15:00 UTC

````
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

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
Your workspace: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/4_gen_paper_repo/_2_gen_viz/gen_viz_4`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/4_gen_paper_repo/_2_gen_viz/gen_viz_4/`:
GOOD: `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/4_gen_paper_repo/_2_gen_viz/gen_viz_4/file.py`, `/ai-inventor/aii_data/runs/run_4i-Wywa44JXf/4_gen_paper_repo/_2_gen_viz/gen_viz_4/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Generate a publication-quality figure for a top-tier venue research paper that exactly follows the provided specification.

Use the aii-image-gen skill (Gemini 3 Pro Image / Nano Banana Pro) to generate the figure in the aspect ratio from the spec. Be as detailed as possible in your image generation prompt: include all data values, axis labels, ranges, legend entries, preferred colors, and describe where each element should be positioned.

IMPORTANT — Two-phase workflow: explore cheaply at 1K, then finalize at 2K. Create a subfolder `fig4_all/` in your workspace for ALL attempts.

PHASE 1 — Explore at 1K (HARD LIMIT: 5 attempts):
- Generate at `--image-size 1K` (fast and cheap). Save attempts as `fig4_all/fig4_v0_it1.jpg`, `fig4_all/fig4_v0_it2.jpg`, … up to `_it5.jpg`.
- After EACH attempt, read the image back and verify it against the checklist below. If it has issues, regenerate with a corrected prompt.
- Do AT MOST 5 generations in this phase — stop early as soon as one is clean. Then pick the single best 1K attempt (the "chosen base").

PHASE 2 — Finalize at 2K (EXACTLY 2 upscale passes of the chosen base):
- Run EXACTLY TWO generations at `--image-size 2K`, each in edit mode passing the chosen base as the input image (`--edit` the chosen base .jpg). Instruct it to upscale and sharpen while preserving the exact layout, data values, labels, and composition — and to fix any remaining issues from the checklist.
- Save them as `fig4_all/fig4_v0_2k_1.jpg` and `fig4_all/fig4_v0_2k_2.jpg`.
- Read both back, verify both, and choose the better of the two as the final figure.

DELIVERABLE:
- Copy ONLY the chosen final 2K image to your workspace root as: fig4_v0.jpg
- The file `fig4_v0.jpg` is the deliverable — everything in `fig4_all/` is reference only.

Verification checklist (apply after EVERY generation in BOTH phases). Check for:
- Layout issues (e.g. text too close together, figure looks cluttered, elements crammed into corners)
- Overlapping or touching labels, legends, or annotations
- Cut-off or truncated text, axis labels, or titles
- Wrong or missing data values, bars, lines, or data points
- Incorrect axis ranges, tick marks, or scales
- Missing or misplaced legend entries
- Blurry text, unreadable font sizes, or poor contrast
- Wrong font family (MUST be sans-serif like Helvetica/Arial — reject any serif fonts like Times New Roman)

In Phase 1, if ANY issue is found — even minor — regenerate with a corrected prompt (within the 5-attempt limit). Do NOT accept a figure with problems as the chosen base.
</task>

<figure_specification>
Figure ID: fig4
Title: Absorber catalog across a four-SAE Gemma Scope suite
Caption: Absorption-structured counts across width $\{16$k$,65$k$\}$ and layer $\{9,12\}$. Absorption is far more prevalent at the earlier layer 9 (strict 6->15 at 16k, 3->29 at 65k going L12->L9) and wider at 65k (relaxed breadth). The 16k/L12 config reproduces the shipped screen bit-exactly (6/110 strict).
Image Generation Description: Grouped bar chart, white background, sans-serif font. X-axis four configurations in this order: '16k / L12', '65k / L12', '16k / L9', '65k / L9'. Two bars per config: 'strict-structured (/110 eligible)' in dark green, and 'relaxed-structured (/336)' in light green. Strict values: 6, 3, 15, 29. Relaxed values: 31, 62, 52, 58. Left y-axis 'count' 0 to 65. Annotate the '16k / L12' group 'reproduces shipped screen bit-exact (336/336)'. Draw a bracket over the two L9 configs labeled 'LAYER effect: earlier layer absorbs MORE'. Draw a bracket over the two 65k configs labeled 'WIDTH effect: wider = more breadth'. Add a small text box bottom-right: 'Stability: 131 tokens structured somewhere; 8 persistent across >=3 configs (Amazon, Jordan in all 4); 69 config-specific'. Aspect ratio 16:9.
Aspect Ratio: 21:9
Summary: Catalog bar chart of strict/relaxed absorption counts across the four SAE configs, showing strong layer and width effects and the bit-exact screen reproduction.
</figure_specification>

<critical_requirements>
1. Accurately represent ALL data values described above — include every number mentioned
2. Do NOT invent additional data points beyond what is described
3. Include clear axis labels only if the figure has axes (not for diagrams/flowcharts)
4. FONT: ALL text MUST use sans-serif font (Helvetica/Arial). NO serif fonts (Times New Roman). Always include "Sans-serif font throughout (Helvetica/Arial style, NOT Times New Roman)" in your image generation prompt. This is the #1 most common issue — check it first during verification
5. Publication camera-ready style: white backgrounds, properly formatted axes, no 3D effects/shadows/gradients. Follow aii-image-gen skill for image generation, prompting best practices, and figure type templates
6. TEXT SPACING: Ensure generous spacing between ALL text labels. Labels MUST NOT overlap or touch. Use large readable font sizes (minimum 12pt equivalent). If labels would overlap, stagger them vertically, use leader lines, or abbreviate. For multi-panel figures, add clear padding between panels
7. RESOLUTION: Explore at 1K (Phase 1), then finalize with two 2K upscale passes of the chosen base (Phase 2) — see the two-phase workflow above. Do NOT use 4K. For multi-panel or detail-heavy figures, use wider aspect ratios to give elements room
8. MANDATORY VERIFICATION: After EVERY generation attempt, read the image and check font first (sans-serif?), then layout, data accuracy, and readability. If anything is wrong, regenerate. Do NOT stop at the first attempt
</critical_requirements>


---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Short descriptive title for the generated figure (roughly 30-90 characters)",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `./.terminal_claude_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-19 03:15:00 UTC

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

### [3] SKILL-INPUT — aii-image-gen · 2026-06-19 03:15:04 UTC

The agent loaded the **aii-image-gen** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-image-gen
description: AI image generation and editing via Gemini API (gemini-3-pro-image-preview). Generate and edit images with aspect ratio control, retries, and parallel batch support. Use for research figures, diagrams, illustrations, and any visual content.
---

# Image Generation & Editing (nano_banana)

Generate images via Gemini API through the ability server. The API key lives on the ability server — this skill routes requests through `call_server()`.

## Setup

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-image-gen"
G="$SKILL_DIR/scripts/image_gen_nano_banana.py"
PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

## Generate Image

```bash
$PY $G --prompt "prompt describing the image" --output output.jpg --aspect-ratio 16:9
```

## Edit Image

```bash
$PY $G --edit input.jpg --prompt "Make the background blue" --output edited.jpg
```

**Parameters:**
- `--prompt` / `-p` (required) — image description or edit instruction
- `--output` / `-o` (default: `./generated_image.jpg`) — output file path (always saved as `.jpg`; suffix is forced)
- `--edit` — path to source image for editing (omit for generation)
- `--aspect-ratio` (default: `16:9`) — valid: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- `--image-size` (default: `1K`) — resolution: `1K`, `2K`, `4K`
- `--style neurips` — appends NeurIPS academic style guidance
- `--negative-prompt` — things to exclude from the image
- `--system` — system-level style instruction

## Parallel Batch Generation

Use GNU `parallel` for multiple images:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-image-gen"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
export G="$SKILL_DIR/scripts/image_gen_nano_banana.py"
parallel -j 5 -k --group --will-cite 'eval {}' ::: \
  "\$PY \$G -p \"prompt 1\" -o output_1.jpg --aspect-ratio 21:9" \
  "\$PY \$G -p \"prompt 2\" -o output_2.jpg --aspect-ratio 16:9" \
  "\$PY \$G -p \"prompt 3\" -o output_3.jpg --aspect-ratio 1:1"
```

## Preview

Do **NOT** open generated images in a GUI viewer (`loupe`, `xdg-open`, `eog`,
etc.). This skill is for automated / headless generation (e.g. pipeline figure
steps), and popping image windows clutters the user's desktop. Inspect images
programmatically if needed (read the file, check the returned JSON), not by
opening a viewer.

For interactive, human-curated review of multiple figure variants — where the
user wants to arrow-navigate batches in `loupe` — use the
`amg-iter-image-gen-human` skill instead; loupe-driven review is its job, not
this one's.

## Features

- **Model**: `gemini-3-pro-image-preview` (fallback: `gemini-3.1-flash-image-preview`)
- **Auth**: API key on ability server (routed via `call_server()`)
- **Retries**: 3 attempts with exponential backoff, then fallback model
- **Edit mode**: Edit existing images with text instructions
- **Parallel**: GNU `parallel` with `-j 5` for batch generation
- **Headless**: never auto-opens a viewer (use `amg-iter-image-gen-human` for human review)

## Prompting Tips

- Include ALL numeric values explicitly (axis ranges, bar values, labels)
- Specify colors, fonts, layout, and what to exclude
- Use `--style neurips` for academic papers
- For data figures: list every data point, axis label, legend entry
- 1K resolution is default and most reliable

## Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| `21:9` | Ultra-wide panoramic (presentations) |
| `16:9` | Wide (slides, video) |
| `4:3` | Standard |
| `1:1` | Square (social, heatmaps) |
| `9:16` | Vertical (stories, posters) |

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
