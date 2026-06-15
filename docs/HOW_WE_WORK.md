# How We Work

**This document must be read by every new thread before starting work.**

## Core Rule

**All changes must be delivered as patch bundles.**

We do **not** edit files directly on `main`. All development happens through controlled patch bundles (zip files) that are created, downloaded, applied, and verified using the terminal.

## Patch Workflow (Mandatory)

1. Do your work locally
2. Create a patch bundle (`zip` or `.patch`)
3. Download the patch to your machine
4. Apply it using `unzip` or `git apply`
5. Verify the changes work correctly
6. Update relevant documentation (see `docs/DOCS_UPDATE_POLICY.md`)
7. Commit and push

See: `docs/WORKFLOW_PATCH_APPLICATION.md` for the full process.

## Documentation Updates

Documentation is **not optional**. When you change architecture, control surfaces, or how the application works, you **must** update the relevant documents (especially `BUCHANAN_THREAD_HANDOVER.md`, `BUCHANAN_SYSTEM_STATE.json`, and the corresponding BDP phase document).

## New Threads

New threads must read the following in order:

1. `docs/HOW_WE_WORK.md` (this document)
2. `docs/NEW_THREAD_ONBOARDING.md`
3. `BUCHANAN_THREAD_HANDOVER.md`
4. `docs/DOCS_UPDATE_POLICY.md`

## Summary

- Patch bundles only
- Terminal-based workflow
- Documentation is mandatory
- Governance first

Failure to follow this process breaks the integrity of the project.
