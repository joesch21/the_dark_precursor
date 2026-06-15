# BDP-003C — Cinematic Experience Reset

## Purpose

This patch resets `frontend/dark_precursor.py` toward the actual Dark Precursor goal:

- large readable cinematic text
- slow reveal / typewriter pacing
- concept-first immersive experience
- differential reading spine built into the prompt
- optional cinematic treatment / storyboard / film-clip brief output
- governed evidence posture retained
- CSS isolated in `frontend/styles/dark_precursor.css`

This is a frontend/generative-surface patch only.

## Apply

```bash
cd /home/joseph/Applications/the_dark_precursor/buchanan_platform_docs

unzip -o ~/Downloads/bdp_003c_cinematic_experience_reset.zip

python3 scripts/update_bdp_003c_cinematic_experience_reset.py
python3 scripts/verify_bdp_003c_cinematic_experience_reset.py

streamlit run frontend/dark_precursor.py
```

## Expected verifier result

```text
[OK] BDP-003C cinematic experience reset verified
```

## Commit

```bash
git add \
  BDP_003C_APPLY_README.md \
  docs/BDP_003C_CINEMATIC_EXPERIENCE_RESET.md \
  frontend/dark_precursor.py \
  frontend/styles/dark_precursor.css \
  scripts/update_bdp_003c_cinematic_experience_reset.py \
  scripts/verify_bdp_003c_cinematic_experience_reset.py \
  BUCHANAN_SYSTEM_STATE.json \
  ai_boot/BUCHANAN_SYSTEM_STATE.json \
  BUCHANAN_THREAD_HANDOVER.md \
  docs/BUCHANAN_THREAD_HANDOVER.md

git commit -m "BDP-003C Reset Dark Precursor cinematic experience"
git push origin main
```

If one of the optional state/handover paths does not exist, remove it from `git add`.

## Boundary

- Database mutation: false
- SQL migration: false
- Evidence spine change: false
- Buchanan claim creation: false
- Interpretation insertion: false
- Frontend/generative surface: true
- Actual video generation API integration: false
- Film/storyboard brief generation: true
