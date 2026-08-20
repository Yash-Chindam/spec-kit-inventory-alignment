---
description: "Consult the inventory before creating or updating requirements"
strategy: wrap
---

## Inventory alignment pre-pass

If `speckit-inventory` is installed, run `speckit.speckit-inventory.list` for the active feature and inspect the read-only JSON inventory before writing requirements.

Classify each proposed requirement against the complete live set:

- **Already true** — an existing requirement already covers it. Do not restate it.
- **Edit existing** — it refines or rewords an existing requirement. Update that requirement in place and preserve its ID.
- **Conflict** — it contradicts an existing requirement. Surface both IDs and ask the user to resolve before writing.
- **Genuinely new** — nothing in the inventory covers it. Assign the next free ID.

Match on meaning, not wording: a reworded requirement ("show a confirm modal" vs "charge on Pay") is an edit, not a new requirement. Never create a second live requirement for behavior an existing ID already owns.

If the extension is not installed, continue with the core workflow unchanged.

{CORE_TEMPLATE}
