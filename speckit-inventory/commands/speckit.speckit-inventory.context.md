---
description: "Print a focused JSON context pack for a feature task"
---

# Feature Context Pack

Use this command to load only the task and live requirement records relevant to one implementation task.

## User input

```text
$ARGUMENTS
```

Accept `feature=<path> task=T014`, or ask the user for both values when either is missing. The feature path must contain `spec.md` and `tasks.md`.

## Execution

Run the bundled read-only inventory script:

```bash
python .specify/extensions/speckit-inventory/scripts/inventory.py --feature-dir <FEATURE_DIR> --task <TASK_ID>
```

Return the JSON unchanged. Do not edit `spec.md`, `tasks.md`, or create a sidecar file. If the task has no `covers:` IDs, return the task with an empty `requirements` list and explain that the task is not linked to requirement IDs.
