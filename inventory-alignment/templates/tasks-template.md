## Requirement Coverage (`covers:`)

When the `inventory-alignment` preset is active, each task MAY declare which requirements it implements by appending a `covers:` field to the task line:

```text
- [ ] T014 [P] [US1] Add the payment confirmation modal in src/checkout/Confirm.tsx (covers: FR-012, SC-003)
```

- **Placement**: at the end of the task description, in parentheses.
- **Value**: a comma-separated list of live requirement IDs (`FR-`, `NFR-`, `SC-`, `AC-`) taken from `spec.md`.
- **Optional**: a task with no `covers:` field remains valid. Omit the field for setup, tooling, or refactor tasks that implement no requirement directly.

Declaring `covers:` lets the `speckit-inventory` extension return a focused context pack for a single task — the task plus only the requirements it implements — instead of loading whole artifacts. Use IDs that already exist in `spec.md`; an ID that appears only in `tasks.md` is a dangling reference and will be reported as such.
