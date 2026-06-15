# Patch & Addition Workflow (Official Preferred Method)

**Status:** Official Standard  
**Date:** June 2026

## Preferred Method of Working

**Patch bundles are the official and preferred way of delivering changes on this project.**

All significant work (new features, architecture changes, documentation updates, script improvements, etc.) should be packaged and applied using controlled patch bundles (`.zip` and/or `.patch` files). This ensures traceability, governance, and clean history.

Direct editing on the main branch without going through the patch process is discouraged for anything beyond trivial fixes.

## Standard Terminal Workflow (Preferred)

### Creating a Patch Bundle

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs

# After making your changes...
zip -r bdp_003aX_descriptive_name.zip backend/ docs/ prompts/ data/ *.md *.sh

# Also create a git patch (recommended)
git diff > bdp_003aX_descriptive_name.patch

mv bdp_003aX_descriptive_name.zip ~/Downloads/
```

### Applying a Patch Bundle

```bash
cd ~/Applications/the_dark_precursor/buchanan_platform_docs
source .venv/bin/activate

unzip -o ~/Downloads/bdp_003aX_descriptive_name.zip

# Verify
python backend/scripts/verify_*.py
python backend/scripts/chat_buchanan.py "test question"

git add .
git commit -m "BDP-003A.X - Your description"
git push
```

## Rules

- Use patch bundles for all non-trivial work.
- Always include documentation updates in the bundle when required (see `DOCS_UPDATE_POLICY.md`).
- Run verifiers after applying.
- Archive old bundles in `archive/patches/`.

This is now the expected standard for future threads.
