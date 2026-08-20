---
description: "Print the complete read-only JSON inventory of live requirement and task IDs"
---

# Live Inventory

Use this command to load every live `FR-`, `NFR-`, `SC-`, `AC-`, and `T-` ID for a feature before adding or reclassifying requirements.

## User input

```text
$ARGUMENTS
```

Accept `feature=<path>`, or infer the active feature directory when the argument is missing. The feature path must contain `spec.md`; `tasks.md` is optional and is treated as empty when absent.

## Execution

Run the bundled read-only inventory script:

```bash
python .specify/extensions/speckit-inventory/scripts/inventory.py --feature-dir <FEATURE_DIR>
```

Return the JSON unchanged. Do not edit `spec.md` or `tasks.md`, and do not create a sidecar file.

Each record reports the `source` artifact it was found in. A requirement whose `source` is `tasks.md` is referenced by a task but never defined in `spec.md` — report it as a dangling reference rather than treating it as a live requirement.
