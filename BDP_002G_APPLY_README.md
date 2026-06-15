# BDP-002G Patch Bundle — Differential Reading Engine

## Purpose

This patch puts the core thesis into the Buchanan application as a governed, reusable operating contract:

> The platform is not merely a Deleuze/Buchanan database. It is a differential reading engine.

The patch is deliberately conservative:
- no database mutation
- no SQL migration
- no canonical passage insertion
- no interpretation insertion
- no Buchanan-specific claim creation
- no forced frontend modification

It adds the doctrine, LLM prompt contract, reusable analysis card schema, optional Streamlit panel module, and update/verify scripts.

## Files Added

- `docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md`
- `prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md`
- `data/templates/differential_analysis_card.schema.json`
- `data/templates/differential_analysis_card_social_media_feed.example.json`
- `frontend/differential_engine_panel.py`
- `scripts/update_bdp_002g_differential_engine.py`
- `scripts/verify_bdp_002g_differential_engine.py`

## Apply

From the Buchanan repo root:

```bash
cd /home/joseph/Applications/the_dark_precursor/buchanan_platform_docs

unzip -o ~/Downloads/bdp_002g_differential_reading_engine.zip

python3 scripts/update_bdp_002g_differential_engine.py
python3 scripts/verify_bdp_002g_differential_engine.py

git status --short
git diff --stat
```

## Optional frontend integration

This patch adds a standalone Streamlit panel module but does not edit `frontend/dark_precursor.py`.

After review, you can manually wire it into the Dark Precursor with:

```python
from differential_engine_panel import render_differential_engine_panel
render_differential_engine_panel()
```

Use the import pattern that matches the existing frontend file structure.

## Commit

```bash
git add \
  BDP_002G_APPLY_README.md \
  docs/BDP_002G_DIFFERENTIAL_READING_ENGINE.md \
  prompts/BUCHANAN_DIFFERENTIAL_READING_SYSTEM_PROMPT.md \
  data/templates/differential_analysis_card.schema.json \
  data/templates/differential_analysis_card_social_media_feed.example.json \
  frontend/differential_engine_panel.py \
  scripts/update_bdp_002g_differential_engine.py \
  scripts/verify_bdp_002g_differential_engine.py \
  BUCHANAN_SYSTEM_STATE.json \
  BUCHANAN_THREAD_HANDOVER.md

git commit -m "BDP-002G Add differential reading engine contract"
git push origin main
```

## Expected verifier result

```text
[OK] BDP-002G differential reading engine contract verified
```
