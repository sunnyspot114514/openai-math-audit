#!/usr/bin/env python3
"""Check a published audit archive, not a mathematical proof.

No subprocess, network request, Lean compiler or archived script is executed.
A matching archive is not an authenticated execution history. It is only
consistent with the records and checksum manifest distributed alongside it.

Copyright 2026 SUNNY99. Licensed under the Apache License, Version 2.0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

PIN = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
TARGETS = {
    "mahler": ("MahlerConjecture", "OAI.Analysis.Mahler.MainTheorem",
               "OAI.SymmetricMahler.symmetric_mahler", "AxMahler"),
    "polar": ("SymmetricPolar", "OAI.Geometry.PolarProducts.Main",
              "OAI.SymmetricPolar.symmetric_polar_main", "AxPolar"),
}


class BundleError(Exception):
    """A required record is missing or inconsistent."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_file(root: Path, relative: str) -> Path:
    """Reject absolute paths, traversal and symlinks before reading a file."""
    rel = PurePosixPath(relative)
    if (not relative or rel.is_absolute() or ".." in rel.parts
            or "\\" in relative or re.match(r"^[A-Za-z]:", relative)):
        raise BundleError(f"Unsafe relative path: {relative!r}")
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            raise BundleError(f"Symlink not allowed in published evidence: {relative}")
    if not path.is_file():
        raise BundleError(f"Missing file: {relative}")
    return path


def read_text(root: Path, relative: str) -> str:
    return safe_file(root, relative).read_text(encoding="utf-8")


def read_json(root: Path, relative: str) -> Any:
    return json.loads(read_text(root, relative))


def check_manifest(root: Path) -> int:
    seen: set[str] = set()
    for line_no, line in enumerate(read_text(root, "SHA256SUMS").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
        if not match:
            raise BundleError(f"Malformed SHA256SUMS line {line_no}")
        expected, relative = match.groups()
        if relative in seen:
            raise BundleError(f"Duplicate checksum entry: {relative}")
        seen.add(relative)
        if sha256(safe_file(root, relative)) != expected:
            raise BundleError(f"Checksum mismatch: {relative}")
    if not seen:
        raise BundleError("Empty checksum manifest")
    required = {"README.md", "README.zh-CN.md", "audit-summary.json",
                "evidence/provenance/publication_map.json"}
    for name, (config, _, _, axiom_file) in TARGETS.items():
        required.update({
            f"evidence/machine/{name}.stdout.log",
            f"evidence/machine/{name}.stderr.log",
            f"evidence/machine/{name}.exitcode",
            f"evidence/machine/{name}.time.txt",
            f"evidence/machine/axcheck-{axiom_file}.out",
            f"evidence/machine/preaudit-copies/{config}.json",
            f"evidence/machine/preaudit-copies/{config}.lean",
        })
    if missing := required - seen:
        raise BundleError("Required evidence absent from manifest: " + ", ".join(sorted(missing)))
    return len(seen)


def check_provenance(root: Path) -> int:
    mapping = read_json(root, "evidence/provenance/publication_map.json")
    if mapping.get("fresh_lean_run_during_packaging") is not False:
        raise BundleError("Publication metadata incorrectly implies a fresh Lean run")
    records = mapping.get("files")
    if not isinstance(records, list) or not records:
        raise BundleError("Missing provenance records")
    destinations: set[str] = set()
    for item in records:
        if item.get("status") == "omitted":
            if not item.get("reason"):
                raise BundleError("Omitted source lacks a reason")
            continue
        relative = item.get("destination", "")
        if relative in destinations:
            raise BundleError(f"Duplicate provenance destination: {relative}")
        destinations.add(relative)
        actual = sha256(safe_file(root, relative))
        if actual != item.get("published_sha256"):
            raise BundleError(f"Publication map mismatch: {relative}")
        if item.get("status") in {"unchanged", "relocated"}:
            if actual != item.get("source_sha256"):
                raise BundleError(f"An unchanged file differs from its source: {relative}")
        elif item.get("status") == "sanitized":
            if not item.get("changes"):
                raise BundleError(f"Sanitized file has no change disclosure: {relative}")
        else:
            raise BundleError(f"Unknown publication status: {relative}")
    return len(destinations)


def check_target(root: Path, name: str) -> dict[str, Any]:
    if name not in TARGETS:
        raise BundleError(f"Unknown target: {name}")
    config, module, theorem, axiom_file = TARGETS[name]
    base = "evidence/machine/"
    cfg = read_json(root, base + f"preaudit-copies/{config}.json")
    if cfg.get("challenge_module") != f"ComparatorChallenges.{config}":
        raise BundleError(f"{name}: wrong challenge module")
    if cfg.get("solution_module") != module or cfg.get("theorem_names") != [theorem]:
        raise BundleError(f"{name}: wrong formal target")
    if set(cfg.get("permitted_axioms", [])) != AXIOMS:
        raise BundleError(f"{name}: permitted axiom list differs")
    if cfg.get("definition_names", []) != []:
        raise BundleError(f"{name}: unexpected definition holes")
    if cfg.get("enable_nanoda") is not False or cfg.get("external_kernels"):
        raise BundleError(f"{name}: kernel configuration differs from the recorded single-kernel run")
    if read_text(root, base + f"{name}.exitcode").strip() != "0":
        raise BundleError(f"{name}: recorded exit code is not zero")
    timing = read_text(root, base + f"{name}.time.txt")
    if re.findall(r"Exit status:\s*(\d+)", timing) != ["0"]:
        raise BundleError(f"{name}: time record does not show one successful exit")
    stdout = read_text(root, base + f"{name}.stdout.log")
    markers = ["Running Lean default kernel on solution.",
               "Lean default kernel accepts the solution", "Your solution is okay!"]
    pos = -1
    for marker in markers:
        next_pos = stdout.find(marker, pos + 1)
        if next_pos < 0:
            raise BundleError(f"{name}: missing or out-of-order success marker: {marker}")
        pos = next_pos
    if theorem not in stdout or module not in stdout:
        raise BundleError(f"{name}: stdout does not identify the expected export")
    if "Lean default kernel rejects the solution" in stdout:
        raise BundleError(f"{name}: contradictory kernel rejection in stdout")
    axiom_output = read_text(root, base + f"axcheck-{axiom_file}.out")
    pattern = re.escape("'" + theorem + "' depends on axioms:") + r"\s*\[([^\]]*)\]"
    matches = re.findall(pattern, axiom_output)
    if len(matches) != 1:
        raise BundleError(f"{name}: missing or ambiguous axiom record")
    actual_axioms = {value.strip() for value in matches[0].split(",") if value.strip()}
    if actual_axioms != AXIOMS:
        raise BundleError(f"{name}: recorded axioms differ: {sorted(actual_axioms)}")
    return {"target": name, "recorded_evidence_consistent": True,
            "fresh_lean_run": False, "axioms": sorted(actual_axioms)}


def inspect(root: Path) -> dict[str, Any]:
    files = check_manifest(root)
    provenance = check_provenance(root)
    summary = read_json(root, "audit-summary.json")
    if summary.get("upstream_commit") != PIN:
        raise BundleError("Unexpected upstream commit")
    if summary.get("fresh_lean_run_during_packaging") is not False:
        raise BundleError("Summary incorrectly claims a fresh Lean run during packaging")
    target_records = summary.get("targets", [])
    if {t.get("id") for t in target_records} != set(TARGETS) or len(target_records) != 2:
        raise BundleError("Summary must identify exactly the two audited targets")
    for record in target_records:
        if record.get("recorded_verdict") != "VERIFIED" or record.get("recorded_exit_code") != 0:
            raise BundleError("Summary disagrees with the recorded target outcome")
        if record.get("theorem") != TARGETS[record["id"]][2]:
            raise BundleError("Summary names the wrong theorem")
    results = [check_target(root, name) for name in TARGETS]
    return {"bundle_status": "BUNDLE_OK", "checksummed_files": files,
            "mapped_publication_files": provenance, "targets": results,
            "fresh_lean_run": False,
            "meaning": "Evidence-file integrity and recorded-result consistency only; not a proof verification or execution-history authentication."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Repository root (defaults to this script's parent repository)")
    parser.add_argument("--json", action="store_true", help="Write structured results to stdout")
    args = parser.parse_args()
    try:
        result = inspect(args.root.resolve())
    except (BundleError, OSError, ValueError, TypeError, KeyError) as exc:
        if args.json:
            print(json.dumps({"bundle_status": "FAILED", "error": str(exc), "fresh_lean_run": False}))
        else:
            print(f"FAIL  {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS  public file checksums")
        print("PASS  publication provenance")
        for name in TARGETS:
            print(f"PASS  {name}: recorded exit 0, kernel acceptance, permitted axioms")
        print("BUNDLE_OK — evidence consistency only; no Lean verification was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
