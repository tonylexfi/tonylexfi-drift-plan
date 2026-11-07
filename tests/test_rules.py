from dataclasses import replace

from contract import Case, CaseInput, DataType
from plugin.read_case import read_case
from verifier.rules import expected


def test_boolean_is_not_numeric(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    old = data.baseline[0]
    new = replace(data.observed[0], types=[DataType.BOOLEAN])
    assert expected(replace(data, baseline=[old], observed=[new])) == {
        "rows": [{"field": "id", "action": "quarantine", "reason": "type_conflict"}]
    }


def test_nullable_all_null_existing_field_is_compatible(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    old = data.baseline[1]
    new = replace(data.observed[1], types=[], null_count=5)
    assert expected(replace(data, baseline=[old], observed=[new]))["rows"][0]["action"] == "retain"


def test_null_violation_precedes_type_conflict(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    new = replace(data.observed[0], types=[DataType.STRING], null_count=1)
    assert expected(replace(data, baseline=[data.baseline[0]], observed=[new]))["rows"][0]["reason"] == "null_violation"


def test_new_mixed_types_are_quarantined(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    assert expected(replace(data, baseline=[], observed=[data.observed[2]]))["rows"][0]["reason"] == "type_conflict"
