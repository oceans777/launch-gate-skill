#!/usr/bin/env python3
"""根据检查状态计算上线门禁结论。

输入 JSON 对象：
{"production_go_live": true, "checks": [
  {"id": "LG-SITE-01", "tier": "P0", "critical": true, "status": "pass"}
]}

状态只允许 pass、fail、not-verified、not-applicable。
tier 只允许 P0、P1、N/A。N/A 档必须是 not-applicable。
至少要有一项 P0。结论与 SKILL.md 一致；两边冲突时先改本脚本。
"""

import json
import sys

STATUSES = ("pass", "fail", "not-verified", "not-applicable")
TIERS = ("P0", "P1", "N/A")
CLOSED = ("pass", "not-applicable")


def evaluate(checks, production_go_live):
    if not isinstance(checks, list) or not checks:
        raise ValueError("checks must be a non-empty list")
    if not isinstance(production_go_live, bool):
        raise ValueError("production_go_live must be a boolean")

    blocked = False
    warnings = False
    saw_p0 = False
    for item in checks:
        if not isinstance(item, dict):
            raise ValueError("each check must be an object")
        tier = item.get("tier")
        status = item.get("status")
        critical = item.get("critical", False)
        check_id = item.get("id", "")
        if tier not in TIERS:
            raise ValueError("invalid tier for %s" % check_id)
        if status not in STATUSES:
            raise ValueError("invalid status for %s" % check_id)
        if not isinstance(critical, bool):
            raise ValueError("critical must be a boolean for %s" % check_id)
        if tier == "N/A":
            if status != "not-applicable":
                raise ValueError("N/A tier must be not-applicable: %s" % check_id)
            if critical:
                raise ValueError("N/A tier cannot be critical: %s" % check_id)
            continue
        if tier == "P1" and critical:
            raise ValueError("P1 cannot be critical: %s" % check_id)
        if tier == "P0":
            saw_p0 = True
            if status == "fail":
                blocked = True
            elif status == "not-verified" and critical and production_go_live:
                blocked = True
            elif status == "not-verified":
                warnings = True
            elif status not in CLOSED:
                raise ValueError("unhandled P0 status for %s" % check_id)
        elif status not in CLOSED:
            warnings = True
    if not saw_p0:
        raise ValueError("at least one P0 check is required")
    if blocked:
        return "BLOCKED"
    if warnings:
        return "READY_WITH_WARNINGS"
    return "READY"


def main(argv):
    if len(argv) != 2:
        print("usage: python scripts/gate_verdict.py report.json", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        payload = json.load(handle)
    print(evaluate(payload["checks"], payload["production_go_live"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
