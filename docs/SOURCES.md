# Sources / 来源

Read relative evidence links first for this audit. Public sources below identify the upstream objects; they do not make this repository an official endorsement. URLs for mathematical objects are pinned to the audited commit wherever possible. Accessed for publication: 2026-10-07.

本审计优先引用仓库内证据。下列链接用于识别上游材料，不构成官方背书。数学材料尽量固定到被审计版本；公开整理访问日期为 2026-10-07。

| ID | Source / 来源 | Purpose / 用途 |
|---|---|---|
| S1 | [OpenAI announcement, 2026-10-06](https://openai.com/index/sharing-ai-progress-in-mathematics/) | Release context; internal model and compute-equivalence disclosure |
| S2 | [Pinned openai/math README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) | 722 manuscripts / 372 families and verification-status boundaries |
| S3 | [Symmetric Mahler Challenge](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/MahlerConjecture.lean) | Exact first target |
| S4 | [Symmetric polar-product Challenge](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/SymmetricPolar.lean) | Exact second target |
| S5 | [Symmetric Mahler paper source](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-symmetric-Mahler-conjecture-and-its-equality-cases-September-22-2026/build) | Upstream argument and attribution |
| S6 | [Symplectic polar-product paper source](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build) | Ball construction, uniform slices, realization and approximation |
| S7 | [Comparator README, pinned version](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md) | Checker contract and trusted-environment assumptions |
| S8 | [Comparator Main.lean, pinned version](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/Main.lean) | Ordering of comparison, axiom checking and kernel replay |
| S9 | [AGMAI recommendations, 2026-09-29](https://agmai.org/general-sep29/) | Responsible release, explanation, attribution and community support |
| S10 | [systemd execution documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) | `RestrictAddressFamilies` reference; historical execution is described in the run report |
| S11 | [JevNet Runtime](https://github.com/sunnyspot114514/jevnet-runtime) | README organization reference only; not a mathematical dependency |

## Local primary records / 本地一手记录

[Machine report](../evidence/machine/REPORT.md) · [Mahler stdout](../evidence/machine/mahler.stdout.log) · [Polar stdout](../evidence/machine/polar.stdout.log) · [Semantic review](../evidence/machine/SEMANTICS.md) · [Secondary review](../evidence/secondary/second_review_zh.md) · [Earlier proof reading](../evidence/manual/audit_zh.md).

The personal chronology and reaction in the essay are the author's account from the drafting conversation. Exact claim-generation transcripts and the private earlier research history are not bundled and are not used as proof-validity evidence.

文章中的个人时间线与感受来自作者自述。原始探索的完整对话与私人研究历史不在本包中，也不作为证明正确性的依据。
