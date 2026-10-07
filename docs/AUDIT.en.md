# Audit findings and limits

[English](AUDIT.en.md) | [中文](AUDIT.zh-CN.md) · [Home](../README.md)

**Snapshot date: 2026-10-07.** This document distinguishes the machine run, secondary review and publication step. It does not add another proof-verification event.

## Result

At `openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, the delivered records show Comparator success for two unchanged target configurations. Both exit codes are zero. Both stdout logs reach the default Lean kernel's acceptance and Comparator's final success message.

| Target | Configuration | Exact formal theorem | Recorded time |
|---|---|---|---|
| Symmetric Mahler | `MahlerConjecture.json` | `OAI.SymmetricMahler.symmetric_mahler` | 11:21.19 |
| Symmetric polar products | `SymmetricPolar.json` | `OAI.SymmetricPolar.symmetric_polar_main` | 47:52.38 |

Direct evidence: [Mahler stdout](../evidence/machine/mahler.stdout.log), [Polar stdout](../evidence/machine/polar.stdout.log), [machine report](../evidence/machine/REPORT.md), [machine-readable summary](../audit-summary.json).

## Mathematical scope

The first statement covers every positive dimension and every compact, convex, origin-symmetric set with nonempty interior. The polar uses the standard coordinate pairing, and `volume` is ordinary finite-dimensional Lebesgue volume. The `toReal` conversion is not an extra hypothesis or an alternative notion of volume. Equality classification is not part of this target.

The second statement covers the open product `int K × int K°` in conjugate position/momentum coordinates. The ball uses the explicit Euclidean expression `π(‖q‖² + ‖p‖²) < c`, not the product space's maximum-norm ball. Smoothness, topological embedding, range containment and derivative preservation of the standard symplectic form are all required. The domain is open, so the derivative is the genuine local derivative. The conclusion includes every capacity strictly below 4, not necessarily an embedding at the supremum.

The complete recorded semantic review is [SEMANTICS.md](../evidence/machine/SEMANTICS.md). The frozen target sources are [MahlerConjecture.lean](../evidence/machine/preaudit-copies/MahlerConjecture.lean) and [SymmetricPolar.lean](../evidence/machine/preaudit-copies/SymmetricPolar.lean).

## Why the successful checks matter

The success is stronger than ordinary Lean compilation. At the recorded Comparator version, the verification process compares the statement environment, checks transitive axiom use and replays the exported solution into the default Lean kernel. This depends on the trusted inputs and environment described by [Comparator upstream](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md).

Both additional axiom outputs contain exactly the permitted set: `propext`, `Classical.choice`, `Quot.sound`. The `sorry` warning in each Challenge file is an intentional placeholder for the task to be proved. It is not a hole in the accepted Solution theorem. See [Mahler axioms](../evidence/machine/axcheck-AxMahler.out) and [Polar axioms](../evidence/machine/axcheck-AxPolar.out).

## Who performed each layer?

The recorded machine work was executed by a Grok bot under a separate non-privileged audit account. GPT-assisted reading examined the mathematical route and later cross-checked the delivery. The [original Chinese secondary review](../evidence/secondary/second_review_zh.md) is preserved separately from this English editorial summary.

The publication step rechecked source checksums, retained the core execution records, pseudonymized a few unrelated host identifiers and tested the archive-consistency script. It did **not** reinstall Lean, rebuild the proof libraries or perform a second kernel run.

## Environment and disclosed deviations

The run report describes Debian 13, an x86-64 Linux 6.12.94+ kernel, 8 vCPUs and 16 GB RAM with no swap. These are one recorded environment, not minimum system requirements. The reported GNU time memory peak is the largest single waited process, not total machine or process-tree memory.

The Lean toolchain is 4.34.1. Comparator source is pinned at `d03acab154d269c06e60e4de7e4cc85deebff94b`; its toolchain pin alone was changed from 4.34.0 to 4.34.1. The supplied diff does not change checker logic. `lean4export` was compiled with the matching toolchain. The two target configurations were not changed.

The report records official Mathlib cache use, with no prebuilt OAI proof objects reused. Repository-owned dependency compatibility patches produced local-change warnings. The reported import closures exclude those patched third-party packages; the trusted Mathlib closure and tracked upstream workspace remained unchanged. This publication did not independently fetch and inspect every dependency again.

Since systemd was unavailable, the run used the archived `restrict_af_unix.c` wrapper together with real landrun/Landlock. The report includes isolation self-tests. Secondary review read the wrapper and tests but did not certify equivalence to a complete systemd environment. The account shared its host with other work; unrelated world-readable directories remained readable. The existence of this limitation must not be erased by describing the run as a clean standalone VM.

Sources: [versions](../evidence/machine/VERSIONS.txt), [patches](../evidence/machine/PATCHES.txt), [workspace diff](../evidence/machine/workspace-diff.txt), [self-test](../evidence/machine/landrun-selftest.log), [machine report](../evidence/machine/REPORT.md).

## What the package does not establish

It does not authenticate an execution history merely by hashing log files. It does not certify the host, compiler, cache provider or proof-checker implementation. It does not provide a second independent kernel check. It does not assert that every prose argument or every upstream theorem has been audited.

General nonsymmetric Mahler, Hanner equality cases, the Quasi-Riemann result, other families, and the model's discovery process remain outside this audit. Source-code patches to a future proof must be reported as a new variant rather than a verification of the unchanged original.

## Appropriate conclusion

> The recorded independent replay of these two fixed formal statements completed successfully, with the default Lean kernel accepting the exports and no axioms outside the permitted set. Semantic review found no mismatch with the stated mathematical targets. Secondary review found no contradiction overturning those records. This conclusion is scoped to the two targets and the documented trust assumptions.

That supports accepting these two results at this evidence level. Further work should answer a specific new question: an external-kernel replay, a source-only build, a concrete defect report, or a better explanation of the argument. It need not be an indefinite series of model opinions.
