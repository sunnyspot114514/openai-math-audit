# Evidence provenance and public-edition handling

[English](PROVENANCE.en.md) | [中文](PROVENANCE.zh-CN.md) · [Home](../README.md)

## Three evidence layers

**Machine replay:** the user supplied `openai-math-audit-adc7f12.tar.gz`. Its SHA-256 is `4f792ce069732d04029f6da79bb425662ebd113600dca1f367e62ad9f593d582`. The private transport archive is not nested inside this public package. Its files are exposed individually under `evidence/machine/`, subject to the transformations below.

**Earlier reading:** `evidence/manual/` preserves the earlier GPT-assisted proof-reading report and finite numerical/symbolic diagnostics. Its report predates the machine replay and therefore correctly says no Lean replay had been completed at that stage. The numerical diagnostics do not prove a universal theorem and were not rerun during publication.

**Secondary review:** `evidence/secondary/` preserves the original review and its upstream blob comparison. That review inspected the delivery; it did not execute Lean again. The English audit overview is an editorial counterpart, not an additional reviewer or validation event.

## Byte preservation and redaction

During packaging, all **58/58** entries in the original outer checksum list and **12/12** in the pre-audit list matched the provided source files. The package transformation is recorded per file in [publication_map.json](../evidence/provenance/publication_map.json).

Only three machine-source files require pseudonymization: `REPORT.md`, `VERSIONS.txt`, and `credential-readability-scan.txt`. A publication notice is added to each. This removes a host identifier, a host-user path and an unrelated project/temp path. It does not erase the shared-host limitation or change the sandbox claims, tool versions, results, exit codes or theorem scope.

Core stdout/stderr, exit-code files, axiom outputs, target `.lean` files and JSON configurations are preserved byte for byte. Historical `/home/mathaudit/...` paths are retained: they refer to the dedicated audit account and help interpret the recorded commands. They are not portable installation instructions.

The standalone systemd manual excerpt is omitted; the primary source is linked in [SOURCES.md](SOURCES.md). The original reports still mention its historical filename. It is an omitted supporting document, not a missing proof log.

The raw original checksum lists are kept under `evidence/provenance/`. They describe the source edition and will not all match the sanitized publication files. Use the repository-root [SHA256SUMS](../SHA256SUMS) for **this** public edition. The transformation map retains the old and new hashes, making modifications explicit.

## What was checked at publication time?

The package builder checked original hashes, copied or explicitly transformed evidence, checked links in the new documents, ran the archive-inspection tests and checked for common token/private-key patterns. No matching credential values were found in that pattern check. It is not a complete secret-discovery or host-security audit.

No original archived shell script was executed. No proof library, prebuilt `.olean`, binary verifier, screenshot of another user, or font is included. The bundled mathematical diagnostics remain supplementary archival material.

## What hashes cannot show

A matching hash establishes agreement with a given byte string or manifest. It cannot show that an original process really ran, that its host was uncompromised, or that the program used the recorded binary. The logs, scripts, versions and consistent results supply the audit record; the new package checker only checks that those records have remained internally consistent.

No claim of a fresh Lean run is made during this publication step.
