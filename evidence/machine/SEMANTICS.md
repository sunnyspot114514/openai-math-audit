# SEMANTICS — do the Challenge statements say what the papers claim?

Sources compared:
- Challenge statements (trusted side, checked by Comparator to be *identical* to what the Solution proves):
  `lean/ComparatorChallenges/MahlerConjecture.lean`, `lean/ComparatorChallenges/SymmetricPolar.lean`.
- Papers: `preprints/The-symmetric-Mahler-conjecture-and-its-equality-cases-September-22-2026/paper.pdf`
  (Theorem 1.1), `preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/paper.pdf`
  (Theorem 1.1); scope note `lean/docs/087.md`.
- Elaborated definitions printed from the built Challenge oleans (inside landrun): `axcheck-DefsMahler.out`,
  `axcheck-DefsPolar.out` (+ small `rfl`/`simp` sanity facts in `axcheck/*.lean`, all accepted, exit 0).

Comparator guarantees the Solution theorem has *exactly* the Challenge type, with every constant in that type
(e.g. `coordinatePolar`, `gromovWidth`, Mathlib's `volume`, `ContDiffOn`) identical in both environments.
So the semantic question reduces to reading the Challenge files. Method: read every definition the statement
unfolds to; no proof content was used to judge meaning.

## 1. Target 1 — `OAI.SymmetricMahler.symmetric_mahler`

```lean
def coordinatePolar (K : Set (I → ℝ)) : Set (I → ℝ) := {p | ∀ v ∈ K, (∑ i, p i*v i) ≤ 1}
theorem symmetric_mahler {n : ℕ} (hn : 1 ≤ n)
    {K : Set (Fin n → ℝ)} (hK : IsCompact K) (hconv : Convex ℝ K)
    (hsym : ∀ x ∈ K, -x ∈ K) (hint : (interior K).Nonempty) :
    (4:ℝ)^n/(Nat.factorial n:ℝ) ≤ (volume K).toReal*(volume (coordinatePolar K)).toReal
```
Paper Thm 1.1: for every integer n ≥ 1 and every origin-symmetric convex body K ⊂ ℝⁿ (convex body = compact
convex with nonempty interior; K = −K), |K||K°| ≥ 4ⁿ/n!, |·| = n-dimensional Lebesgue volume,
K° = {y : ⟨x,y⟩ ≤ 1 ∀x∈K}.

| Item | Lean | Paper | Match |
|---|---|---|---|
| Dimension | every `n` with `1 ≤ n` | every n ≥ 1 | yes |
| Space | `Fin n → ℝ` (product topology = Euclidean topology; linear structure standard) | ℝⁿ | yes |
| Compact / convex / int ≠ ∅ | `IsCompact K`, `Convex ℝ K`, `(interior K).Nonempty` | convex body | yes |
| Origin symmetry | `∀ x ∈ K, -x ∈ K` (negation is an involution ⇒ K = −K) | K = −K | yes |
| Volume | `MeasureTheory.volume` on `Fin n → ℝ`; checked `volume = Measure.pi (fun _ => volume)` by `rfl` and `volume (Icc 0 1) = 1` | Lebesgue measure | yes (standard Lebesgue, unit cube = 1) |
| Polar | `∑ i, p i * v i ≤ 1` for all `v ∈ K` (standard dot product) | ⟨x,y⟩ ≤ 1 ∀x∈K | yes |
| Conclusion | `4^n / n! ≤ vol(K).toReal * vol(K°).toReal`, in ℝ | ≥ 4ⁿ/n! | yes; direction and constant as claimed |

Remarks.
- `ENNReal.toReal`: vol(K) < ∞ since K is compact; under the hypotheses 0 ∈ int K, so K° is bounded and
  closed, vol(K°) < ∞. So the real-valued product equals the true volume product. In any case `toReal ∞ = 0`
  would make the inequality *false*, so the cast cannot make the statement vacuous.
- No added hypotheses, no weakened conclusion. The equality classification (paper's second sentence) is not part
  of this target (it is `SymmetricMahlerEquality.json`, out of scope).

## 2. Target 2 — `OAI.SymmetricPolar.symmetric_polar_main`

```lean
abbrev Position (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev Phase (n : ℕ) := Position n × Position n
def IsSymmetricConvexBody (K) : Prop := IsCompact K ∧ Convex ℝ K ∧ (interior K).Nonempty ∧ ∀ x, x ∈ K ↔ -x ∈ K
def polar (K) := {p | ∀ q ∈ K, inner (𝕜 := ℝ) q p ≤ 1}
def polarProduct (K) := interior K ×ˢ interior (polar K)
def capacityBall (n) (c : ℝ) := {z | Real.pi * (‖z.1‖ ^ 2 + ‖z.2‖ ^ 2) < c}
def omega0 (v w : Phase n) : ℝ := inner v.1 w.2 - inner w.1 v.2
def HasSymplecticEmbedding (U V) : Prop := ∃ e : Phase n → Phase n,
    ContDiffOn ℝ ∞ e U ∧ Topology.IsEmbedding (fun z : U => e z) ∧ MapsTo e U V ∧
    ∀ z ∈ U, ∀ v w, omega0 (fderiv ℝ e z v) (fderiv ℝ e z w) = omega0 v w
def gromovWidth (U) : ℝ≥0∞ := sSup (ENNReal.ofReal '' {c | 0 < c ∧ HasSymplecticEmbedding (capacityBall n c) U})
theorem symmetric_polar_main {n : ℕ} (hn : 2 ≤ n) (K) (hK : IsSymmetricConvexBody K) :
    gromovWidth (polarProduct K) = 4 ∧ ∀ c : ℝ, 0 < c → c < 4 → HasSymplecticEmbedding (capacityBall n c) (polarProduct K)
```
Paper Thm 1.1: for every integer n ≥ 2 and every origin-symmetric convex body K ⊂ ℝⁿ, c_G(int K × int K°) = 4,
and for every 0 < c < 4 there is a smooth symplectic embedding B²ⁿ(c) ↪ U_K, where
ω₀ = Σ dq_j ∧ dp_j on ℝⁿ_q × ℝⁿ_p, B²ⁿ(c) = {π(|q|²+|p|²) < c}, c_G(U) = sup of c admitting a smooth embedding
e : B²ⁿ(c) → U with e*ω₀ = ω₀.

| Item | Lean | Paper | Match |
|---|---|---|---|
| Dimension | every `n` with `2 ≤ n` | every n ≥ 2 | yes |
| Convex body | compact ∧ convex ∧ int ≠ ∅ ∧ (x∈K ↔ −x∈K) on `EuclideanSpace ℝ (Fin n)` | same | yes |
| Polar | `⟪q,p⟫ ≤ 1 ∀ q∈K`, Euclidean inner product | same | yes |
| Domain | `interior K ×ˢ interior (polar K)`, K in position, K° in momentum | U_K = int K × int K° | yes |
| Ball / capacity normalisation | `π(‖q‖²+‖p‖²) < c`, Euclidean norms (radius r ↔ capacity πr²) | B²ⁿ(c), cap(B(r)) = πr² | yes |
| Symplectic form | `ω₀(v,w) = ⟪v_q,w_p⟫ − ⟪w_q,v_p⟫` = Σ_j (dq_j∧dp_j)(v,w); sanity: ω₀(e_{q1}, e_{p1}) = 1 checked | Σ dq_j ∧ dp_j | yes (standard sign) |
| Smoothness | `ContDiffOn ℝ ∞ e U`; printed as `ContDiffOn ℝ (↑⊤) e U`; checked `(∞ : WithTop ℕ∞) = ↑(⊤ : ℕ∞)` by `rfl` and `∞ < ω` (so C^∞, not analytic) | smooth | yes |
| Embedding | `Topology.IsEmbedding` of `e` restricted to `U` (injective, homeomorphism onto image) + `MapsTo e U V` | embedding B → U | yes (see remark) |
| Symplectic condition | `ω₀(De(z)v, De(z)w) = ω₀(v,w)` ∀ z ∈ U, ∀ v w | e*ω₀ = ω₀ | yes |
| Gromov width | `sSup` in ℝ≥0∞ of capacities c > 0 that embed | supremum of such c | yes |
| Conclusion | width = 4 **and** every 0<c<4 embeds; nothing claimed at c = 4 | same | yes |

Remarks.
- `e` is a total function on `Phase n` but only constrained on `U`; `U = capacityBall n c` is open, so for
  z ∈ U `fderiv ℝ e z` is the genuine derivative of e|U (ContDiffOn on an open set ⇒ differentiable there; the
  junk value 0 of `fderiv` cannot satisfy the ω₀ condition, since ω₀ is nondegenerate).
- The ω₀-preservation makes each De(z) a symplectic, hence invertible, linear map, so e is an immersion; with
  `IsEmbedding` this is a smooth embedding in the usual sense. Notion is not weaker than the paper's.
- `Phase n` carries Lean's product (sup) norm, but the ball is written with the explicit Euclidean sum
  ‖q‖²+‖p‖², and derivatives in finite dimension do not depend on the chosen norm.
- `gromovWidth = 4` contains both the lower bound and the upper bound (no symplectic embedding of B(c) for any
  c > 4 — a nonsqueezing-type statement). The Solution proves the upper bound via an in-repo nonsqueezing
  development (`OAI/Geometry/PolarProducts/Nonsqueezing.lean`, `CanonicalCylinder.lean`, …); its content was
  kernel-checked by Comparator's replay but not reviewed by this audit (not needed for the verdict).

## 3. Conclusion
No mismatch, added hypothesis, weakened conclusion or definitional deviation was found for either target relative
to the cited paper theorems (for Mahler: inequality part only; for the polar product: full Theorem 1.1).
Modelling choices that differ in form but not in meaning: Mahler uses `Fin n → ℝ` with an explicit coordinate
pairing instead of `EuclideanSpace`; the polar target uses an explicit product type and spells out ω₀,
balls and Gromov width by hand rather than using a library symplectic-geometry API (Mathlib has none).
