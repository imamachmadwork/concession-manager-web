#!/usr/bin/env python3
"""Turn Allure results into per-team markdown bug reports.

Reads *-result.json files from an Allure results directory (produced by
`pytest --alluredir`), groups failing/broken tests by their "feature" label
(Frontend / Backend) and "epic" label (test suite, e.g. "Sign In"), and
writes one markdown document per feature/suite pair under reports/bug-reports/
so each team gets a report scoped to just their side of a broken feature.

Usage:
    uv run python scripts/generate_bug_report.py
    uv run python scripts/generate_bug_report.py --results-dir allure-results --out-dir reports/bug-reports
"""

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FAILING_STATUSES = {"failed", "broken"}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unclassified"


def load_results(results_dir: Path) -> list[dict]:
    results = []
    for path in sorted(results_dir.glob("*-result.json")):
        with path.open() as f:
            results.append(json.load(f))
    return results


def label(result: dict, name: str, default: str) -> str:
    for entry in result.get("labels", []):
        if entry["name"] == name:
            return entry["value"]
    return default


def group_failures(results: list[dict]) -> dict[str, dict[str, list[dict]]]:
    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for result in results:
        if result.get("status") not in FAILING_STATUSES:
            continue
        feature = label(result, "feature", "Unclassified")
        epic = label(result, "epic", "Unclassified")
        grouped[feature][epic].append(result)
    return grouped


def render_report(feature: str, epic: str, failures: list[dict], environment: str) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# {epic} — {feature} bugs",
        "",
        f"- Generated: {generated_at}",
        f"- Environment: {environment}",
        f"- Failing tests: {len(failures)}",
        "",
    ]
    for result in failures:
        details = result.get("statusDetails", {})
        lines += [
            f"## {result.get('name', 'unknown test')}",
            "",
            f"- Status: `{result.get('status')}`",
            f"- Full name: `{result.get('fullName', 'n/a')}`",
            "",
            "**Error**",
            "```",
            details.get("message", "(no error message captured)").strip(),
            "```",
            "",
        ]
        trace = details.get("trace", "").strip()
        if trace:
            lines += ["<details><summary>Trace</summary>", "", "```", trace, "```", "", "</details>", ""]
        lines += [
            "Screenshots/videos/traces for this run are in the `test-results/` "
            "or `playwright-artifacts` CI artifact.",
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", default="allure-results", type=Path)
    parser.add_argument("--out-dir", default="reports/bug-reports", type=Path)
    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"No results directory at {args.results_dir}, nothing to report.")
        return

    environment = os.environ.get("API_BASE_URL") or os.environ.get("PYTEST_BASE_URL", "https://concessions.roamstay.com")
    results = load_results(args.results_dir)
    grouped = group_failures(results)

    if not grouped:
        print("No failing tests found — no bug reports generated.")
        return

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_lines = ["## Failing test suites\n"]
    written = []

    for feature, epics in sorted(grouped.items()):
        feature_dir = args.out_dir / slugify(feature)
        feature_dir.mkdir(parents=True, exist_ok=True)
        for epic, failures in sorted(epics.items()):
            out_path = feature_dir / f"{slugify(epic)}.md"
            out_path.write_text(render_report(feature, epic, failures, environment))
            written.append(out_path)
            summary_lines.append(f"- **{feature} / {epic}**: {len(failures)} failing (`{out_path}`)")
            print(f"Wrote {out_path}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("\n".join(summary_lines) + "\n")


if __name__ == "__main__":
    main()
