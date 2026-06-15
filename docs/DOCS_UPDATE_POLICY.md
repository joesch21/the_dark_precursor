# Documentation Update Policy (Mandatory)

**Status:** Governing Rule
**Version:** 1.0
**Date:** June 2026

## Core Principle

Documentation is not optional. It is part of the evidence spine and governance of the Buchanan Deleuze Intelligence Platform.

Any significant change to architecture, control surfaces, generative behaviour, data models, or user-facing surfaces **must** be reflected in the documentation before the work is considered complete.

## Mandatory Documents

These documents **must** be consulted and updated when relevant changes occur:

| Priority | Document                                      | When to Update                                      | Owner                  |
|----------|-----------------------------------------------|-----------------------------------------------------|------------------------|
| 1        | `BUCHANAN_THREAD_HANDOVER.md`                 | End of every significant phase or thread            | Always                 |
| 2        | `BUCHANAN_SYSTEM_STATE.json`                  | When phases, invariants, next steps, or boundaries change | Always            |
| 3        | `BDP_003A_GENERATIVE_LAYER_FOUNDATION.md`     | When generative layer logic, prompts, or boundaries change | Generative work   |
| 4        | `docs/BDP_002F_KEY_PASSAGES_REVIEWED.md`      | When new passages are reviewed or added             | Passage review work    |
| 5        | `BUCHANAN_ARCHITECTURE.md`                    | When high-level architecture or layer responsibilities change | Architecture changes |
| 6        | `BUCHANAN_SEMANTIC_WORKBENCH.md`              | When workbench surfaces or readback logic change    | Workbench changes      |
| 7        | `docs/DOCS_UPDATE_POLICY.md`                  | When this policy itself changes                     | Policy changes         |

## Pre-Thread Requirements (Mandatory)

**Before starting any new thread or major phase, the developer must:**

1. Read the latest version of `BUCHANAN_THREAD_HANDOVER.md`
2. Review the current state in `BUCHANAN_SYSTEM_STATE.json`
3. Consult the relevant phase or architecture documents
4. Confirm understanding of current boundaries and invariants

**After completing work, the developer must:**

1. Update `BUCHANAN_THREAD_HANDOVER.md` with a clear, structured summary of what was done
2. Update `BUCHANAN_SYSTEM_STATE.json` (phases, invariants, next recommended step)
3. Update any other affected mandatory documents listed above
4. Run relevant verifiers before marking the thread as complete

## Patch & Addition Workflow (Terminal Controlled)

All changes to the platform should preferably be delivered and applied using **patch bundles** for traceability and control.

### Recommended Terminal Workflow

```bash
# 1. Make changes locally in your working directory
# 2. Create a patch bundle (zip or tar.gz)
zip -r bdp_003aX_feature_name.zip backend/ docs/ prompts/ scripts/ *.md

# 3. (Optional but recommended) Create a git patch as well
git diff > bdp_003aX_feature_name.patch

# 4. Move the bundle to a safe location or upload it
mv bdp_003aX_feature_name.zip ~/Downloads/

# --- On the receiving / main machine ---

# 5. Download the bundle
cd ~/Applications/the_dark_precursor/buchanan_platform_docs

# 6. Extract / apply the patch
unzip -o ~/Downloads/bdp_003aX_feature_name.zip
# or
tar -xzf ~/Downloads/bdp_003aX_feature_name.tar.gz

# 7. Verify the changes
python backend/scripts/verify_*.py

# 8. Test functionality
python backend/scripts/chat_buchanan.py "test question"

# 9. Commit the changes (recommended)
git add .
git commit -m "BD XXX - Description of change"
git push
```

### Rules for Patch Application

- Always extract patches while inside the project root.
- Run verifiers after applying patches.
- Never apply patches that would break the current verified invariants without explicit discussion.
- Major architectural changes should be delivered with both a zip bundle **and** a `.patch` file when possible.

## Enforcement

- No major change is considered complete until the relevant documentation has been updated.
- Future threads will assume the documentation reflects the current state of the platform.
- Incomplete documentation from a previous thread is considered a governance gap that should be addressed before new work begins.

**Maintaining documentation is a non-negotiable part of the development process.**
