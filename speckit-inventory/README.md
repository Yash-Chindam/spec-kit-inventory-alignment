# Spec Inventory Extension

`speckit-inventory` is a read-only, opt-in extension implementing the Phase 1 primitive discussed in [Spec Kit issue #4164](https://github.com/github/spec-kit/issues/4164).

It regenerates every live `FR-`, `NFR-`, `SC-`, `AC-`, and `T-` ID from the existing `spec.md` and `tasks.md` on each run and prints JSON. There is no sidecar file, no mutation, and no second source of truth — so a `tasks.yaml` ↔ `tasks.md` sync problem cannot arise. Embeddings are intentionally out of scope.

## Install

From the published release:

```bash
specify extension add speckit-inventory --from https://github.com/Yash-Chindam/spec-kit-inventory-alignment/releases/download/v0.1.0/speckit-inventory.zip
```

Or from a local checkout:

```bash
specify extension add --dev /path/to/speckit-inventory
```

## Commands

### `speckit.speckit-inventory.list`

Prints the complete inventory of live requirement and task IDs for a feature.

```text
speckit.speckit-inventory.list feature=specs/my-feature
```

### `speckit.speckit-inventory.context`

Prints a focused context pack — one task plus only the requirements that task covers — instead of a whole-file dump.

```text
speckit.speckit-inventory.context feature=specs/my-feature task=T014
```

Task IDs are matched leniently: `T014`, `T14`, `t14`, and `TASK-14` all resolve to the same record.

## Output

Every record reports the `source` artifact it was found in:

```json
{
  "schema_version": "1",
  "feature_dir": "specs/my-feature",
  "requirements": [
    { "id": "FR-001", "source": "spec.md", "line": 12, "text": "- FR-001: Charge on Pay" }
  ],
  "tasks": [
    { "id": "T014", "source": "tasks.md", "line": 40, "text": "Add confirm modal (covers: FR-001)", "covers": ["FR-001"] }
  ]
}
```

`spec.md` is scanned first, so it wins as the definition site. A requirement whose `source` is `tasks.md` is referenced by a task but never defined in the spec — a dangling reference worth reporting.

## Hooks

Optional `before_specify` and `before_analyze` hooks offer to load the inventory before those commands run. Both are `optional: true`, so they prompt rather than execute automatically.

## Companion preset

The [`inventory-alignment`](../inventory-alignment/README.md) preset wraps `speckit.specify` and `speckit.analyze` with a classify-against-the-inventory pre-pass, and documents the optional `covers:` task field this extension reads.

## Requirements

Python 3.11+. No third-party dependencies.
