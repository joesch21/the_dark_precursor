# BDP-002H Apply README — Dark Precursor CSS Split

## Purpose

This patch splits the embedded Streamlit CSS block in `frontend/dark_precursor.py` into a local stylesheet:

- `frontend/styles/dark_precursor.css`

It also moves the differential engine panel render call so Streamlit page configuration is applied first.

## Scope

- Frontend refactor only.
- No database mutation.
- No SQL migration.
- No evidence spine change.
- No generative behaviour change.

## Apply

Run from the repository root:

```bash
cd /home/joseph/Applications/the_dark_precursor/buchanan_platform_docs

unzip -o ~/Downloads/bdp_002h_dark_precursor_css_split.zip

python3 scripts/apply_bdp_002h_dark_precursor_style_split.py
python3 scripts/update_bdp_002h_dark_precursor_style_split.py
python3 scripts/verify_bdp_002h_dark_precursor_style_split.py

git status --short
git diff --stat
```

## Expected verifier output

```text
[OK] BDP-002H Dark Precursor CSS split verified
```

## Optional app smoke test

```bash
cd /home/joseph/Applications/the_dark_precursor/buchanan_platform_docs
./activate_env.sh
streamlit run frontend/dark_precursor.py
```

## Commit

```bash
git add \
  BDP_002H_APPLY_README.md \
  docs/BDP_002H_DARK_PRECURSOR_STYLE_SPLIT.md \
  frontend/dark_precursor.py \
  frontend/styles/dark_precursor.css \
  scripts/apply_bdp_002h_dark_precursor_style_split.py \
  scripts/update_bdp_002h_dark_precursor_style_split.py \
  scripts/verify_bdp_002h_dark_precursor_style_split.py \
  BUCHANAN_SYSTEM_STATE.json \
  BUCHANAN_THREAD_HANDOVER.md \
  docs/BUCHANAN_THREAD_HANDOVER.md

git commit -m "BDP-002H Split Dark Precursor stylesheet"
git push origin main
```

If either handover path does not exist, Git will ignore the missing one if you add files individually or rerun `git status --short` and add only shown files.
