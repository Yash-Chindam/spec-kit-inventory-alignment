# Inventory Alignment Preset

This opt-in preset wires the read-only [`speckit-inventory`](../speckit-inventory/README.md) extension into the core flow, implementing the Phase 1 alignment behavior discussed in [Spec Kit issue #4164](https://github.com/github/spec-kit/issues/4164).

## Install

Install the companion extension first — the preset's prompts are inert without it:

```bash
specify extension add --dev /path/to/speckit-inventory
specify preset add --dev /path/to/inventory-alignment
```

> [!NOTE]
> `preset.yml`'s `requires:` can only declare `speckit_version`, so there is no formal "requires extension X" dependency to enforce this pairing. The wrappers degrade safely: if the extension is absent, the core workflow runs unchanged and the inventory checks are skipped.

## What it changes

| Target | Strategy | Effect |
|---|---|---|
| `speckit.specify` | `wrap` | Prepends a pre-pass that loads the inventory and classifies each proposed requirement as already-true, edit-existing, conflict, or genuinely-new before writing. |
| `speckit.analyze` | `wrap` | Prepends a pre-pass that loads the complete ID set as an input to cross-artifact coverage and conflict review. |
| `tasks-template` | `append` | Documents the optional `covers:` field that links a task to the requirement IDs it implements. |

Both command overrides use the `{CORE_TEMPLATE}` placeholder and fall through to the original command body.

## When to use it

Use this preset when requirements are frequently reworded and you want an explicit alignment step, rather than relying on an agent grepping for similar wording. Do not use it if you want the unmodified core prompts.

The preset adds no embeddings, changes no core files, and introduces no second source of truth.
