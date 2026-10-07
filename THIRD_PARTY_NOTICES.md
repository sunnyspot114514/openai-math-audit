# Attribution and licensing / 署名与许可

New editorial text, translations and bundle-inspection code are provided under [Apache-2.0](LICENSE), following the license convention of the reference project. The underlying mathematical discoveries and formal proofs are not claimed as the maintainer's work.

新增说明、译文和材料检查脚本采用 [Apache-2.0](LICENSE)。本仓库不主张对被核验定理或其原始形式化证明的作者权。

| Material | Origin | Treatment |
|---|---|---|
| Challenge `.lean` files, Comparator JSON configurations and archived build metadata | [openai/math, pinned commit](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a) | Apache-2.0; upstream bytes preserved |
| Comparator README snapshots | [leanprover/comparator](https://github.com/leanprover/comparator/tree/d03acab154d269c06e60e4de7e4cc85deebff94b) | Apache-2.0; Lean FRO / upstream contributors retain attribution |
| Machine-run reports, command records and logs | User-organized Grok bot audit, 2026-10-07 | Historical evidence, not a new publication-time execution |
| Earlier proof-reading notes and numerical diagnostics | User-organized GPT-assisted audit, 2026-10-07 | Supplementary records; numerical checks are not proofs |
| Original second review | GPT-assisted cross-check of the delivered audit package | Not a second Lean execution |
| systemd documentation | Primary documentation linked in `docs/SOURCES.md` | The excerpt from the private source archive is not redistributed here |

Private host identifiers and unrelated host paths are pseudonymized only in files marked as publication copies. The per-file source and publication hashes are recorded in [publication_map.json](evidence/provenance/publication_map.json). All target statements, target JSON files, stdout success records and axiom outputs remain byte-identical to the supplied source archive.

No upstream proof library, compiled Lean objects, credentials, font files or private-machine screenshots are bundled. This project is not endorsed by OpenAI, Lean FRO, xAI or AGMAI.
