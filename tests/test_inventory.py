"""Tests for the community inventory extension's read-only parser."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "speckit-inventory" / "scripts" / "inventory.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("inventory", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(name="inventory_module")
def _inventory_module():
    return _load_module()


def _write_feature(tmp_path: Path, spec: str, tasks: str) -> Path:
    feature_dir = tmp_path / "feature"
    feature_dir.mkdir()
    (feature_dir / "spec.md").write_text(spec, encoding="utf-8")
    (feature_dir / "tasks.md").write_text(tasks, encoding="utf-8")
    return feature_dir


def test_inventory_extracts_unique_requirements_and_tasks(
    tmp_path: Path, inventory_module
) -> None:
    """Inventory output keeps stable IDs and source context."""
    feature_dir = _write_feature(
        tmp_path,
        "## Requirements\n- FR-001: Search\n- FR-001: duplicate mention\n- SC-002: Fast\n",
        "- [ ] T001 [US1] Implement search (covers: FR-001)\n"
        "- [ ] T001 duplicate\n"
        "- [ ] T002 Add tests (covers: SC-002)\n",
    )

    inventory = inventory_module.build_inventory(feature_dir)

    assert [item["id"] for item in inventory["requirements"]] == ["FR-001", "SC-002"]
    assert [item["id"] for item in inventory["tasks"]] == ["T001", "T002"]
    assert inventory["tasks"][0]["covers"] == ["FR-001"]


def test_requirements_defined_in_spec_win_over_task_references(
    tmp_path: Path, inventory_module
) -> None:
    """`spec.md` is the definition site; `tasks.md`-only IDs are still reported."""
    feature_dir = _write_feature(
        tmp_path,
        "- FR-001: Search\n",
        "- [ ] T001 Implement (covers: FR-001, NFR-009)\n",
    )

    by_id = {
        item["id"]: item
        for item in inventory_module.build_inventory(feature_dir)["requirements"]
    }

    assert by_id["FR-001"]["source"] == "spec.md"
    # NFR-009 is referenced by a task but never defined, so it surfaces as dangling.
    assert by_id["NFR-009"]["source"] == "tasks.md"


@pytest.mark.parametrize("requested", ["T014", "T14", "t14", "TASK-14"])
def test_context_pack_accepts_equivalent_task_id_spellings(
    tmp_path: Path, inventory_module, requested: str
) -> None:
    """Unpadded and prefixed task IDs resolve to the same canonical record."""
    feature_dir = _write_feature(
        tmp_path,
        "FR-001 Search\nFR-002 Export\n",
        "- [ ] T14 Search (covers: FR-001)\n",
    )

    inventory = inventory_module.build_inventory(feature_dir)
    pack = inventory_module.context_pack(inventory, requested)

    assert pack["task"]["id"] == "T014"
    assert [item["id"] for item in pack["requirements"]] == ["FR-001"]


def test_context_pack_rejects_unknown_and_malformed_task_ids(
    tmp_path: Path, inventory_module
) -> None:
    """A missing task raises `LookupError`; a numberless ID raises `ValueError`."""
    feature_dir = _write_feature(tmp_path, "FR-001 Search\n", "- [ ] T001 Search\n")
    inventory = inventory_module.build_inventory(feature_dir)

    with pytest.raises(LookupError):
        inventory_module.context_pack(inventory, "T999")

    with pytest.raises(ValueError):
        inventory_module.context_pack(inventory, "Txx")


def test_task_without_covers_yields_empty_requirement_list(
    tmp_path: Path, inventory_module
) -> None:
    """An unlinked task is valid and returns no requirements."""
    feature_dir = _write_feature(tmp_path, "FR-001 Search\n", "- [ ] T003 Configure CI\n")

    inventory = inventory_module.build_inventory(feature_dir)
    pack = inventory_module.context_pack(inventory, "T003")

    assert pack["task"]["covers"] == []
    assert pack["requirements"] == []


def test_missing_tasks_file_is_treated_as_empty(tmp_path: Path, inventory_module) -> None:
    """`tasks.md` is optional, so a spec-only feature still produces an inventory."""
    feature_dir = tmp_path / "feature"
    feature_dir.mkdir()
    (feature_dir / "spec.md").write_text("- FR-001: Search\n", encoding="utf-8")

    inventory = inventory_module.build_inventory(feature_dir)

    assert [item["id"] for item in inventory["requirements"]] == ["FR-001"]
    assert inventory["tasks"] == []
