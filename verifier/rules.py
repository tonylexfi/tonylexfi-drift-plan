def expected(data):
    baseline = {row.name: row for row in data.baseline}
    observed = {row.name: row for row in data.observed}
    rows = []
    for name in sorted(set(baseline) | set(observed)):
        old, new = baseline.get(name), observed.get(name)
        if new is None:
            action, reason = ("retain", "optional_absent") if old.nullable else ("quarantine", "required_absent")
        elif old is None:
            kinds = {kind.value for kind in new.types}
            if not kinds:
                action, reason = "quarantine", "unknown_new_type"
            elif len(kinds) == 1 or kinds <= {"integer", "number"}:
                action, reason = "add_nullable", "new_field"
            else:
                action, reason = "quarantine", "type_conflict"
        elif new.null_count > 0 and not old.nullable:
            action, reason = "quarantine", "null_violation"
        else:
            kinds = {kind.value for kind in new.types}
            allowed = {old.type.value} | ({"integer"} if old.type.value == "number" else set())
            if kinds <= allowed:
                action, reason = "retain", "compatible"
            elif old.type.value == "integer" and kinds <= {"integer", "number"}:
                action, reason = "widen_number", "numeric_widening"
            else:
                action, reason = "quarantine", "type_conflict"
        rows.append({"field": name, "action": action, "reason": reason})
    return {"rows": rows}
