# Dopemux Copilot-ready PR Queue

This document elaborates each pull request proposed in **UBERSLICER_DESIGN.md**. Use it as the implementation checklist for upcoming patches.

### Review checklist
- `pre-commit run --files <changed>` passes
- `pytest -q` succeeds
- `dopemux doctor` runs without stack-trace
- Manifest updated when paths change
- Docs updated if behaviour changes

---

## PR #1: `fix/utils-merge-hell`

Clean up utility modules and remove any leftover merge markers.

### Scope
- `utils.py`
- `cli.py`
- `tests/*`

### Tasks
1. Search the repo for merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). Remove them and restore the correct logic.
2. Unify config caching: `utils.load_config()` should load and cache the parsed YAML once. Replace all direct `yaml.safe_load(Path("config.yaml"))` calls with this helper.
3. Centralise colour handling:
   - Move colour constants and `colorize()` to a single location in `utils.py`.
   - Update other modules to import from `utils`.
4. Adjust tests to use the unified helpers.

### Acceptance
- `pytest -q` passes with no warnings.
- Source tree contains no conflict markers (`<<<<<<<`).
- Calling `dopemux` CLI prints the configured banner with colours.

---

## PR #2: `pkg-layout-refactor`

Turn the `UBERSLICER-TFE` code into an installable package under `src/dopemux_ultraslicer` and create namespace packages.

### Scope
- `pyproject.toml`
- New directory `src/dopemux_ultraslicer/`
- Imports across the repo

### Tasks
1. Create `src/dopemux_ultraslicer/__init__.py` exposing `slice()` and CLI hooks.
2. Move existing modules from `uberslicer/` into the new package with minimal renames (e.g., `validator.py`, `chunkasaurus.py`).
3. Use namespace packages (`src/dopemux_core`, `src/dopemux_ultraslicer`). Update `pyproject.toml` `packages` section accordingly.
4. Fix imports and update tests to use the new package paths.
5. Confirm `dopemux` still functions via `python -m dopemux_cli`.

### Acceptance
- `pip install -e .` installs both packages.
- Running `pytest -q` succeeds.

---

## PR #3: `config-path-absolutist`

Centralise all path configuration in `config.yaml` and ensure modules read paths only via `load_config()`.

### Scope
- `uberslicer/*`
- `scripts/*`

### Tasks
1. Extend `config.yaml` with explicit keys for `schema`, `tagged`, `logs`, and other paths referenced in code.
2. Refactor modules so absolute paths are built using this config. No hard-coded relative paths remain.
3. Update helper scripts under `scripts/` to honour the same config keys.
4. Write regression tests covering path resolution (use a temp directory).

### Acceptance
- No module contains literal paths like `"tagged/"` or `"schema/"`.
- All tests pass.

---

## PR #4: `manifest-schema-dedupe`

Deduplicate schema copies and update loader logic.

### Scope
- `schemas/*.json`
- `validator.py`

### Tasks
1. Inspect `schemas/` and remove any duplicate JSON schema files keeping the canonical version.
2. Change `validator.py` to load schema via a single helper (e.g., `get_schema(name)`).
3. Adjust tests to use the canonical path.
4. Verify `manifest.json` no longer includes removed duplicate paths.

### Acceptance
- Only one copy of each schema remains under `schemas/`.
- Validation continues to work via `pytest`.

---

## PR #5: `openai-batch-engine`

Implement asynchronous batch processing using OpenAI as described in `MUST-BUILD-API-SPEC.md`.

### Scope
- `src/dopemux_ultraslicer/api_interface.py`
- New tests covering async batch calls

### Tasks
1. Create `api_interface.py` with `process_chunks_async(chunks, phases)` implementing the spec. Use `asyncio` and `aiohttp` for HTTP calls.
2. Write mocks in tests to simulate OpenAI responses; ensure schemas are validated on response.
3. Expose a CLI command `dopemux batch INPUT` that slices and pipes chunks through the API driver.
4. Document environment variables required for API keys.

### Acceptance
- `pytest -q` including new async tests passes.
- Running `dopemux batch sample.txt` prints processed block summaries.

---

## PR #6: `cli-dopamine-upgrade`

Add dopamine‑themed sub‑commands and banner improvements.

### Scope
- `cli.py`
- `utils.py`
- `docs/`

### Tasks
1. Add sub-commands:
   - `dopemux dopamine-hit` → print a random dopamine fact.
   - `dopemux chunk FILE` → slice a single file.
   - `dopemux batch` → wrapper around the OpenAI batch engine.
2. Display coloured skull banners before each command using `utils.colorize`.
3. Update documentation with examples for each new command.

### Acceptance
- `dopemux --help` lists the new commands.
- Example commands in docs produce expected output when followed.

---

## PR #7: `dev-ux-turbo`

Improve developer experience via pre‑commit hooks, VS Code tasks, and helper scripts.

### Scope
- `.pre-commit-config.yaml`
- `scripts/`
- `docs/dev-ux.md`

### Tasks
1. Enable `black`, `ruff`, `mypy`, and manifest checks in `.pre-commit-config.yaml`.
2. Add VS Code `tasks.json` for common commands (`pytest`, `pre-commit run`, etc.).
3. Provide `scripts/fzf-select.sh` to quickly open project files via `fzf`.
4. Document dev setup in `docs/dev-ux.md`.

### Acceptance
- `pre-commit run --files <file>` works locally.
- The docs describe how to enable the tooling.

---

## PR #8: `docs-brand-sync`

Align README and roadmap with the latest rituals and add roast templates.

### Scope
- `README.md`
- `docs/Dopemux-product-roadmap.md`

### Tasks
1. Revise README to reflect new command names and dopamine rituals.
2. Update the roadmap with milestones matching sections in `UBERSLICER_DESIGN.md`.
3. Add example roast templates under `docs/` referenced by the CLI.

### Acceptance
- Markdown renders cleanly (`pre-commit` markdownlint passes if configured).
- README instructions match the current CLI behaviour.

---

### 🔨 Developer friction killers (bake into PRs)

* **One-line bootstrap:**

  ```bash
  make dev   # sets venv, installs dev deps, pre-commit hooks
  ```
* **`dopemux doctor`** prints actionable drift report + roast instead of silent fail.
* **Colour constants** live in `config.yaml → colors:`; CLI calls `utils.colorize`.
* **`pytest -q` in 1 s**: mark slow OpenAI tests with `@pytest.mark.slow` and skip by default.
* **fzf helpers** (`scripts/fzf-blocks.sh`) let devs fuzzy-open any block/devlog entry instantly.

### 🚀 OpenAI Batch Sprint (after PR #5 lands)

1. **ENV wiring:** copy `.env.example`, export `OPENAI_API_KEY`.
2. **Async runner:** `dopemux batch blocks/ --phase phase1 --workers 8`.
3. **Devlog integration:** Every 100 blocks ⇒ `log_dev("batch-progress", ["100/… processed"])`.
4. **Fail-fast:** On schema-drift → write patch block, continue; overall job never dies dumb.
5. **Metrics:** Summarise latency, cost, drift % to `logs/batch-summary-YYYYMMDD.yaml`.

### 📋 Road-map delta (post-approval)

| Week    | Milestone                                           |
| ------- | --------------------------------------------------- |
| **0-1** | Merge PR #1-#3, CI green                            |
| **2**   | Package refactor (PR #2) released on internal PyPI  |
| **3-4** | PR #4 & #5 → first async batch run on 5 k-block log |
| **5**   | Dopamine-upgraded CLI + dev-UX turbo PRs merged     |
| **6**   | Public beta of Dopemux 1.5 w/ OpenAI pipeline       |
