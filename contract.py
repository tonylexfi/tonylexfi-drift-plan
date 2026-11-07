"""Typed declarations for the task and every tool."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Case(Enum):
    STANDARD = "standard"
    BOUNDARY = "boundary"


class Tool(Enum):
    READ_CASE = "read_case"
    WRITE_RESULT = "write_result"
    REFERENCE = "reference"


class Task(Enum):
    SOLVE = "tonylexfi-drift-plan"


class DataType(Enum):
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"


class Action(Enum):
    RETAIN = "retain"
    ADD_NULLABLE = "add_nullable"
    WIDEN_NUMBER = "widen_number"
    QUARANTINE = "quarantine"


class Reason(Enum):
    COMPATIBLE = "compatible"
    OPTIONAL_ABSENT = "optional_absent"
    NUMERIC_WIDENING = "numeric_widening"
    NEW_FIELD = "new_field"
    TYPE_CONFLICT = "type_conflict"
    REQUIRED_ABSENT = "required_absent"
    NULL_VIOLATION = "null_violation"
    UNKNOWN_NEW_TYPE = "unknown_new_type"


@dataclass
class BaselineField(Output):
    name: Annotated[str, "Unique field name"]
    type: Annotated[DataType, "Baseline scalar type"]
    nullable: Annotated[bool, "Whether nulls are allowed"]


@dataclass
class ObservedField(Output):
    name: Annotated[str, "Unique field name"]
    types: Annotated[list[DataType], "Distinct observed non-null types, empty for all-null"]
    null_count: Annotated[int, "Count of observed nulls"]


@dataclass
class CaseInput(Output):
    case: Annotated[Case, "Which reproducible fixture case to solve"]


@dataclass
class DataOutput(Output):
    case: Annotated[Case, "Case identity"]
    baseline: Annotated[list[BaselineField], "Declared baseline schema"]
    observed: Annotated[list[ObservedField], "Current batch field profile"]


@dataclass
class AnswerRow(Output):
    field: Annotated[str, "Field name"]
    action: Annotated[Action, "Required migration action"]
    reason: Annotated[Reason, "First applicable rule"]


@dataclass
class AnswerInput(Output):
    rows: Annotated[list[AnswerRow], "Complete answer rows in the required canonical order"]


@dataclass
class ResultOutput(Output):
    path: Annotated[str, "Must be result.json in the workspace"]
    count: Annotated[int, "Number of answer rows written"]


@dataclass
class ReferenceOutput(Output):
    case: Annotated[Case, "Pinned case identity"]
    data: Annotated[DataOutput, "Immutable ground-truth case snapshot"]


TOOLS = {
    Tool.READ_CASE: (CaseInput, DataOutput),
    Tool.WRITE_RESULT: (AnswerInput, ResultOutput),
    Tool.REFERENCE: (CaseInput, ReferenceOutput),
}
TASKS = {Task.SOLVE: (CaseInput, ResultOutput)}
