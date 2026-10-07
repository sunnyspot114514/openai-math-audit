"""Tests of the archive checker only. These tests never invoke Lean."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_bundle as audit


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "bundle"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", ".git"))

    def tearDown(self):
        self.temp.cleanup()

    def test_public_bundle(self):
        result = audit.inspect(self.root)
        self.assertEqual(result["bundle_status"], "BUNDLE_OK")
        self.assertFalse(result["fresh_lean_run"])
        self.assertEqual(len(result["targets"]), 2)

    def test_changed_bytes_rejected(self):
        p = self.root / "README.md"
        p.write_bytes(p.read_bytes() + b"\nChanged.\n")
        with self.assertRaises(audit.BundleError):
            audit.check_manifest(self.root)

    def test_nonzero_process_exit_rejected(self):
        (self.root / "evidence/machine/mahler.exitcode").write_text("1\n")
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "mahler")

    def test_missing_final_marker_rejected(self):
        p = self.root / "evidence/machine/polar.stdout.log"
        p.write_text(p.read_text().replace("Your solution is okay!", ""))
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "polar")

    def test_disallowed_axiom_rejected(self):
        p = self.root / "evidence/machine/axcheck-AxMahler.out"
        p.write_text(p.read_text().replace("Quot.sound]", "Quot.sound, sorryAx]"))
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "mahler")

    def test_definition_hole_rejected(self):
        p = self.root / "evidence/machine/preaudit-copies/SymmetricPolar.json"
        cfg = json.loads(p.read_text())
        cfg["definition_names"] = ["FakeDefinition"]
        p.write_text(json.dumps(cfg))
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "polar")

    def test_external_kernel_claim_rejected(self):
        p = self.root / "evidence/machine/preaudit-copies/SymmetricPolar.json"
        cfg = json.loads(p.read_text())
        cfg["enable_nanoda"] = True
        p.write_text(json.dumps(cfg))
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "polar")

    def test_missing_exit_file_rejected(self):
        (self.root / "evidence/machine/polar.exitcode").unlink()
        with self.assertRaises(audit.BundleError):
            audit.check_target(self.root, "polar")

    def test_manifest_path_traversal_rejected(self):
        (self.root / "SHA256SUMS").write_text("0" * 64 + "  ../outside\n")
        with self.assertRaises(audit.BundleError):
            audit.check_manifest(self.root)

    def test_source_identity_claim_rejected(self):
        p = self.root / "evidence/provenance/publication_map.json"
        data = json.loads(p.read_text())
        item = next(x for x in data["files"] if x["status"] == "unchanged")
        item["source_sha256"] = "0" * 64
        p.write_text(json.dumps(data))
        with self.assertRaises(audit.BundleError):
            audit.check_provenance(self.root)

    def test_checker_does_not_claim_new_proof_run(self):
        result = audit.check_target(self.root, "mahler")
        self.assertTrue(result["recorded_evidence_consistent"])
        self.assertFalse(result["fresh_lean_run"])


if __name__ == "__main__":
    unittest.main()
