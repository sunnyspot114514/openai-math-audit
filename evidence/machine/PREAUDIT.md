# PREAUDIT — openai/math @ adc7f1241b42e322a6451854ab7e4b4c146bf78a

Written after reading the files below and **before** any build of Solution modules or any Comparator run.
Only actions before this note: clean clone/checkout, toolchain install (elan, Lean v4.34.1), building the
checker tools (comparator, lean4export, landrun) from upstream sources, and dependency preparation
(`lake exe cache get`, which elaborates `lakefile.lean` — see §4). Copies of every file read are in
`preaudit-copies/` (SHA256SUMS included).

## 1. Checkout
- `git rev-parse HEAD` = `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; `git status --porcelain` empty (see `git-log-1.txt`).
- Single commit ("Initial commit", author "Anonymous", 2026-10-06 14:58:50 -0700).

## 2. Comparator configs (verbatim content in preaudit-copies/)
| | MahlerConjecture.json | SymmetricPolar.json |
|---|---|---|
| challenge_module | `ComparatorChallenges.MahlerConjecture` | `ComparatorChallenges.SymmetricPolar` |
| solution_module | `OAI.Analysis.Mahler.MainTheorem` | `OAI.Geometry.PolarProducts.Main` |
| theorem_names | `OAI.SymmetricMahler.symmetric_mahler` | `OAI.SymmetricPolar.symmetric_polar_main` |
| definition_names | `[]` (no definition holes) | `[]` (no definition holes) |
| permitted_axioms | `propext`, `Quot.sound`, `Classical.choice` | same |
| enable_nanoda | `false` | `false` |
| external_kernels | absent | absent |

Consequence: Comparator will check (a) statement/declaration match against the Challenge environment,
(b) axioms of the listed theorems within the permitted three, (c) replay of the whole Solution export
into the Lean 4.34.1 kernel (built into comparator). No second kernel (nanoda) is requested by the configs;
this audit runs the configs unmodified.

## 3. Challenge (trusted) files
- `ComparatorChallenges/MahlerConjecture.lean` (sha256 40718172…): `import Mathlib` only. Defines
  `OAI.SymmetricMahler.coordinatePolar` and states `symmetric_mahler` with `sorry` (goal placeholder).
- `ComparatorChallenges/SymmetricPolar.lean` (sha256 3683f15e…): `import Mathlib` only. Defines
  `Position`, `Phase` (abbrevs), `IsSymmetricConvexBody`, `polar`, `polarProduct`, `capacityBall`,
  `omega0`, `HasSymplecticEmbedding`, `gromovWidth`, and states `symmetric_polar_main` with `sorry`.
- Neither file imports anything from `OAI.*` or any non-Mathlib package. Scan for
  `run_cmd|run_tac|elab|macro|syntax|initialize|@[extern]|implemented_by|native_decide|unsafe|axiom|opaque|set_option|attribute|notation`
  found **no matches** in either file (only the `import Mathlib` line matched the `import` pattern).
- Trusted import closure of the Challenges = Mathlib @ `d13f23b723b8a846827a245b89c10fc7d3f11612` and its
  own dependencies (batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient, plausible), as pinned in
  `lake-manifest.json`. Mathlib itself is **not** patched by the repo.

## 4. lakefile.lean (trusted per Comparator assumption 1) — notable content
- `package OAI` with `fixedToolchain := true`, `leanOptions := #[⟨autoImplicit, false⟩]`. No `extern_lib`,
  no `precompileModules`, no `moreLinkArgs`, no custom targets/scripts for the challenges.
- 30 `require … from git … @ <full commit>` lines (all pinned to commits), incl. mathlib `d13f23b7…`.
- **A top-level `run_cmd` block executes at every lakefile elaboration** (i.e. on any `lake` invocation,
  including `lake env comparator`). It: for 11 packages (`iut, tate-curves-theta, genl, heights, pi1,
  orbicurve-cores, oka, tempered-fundamental-groups, elliptic-curves, formal-schemes, belyi`) checks the
  checkout in `.lake/packages/<pkg>` is at the pinned commit with the pinned origin URL, and if absent does
  `git clone --no-checkout <url>` + `git checkout --detach <rev>` + `git apply patches/<pkg>-lean4341.patch`
  (with `git apply --check` forward/reverse verification). It runs only `git` on paths under `.lake/packages`.
- A `post_update` hook (runs only on `lake update`) applies 12 further compatibility patches
  (`fixed-point-theorems, PrimeNumberTheoremAnd, Zeta3Irrational, rellich-kondrachov, carleson, StrongPNT,
  AbsorptionCutoff, AINTLIB, ClassFieldTheory, schoenflies-lean, SphereEversion, gromov`).
- `patches/` holds 23 patch files (≈160k lines total) touching third-party deps only. They do not touch
  Mathlib or the Challenge files.
- Assessment: this code is dependency-preparation logic, not checking logic. It cannot alter the Challenge
  statements (which depend only on unpatched Mathlib). It does run before Comparator, as for any user of the repo.

## 5. Solution import closure (static, textual — no compilation)
Computed with `tools/imports.py` (recursive parse of `import` lines):
- `OAI.Analysis.Mahler.MainTheorem`: 229 local `OAI.*` modules; external roots: **Mathlib only**.
- `OAI.Geometry.PolarProducts.Main`: 46 local `OAI.*` modules (incl. an in-repo nonsqueezing development:
  `Nonsqueezing.lean`, `CanonicalCylinder.lean`, …, ≈12.2k lines); external roots: **Mathlib only**.
- Hence none of the 23 patched third-party packages is in either target's import closure; the repo README's
  `lake update` (whose only effect beyond resolution is the post_update patching) is not needed for these
  two targets. Per the task instructions `lake update` was **not** run; `lake-manifest.json` was used as-is.

## 6. Plan for dependency preparation
- `lake exe cache get` (Mathlib's official cache tool, built from Mathlib @ d13f23b7…, downloading from
  `https://cache.mathlib.org`), no `lake update`. No OAI `.olean` from any source; `lean/.lake/build` did not
  exist before the Comparator runs.
