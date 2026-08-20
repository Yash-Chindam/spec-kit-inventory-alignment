# Spec Kit Inventory Alignment

A paired Spec Kit **extension** and **preset** that replace grep-based spec alignment with a structured, script-owned inventory of requirement and task IDs.

Built for [Spec Kit issue #4164](https://github.com/github/spec-kit/issues/4164), following the extension + preset design [proposed by a maintainer](https://github.com/github/spec-kit/issues/4164#issuecomment-5348616852). Requires no changes to Spec Kit core.

## The problem

Agents find related work by grepping similar wording across `spec.md`, `plan.md`, and `tasks.md`. After a requirement is reworded — "charge on Pay" becomes "show a confirm modal" — the original line no longer matches, so the agent adds a *second* live requirement instead of updating the first. The result is silent duplicates and contradictions that `/speckit.analyze` cannot catch, because the relevant lines were never loaded into context.

## The approach

| Component | What it does |
|---|---|
| [`speckit-inventory`](speckit-inventory/README.md) | Read-only extension. Regenerates every live `FR-`/`NFR-`/`SC-`/`AC-`/`T-` ID from the existing Markdown on each run and prints JSON. Also returns a focused context pack for one task. |
| [`inventory-alignment`](inventory-alignment/README.md) | Preset. Wraps `speckit.specify` and `speckit.analyze` with a classify-against-the-inventory pre-pass, and documents the optional `covers:` task field. |

Design constraints held deliberately:

- **No second source of truth.** The inventory is derived on every run, never stored. A `tasks.yaml` ↔ `tasks.md` sync problem cannot arise.
- **No mutation.** The extension only reads.
- **No core changes.** Everything ships as an installable, opt-in bundle.
- **No embeddings.** That was Phase 2 of the original proposal and is out of scope.

## Install

```bash
specify extension add --dev /path/to/spec-kit-inventory-alignment/speckit-inventory
specify preset add --dev /path/to/spec-kit-inventory-alignment/inventory-alignment
```

Install the extension first — the preset's prompts fall through to the unmodified core workflow without it.

## Tests

```bash
python -m pytest tests -q
```

## Requirements

Spec Kit >= 0.9.0, Python 3.11+. No third-party dependencies.

## License

[MIT](LICENSE)
