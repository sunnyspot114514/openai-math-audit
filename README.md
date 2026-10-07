# OpenAI Math Audit

[![Recorded audit: 2 targets](https://img.shields.io/badge/recorded_audit-2_targets-2c7a7b)](docs/AUDIT.en.md)
[![Lean 4.34.1](https://img.shields.io/badge/Lean-4.34.1-blue)](evidence/machine/VERSIONS.txt)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[🇺🇸 English](README.md) | [🇨🇳 中文](README.zh-CN.md)

**An independent, evidence-backed audit of two mathematical statements in OpenAI's October 2026 release.**

This repository preserves a Comparator replay of the **symmetric Mahler inequality** and **Gromov width of symmetric polar products**. It includes execution records, axiom outputs, statement checks, review notes and a bilingual essay.

> **As generation becomes cheaper, verification and explanation deserve more attention.**

## 60-second evidence check

After downloading or cloning this repository, run from its root:

```bash
python scripts/check_bundle.py
```

Python 3.10+ and the standard library are sufficient.

Expected output shape:

```text
PASS  public file checksums
PASS  publication provenance
PASS  mahler: recorded exit 0, kernel acceptance, permitted axioms
PASS  polar: recorded exit 0, kernel acceptance, permitted axioms
BUNDLE_OK — evidence consistency only; no Lean verification was run.
```

This checks the published archive. For a new formal replay, read [Reproduce the audit](docs/REPRODUCE.en.md).

## What was checked?

The audited upstream commit is:

```text
openai/math
adc7f1241b42e322a6451854ab7e4b4c146bf78a
```

| Target | Recorded result | Wall time | Direct evidence |
|---|---|---|---|
| Symmetric Mahler inequality, every dimension n ≥ 1 | Comparator exit **0**; Lean default kernel accepted | **11:21.19** | [stdout](evidence/machine/mahler.stdout.log), [time](evidence/machine/mahler.time.txt), [axioms](evidence/machine/axcheck-AxMahler.out) |
| Symmetric polar-product width, every dimension n ≥ 2 | Comparator exit **0**; Lean default kernel accepted | **47:52.38** | [stdout](evidence/machine/polar.stdout.log), [time](evidence/machine/polar.time.txt), [axioms](evidence/machine/axcheck-AxPolar.out) |

These are recorded verification times after dependency preparation, with an official Mathlib cache. See the [machine-run report](evidence/machine/REPORT.md).

For every origin-symmetric convex body $K\subset\mathbb R^n$, the first target states

$$
|K|\,|K^\circ|\geq\frac{4^n}{n!},\qquad n\geq1.
$$

The second states

$$
c_G\!\left(\operatorname{int}K\times\operatorname{int}K^\circ\right)=4,\qquad n\geq2,
$$

and includes a smooth symplectic embedding of every ball of capacity $0<c<4$.

Both recorded axiom outputs contain only:

```text
propext, Classical.choice, Quot.sound
```

The precise hypotheses, normalizations and scope checks are in [SEMANTICS.md](evidence/machine/SEMANTICS.md) and the [bilingual audit overview](docs/AUDIT.en.md).

## What problem does this project address?

A generated manuscript, an LLM's favorable review, a compiling Lean file and a successful theorem check are different kinds of evidence.

| Question | Evidence supplied here |
|---|---|
| Which exact statement was checked? | Pinned Challenge files and original JSON configurations |
| Did the checker actually complete? | stdout, stderr, process exit codes and timing records |
| Was an assumption added to make it pass? | Comparator axiom check and separate `#print axioms` outputs |
| Was the mathematical meaning weakened? | Definition, hypothesis and normalization review |
| What must be trusted? | Tool versions, cache use, patches and isolation limitations |
| What can another reader learn or reuse? | Proof-reading notes, explanation and reproducibility guide |

## The mental model

```text
Candidate mathematical result
             |
             v
Precise, versioned theorem statement
             |
             v
Formal replay and preserved execution evidence
             |
             v
Semantic and scope review
             |
             v
Understandable, reusable mathematical knowledge
```

AI can assist throughout this process.

## Start reading

| Purpose | English | 中文 |
|---|---|---|
| Audit findings | [Audit overview](docs/AUDIT.en.md) | [核验说明](docs/AUDIT.zh-CN.md) |
| Run a new formal audit | [Reproduction guide](docs/REPRODUCE.en.md) | [复跑说明](docs/REPRODUCE.zh-CN.md) |
| Understand the mathematical route | [Proof map](docs/EXPLANATION.en.md) | [证明路线解读](docs/EXPLANATION.zh-CN.md) |
| Read the author's perspective | [Essay](articles/essay.en.md) | [知乎回答稿](articles/zhihu.zh-CN.md) |
| Public evidence edition | [Provenance](docs/PROVENANCE.en.md) | [来源与公开处理](docs/PROVENANCE.zh-CN.md) |

## Who did what?

**SUNNY99** organized the inquiry and audit. GPT-assisted work covered proof reading, local diagnostics, secondary review and editorial preparation. A **Grok bot** performed the recorded machine replay. **Comparator and the Lean default kernel** performed the recorded formal checks.

## Research context

In July, the author discussed AI tackling open mathematical problems. An August reply proposed Viterbo/Mahler as a challenge, which led to about two months of AI-assisted attempts and partial candidate results. The new general results overtook that narrow target.

The author's reaction is **mostly positive, with some mild disappointment**. Verification and explanation were already recurring priorities before this release. The [essay](articles/essay.en.md) gives the full account.

## Repository layout

```text
README.md / README.zh-CN.md  bilingual entry points
articles/                   English essay and Chinese publication draft
docs/                       audit, reproduction, explanation and provenance
evidence/machine/           recorded run evidence and pinned source snapshots
evidence/manual/            earlier proof-reading notes and finite diagnostics
evidence/secondary/         review of the delivered audit package
evidence/provenance/        source hashes and public-edition transformation map
scripts/check_bundle.py     offline archive-consistency checker
tests/                     tests of the archive checker
SHA256SUMS                  checksums of this published edition
CITATION.cff                citation metadata for this audit record
```

## Contributing and citation

Report a concrete issue with the commit, target, command, log and smallest relevant discrepancy. Separate mathematical objections, formalization mismatches and environment failures. See [CONTRIBUTING.md](CONTRIBUTING.md).

Cite this audit separately from the upstream papers using [CITATION.cff](CITATION.cff). Upstream sources are listed in [SOURCES.md](docs/SOURCES.md).

## License

New editorial material and bundle-inspection code: **Apache-2.0**. Upstream snapshots retain their original attribution and licenses. See [LICENSE](LICENSE), [NOTICE](NOTICE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
