# Buchanan Patch Bundle Workflow

## Purpose

This document records the preferred working method for Buchanan Platform repository changes after BDP-001H.

The platform should prefer downloadable patch bundles over ad hoc pasted scripts when a phase changes repository files.

## Preferred Method

```text
make patch bundle
→ download zip
→ unzip locally
→ apply with git apply --check
→ run verifiers
→ commit/push from local repo
```

## Why This Method

The patch bundle method keeps the operator in control of the local repository while still allowing prepared, reviewable build slices.

It gives each phase:

1. a downloadable bundle.
2. a patch file that can be checked before application.
3. an apply script that runs verification before commit.
4. local visibility through `git diff` and `git status`.
5. a clear commit boundary.

## Bundle Shape

Each phase bundle should prefer this shape:

```text
bdp_phase_patch_bundle.zip
├── bdp_phase.patch
├── apply_bdp_phase_patch.sh
└── README_BDP_PHASE_PATCH.md
```

Avoid nested duplicate bundle folders when possible.

## Safety Rule

A bundle must state whether it mutates the database.

If the phase is read-only, the apply script must confirm the database invariant before and after the patch.

If the phase applies a SQL migration, the apply script must:

1. confirm the pre-migration invariant.
2. apply the migration exactly once.
3. run the phase verifier.
4. confirm the post-migration invariant.
5. commit only after verification passes.

## Current Use

BDP-001I records this method as the preferred working pattern for the Buchanan Platform.

## BDP-001J.0 Patch Bundle Lesson

Patch bundles should remain the default working method:

```text
make patch bundle
→ download zip
→ unzip locally
→ apply with git apply --check
→ run verifiers
→ commit/push from local repo
```

Compatibility repairs should avoid brittle exact-string replacement where possible.
