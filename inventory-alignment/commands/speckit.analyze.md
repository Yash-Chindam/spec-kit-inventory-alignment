---
description: "Use the inventory as a complete input to cross-artifact analysis"
strategy: wrap
---

## Inventory alignment pre-pass

If `speckit-inventory` is installed, run `speckit.speckit-inventory.list` for the active feature and load the complete read-only inventory before analyzing artifacts.

Use it as a complete input rather than a hint:

- Include every inventory record in the coverage and conflict review — do not rely on grep to find related wording.
- Report any requirement or task ID present in one artifact but absent from the others.
- Treat a requirement whose `source` is `tasks.md` as a dangling reference: a task covers an ID that `spec.md` never defines.
- Report requirements that no task covers as uncovered.

If the extension is not installed, continue with the core workflow unchanged.

{CORE_TEMPLATE}
