"""契约测试：校验技能文档与结论脚本，不访问外部站点。"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gate_verdict import evaluate  # noqa: E402

REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "references/tiers.md",
    "references/droidhz-mapping.md",
    "references/report-template.md",
    "scripts/gate_verdict.py",
    ".github/workflows/ci.yml",
)
FIELDS = (
    "id",
    "category",
    "tier",
    "critical",
    "verify",
    "evidence",
    "pass",
    "fail",
    "not-verified",
    "not-applicable",
)
AUDIT_IDS = {
    "PAY-01",
    "AUTH-01",
    "CREDIT-01",
    "JOB-01",
    "JOB-02",
    "INPUT-01",
    "MOD-01",
    "OUTPUT-01",
    "STORE-01",
    "MOBILE-01",
    "DEPLOY-01",
    "DB-01",
    "DELIVERY-01",
    "LIMIT-01",
    "PRIVACY-01",
    "OBS-01",
}
SECRET_RE = re.compile(
    r"(api[_-]?key\s*[:=]|secret\s*[:=]|token\s*[:=]|password\s*[:=]|"
    r"authorization\s*:?\s*bearer|sk-[a-zA-Z0-9_-]{10,})",
    re.I,
)
LOCAL_PATH_RE = re.compile(
    r"(^|[^A-Za-z0-9_])(%s[^/]+(/|$)|%s[^/]+(/|$)|[A-Za-z]:[\\/][Uu]sers[\\/][^\\/]+([\\/]|$)|%s(var|tmp|etc)(/|$))"
    % (re.escape("/" + "Users/"), re.escape("/" + "home/"), re.escape("/" + "private/"))
)


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]
    data = {}
    match = re.search(r"(?m)^name:\s*(\S+)\s*$", block)
    if match:
        data["name"] = match.group(1)
    desc = re.search(r'(?m)^description:\s*"(.*)"\s*$', block)
    if desc:
        data["description"] = desc.group(1)
    return data


def checks(text):
    parts = re.split(r"(?m)^## (LG-[A-Z0-9-]+)\s*$", text)
    found = []
    # parts[0] is preamble, then id, body, id, body...
    for index in range(1, len(parts), 2):
        check_id = parts[index]
        body = parts[index + 1]
        item = {"heading": check_id}
        for field in FIELDS:
            match = re.search(r"(?m)^- %s: (.*)$" % re.escape(field), body)
            item[field] = match.group(1).strip() if match else None
        found.append(item)
    return found


class ContractTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative in REQUIRED_FILES:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_frontmatter(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        meta = frontmatter(skill)
        self.assertEqual(meta.get("name"), "launch-gate-skill")
        description = meta.get("description", "")
        self.assertGreater(len(description), 40)
        self.assertLessEqual(len(description), 1024)
        self.assertNotIn("<", description)
        self.assertNotIn(">", description)
        for phrase in ("P0", "P1", "N/A", "上线门禁", "上线前全部检查"):
            self.assertIn(phrase, description)

    def test_behavior_rules_are_in_skill(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "上线前检测",
            "launch gate",
            "go-live check",
            "能不能上线",
            "inspect-only",
            "BLOCKED",
            "READY_WITH_WARNINGS",
            "READY",
            "pass",
            "fail",
            "not-verified",
            "not-applicable",
            "audit-ai-generation-site",
            "npm run doctor",
            "seo:check",
            "production_go_live",
            "critical",
        ):
            self.assertIn(phrase, skill)
        self.assertIn("全部", skill)
        self.assertIn("P0", skill)
        self.assertNotIn("index-skill", skill)

    def test_growth_items_are_not_blockers(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        mapping = (ROOT / "references/droidhz-mapping.md").read_text(encoding="utf-8")
        for phrase in ("Reddit", "AppSumo", "Creem", "Neon", "Vercel"):
            self.assertIn(phrase, skill + "\n" + mapping)
        self.assertIn("不得当成部署阻断", skill)
        self.assertIn("禁止把它们升为 P0", skill)

    def test_reference_links_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for link in re.findall(r"\]\((references/[^)]+)\)", skill):
            self.assertTrue((ROOT / link).is_file(), link)

    def test_check_table(self):
        table = checks((ROOT / "references/tiers.md").read_text(encoding="utf-8"))
        ids = [item["heading"] for item in table]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(AUDIT_IDS).isdisjoint(ids))
        self.assertGreaterEqual(len(ids), 20)
        expected = {
            "LG-SITE-01",
            "LG-PROV-01",
            "LG-BILL-01",
            "LG-AUTH-01",
            "LG-SEO-01",
            "LG-SEC-01",
            "LG-AUTO-01",
            "LG-LEGAL-01",
            "LG-GSC-01",
            "LG-IDX-01",
            "LG-ANA-01",
            "LG-CHAT-01",
            "LG-COPY-01",
            "LG-LINK-01",
            "LG-ERR-01",
            "LG-ICON-01",
            "LG-CAC-01",
            "LG-NA-DB-01",
            "LG-NA-PAY-01",
            "LG-NA-HOST-01",
            "LG-NA-GROWTH-01",
        }
        self.assertTrue(expected <= set(ids))
        for item in table:
            for field in FIELDS:
                self.assertTrue(item[field], "%s missing %s" % (item["heading"], field))
            self.assertEqual(item["id"], item["heading"])
            self.assertIn(item["tier"], ("P0", "P1", "N/A"))
            self.assertIn(item["critical"], ("yes", "no"))
            if item["tier"] != "P0":
                self.assertEqual(item["critical"], "no")
            if item["tier"] == "N/A":
                self.assertIn("始终使用", item["not-applicable"])
        legal = next(item for item in table if item["id"] == "LG-LEGAL-01")
        self.assertEqual(legal["tier"], "P0")
        self.assertEqual(legal["critical"], "no")
        growth = next(item for item in table if item["id"] == "LG-NA-GROWTH-01")
        self.assertEqual(growth["tier"], "N/A")

    def test_mapping_covers_source_categories(self):
        mapping = (ROOT / "references/droidhz-mapping.md").read_text(encoding="utf-8")
        for category in ("需求挖掘", "SEO", "开发", "数据分析", "支付", "流量", "外链", "产品", "部署", "复盘"):
            self.assertIn(category, mapping)
        self.assertIn("audit-ai-generation-site", mapping)
        self.assertLess(len(mapping), 4000)

    def test_report_template_lists_statuses_and_ids(self):
        report = (ROOT / "references/report-template.md").read_text(encoding="utf-8")
        for status in ("pass", "fail", "not-verified", "not-applicable"):
            self.assertIn(status, report)
        for verdict in ("BLOCKED", "READY_WITH_WARNINGS", "READY"):
            self.assertIn(verdict, report)
        for check_id in ("LG-SITE-01", "LG-LEGAL-01", "LG-ANA-01", "LG-NA-GROWTH-01"):
            self.assertIn(check_id, report)

    def test_readme_install_line(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "请帮我把这个 Skill（技能）安装到当前项目：https://github.com/oceans777/launch-gate-skill",
            readme,
        )

    def test_no_local_paths_or_secret_assignments(self):
        skipped = {".git", "__pycache__", ".pytest_cache"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or skipped.intersection(path.parts):
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(SECRET_RE.search(text), str(path))
            self.assertIsNone(LOCAL_PATH_RE.search(text), str(path))

    def test_verdict_matrix(self):
        def row(check_id, tier, critical, status):
            return {"id": check_id, "tier": tier, "critical": critical, "status": status}

        base = [
            row("LG-SITE-01", "P0", True, "pass"),
            row("LG-LEGAL-01", "P0", False, "pass"),
            row("LG-GSC-01", "P1", False, "pass"),
            row("LG-NA-GROWTH-01", "N/A", False, "not-applicable"),
        ]
        self.assertEqual(evaluate(base, True), "READY")
        warned = [row("LG-SITE-01", "P0", True, "pass"), row("LG-GSC-01", "P1", False, "not-verified")]
        self.assertEqual(evaluate(warned, True), "READY_WITH_WARNINGS")
        failed = [row("LG-SITE-01", "P0", True, "fail"), row("LG-GSC-01", "P1", False, "pass")]
        self.assertEqual(evaluate(failed, False), "BLOCKED")
        unseen = [row("LG-SITE-01", "P0", True, "not-verified")]
        self.assertEqual(evaluate(unseen, True), "BLOCKED")
        self.assertEqual(evaluate(unseen, False), "READY_WITH_WARNINGS")
        legal_gap = [row("LG-SITE-01", "P0", True, "pass"), row("LG-LEGAL-01", "P0", False, "not-verified")]
        self.assertEqual(evaluate(legal_gap, True), "READY_WITH_WARNINGS")
        skipped = [
            row("LG-SITE-01", "P0", True, "not-applicable"),
            row("LG-GSC-01", "P1", False, "not-applicable"),
        ]
        self.assertEqual(evaluate(skipped, True), "READY")
        with self.assertRaises(ValueError):
            evaluate([row("LG-NA-GROWTH-01", "N/A", False, "fail")], True)
        with self.assertRaises(ValueError):
            evaluate([row("LG-GSC-01", "P1", False, "pass")], True)

    def test_cli_prints_verdict(self):
        payload = {
            "production_go_live": True,
            "checks": [
                {"id": "LG-SITE-01", "tier": "P0", "critical": True, "status": "pass"},
                {"id": "LG-ANA-01", "tier": "P1", "critical": False, "status": "fail"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "gate_verdict.py"), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "READY_WITH_WARNINGS")


if __name__ == "__main__":
    unittest.main()
