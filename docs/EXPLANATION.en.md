# A reading map of the polar-product argument

[English](EXPLANATION.en.md) | [中文](EXPLANATION.zh-CN.md) · [Home](../README.md)

This is a guide to the argument already examined in the earlier audit, not a new proof or an independent certification of every line. The source is the [pinned polar-product manuscript](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections). The longer original reading record is [audit_zh.md](../evidence/manual/audit_zh.md).

## The target and the payoff

For a symmetric convex body $K$, place $K$ in position coordinates and its polar $K^\circ$ in momentum coordinates. The theorem obtains smooth symplectic balls of every capacity $c<4$ inside the open product. Symplectic maps preserve volume, and the capacity-$c$ ball has volume $c^n/n!$. Therefore the embeddings imply

$$
|K||K^\circ|\geq c^n/n!\quad\text{for every }0<c<4,
$$

and taking the limit in this scalar inequality gives the symmetric Mahler bound. This step does not require an embedding at $c=4$ or a limit of embedding maps.

## The construction in five steps

**1. Turn a high-order holomorphic zero into a ball.** A tuple $f$ with a unique common zero leads to a potential $|z|^2+|f(z)|^2$. A local radial replacement exposes a ball, and a compactly supported Moser deformation transports it back. The reading checked that the modified potentials retain a common compact support and that the inner radius is fixed before the smoothing parameter is reduced. Large volume alone would not be enough; this construction supplies an actual embedding.

**2. Obtain a bound uniform over all planar slices.** A conformal lens supplies an inverse map $g$ and horizontal primitives $J_k$. The required estimate is

$$
|J_k(v,t)|/k\leq (\pi/4)|g(v+it)|^{2k}+\epsilon_k,\qquad\epsilon_k\to0,
$$

uniformly in the point. The slice can approach a tip as $k$ changes. The delicate error is bounded using

$$
I(k,a)=k\int_a^1r^{2k-1}\sqrt{\frac{1-r}{r-a}}\,dr\leq1+\pi/e.
$$

The substitution $H=k(1-a)$ and $y=k(1-r)$ makes the moving endpoint explicit. A fixed cutoff is chosen before $k$ grows. This is the part where pointwise convergence would not suffice.

**3. Realize the form inside a scaled polar product.** For a fixed finite-strip body, write $z=u+ix$ and set

$$
q=x,\qquad p=-u-\sum_jJ_k(b_j\cdot u,b_j\cdot x)b_j.
$$

The pullback gives the needed symplectic form. For two inputs at the same $x$, monotonicity gives

$$
(p_2-p_1)\cdot(u_2-u_1)\leq-\|u_2-u_1\|^2,
$$

which proves global injectivity, not merely local nondegeneracy. A support-function estimate puts the image in $\operatorname{int}K\times S\operatorname{int}K^\circ$.

**4. Balance the two scales.** The holomorphic construction produces balls below capacity $\pi k$, while the momentum scale can be taken as $S=(1+\eta)\pi k/4$. Scaling only momentum by $1/S$ is not symplectic. The proof also enlarges the source by $\sqrt S$, so the two factors in the pulled-back form cancel. For a fixed $c<4$, choose $(1+\eta)c<4$ and then a sufficiently large $k$.

**5. Approximate an arbitrary body and match the upper bound.** Finite approximation in the polar gives $K\subset K'\subset(1+\alpha)K$ and $(K')^\circ\subset K^\circ$. For each desired capacity, first fix the approximation and its number of constraints, then choose $k$. No limit of embeddings is required. A supporting-cylinder construction, together with nonsqueezing, gives the matching upper bound of 4.

## What this explains about the earlier route

The earlier user-led work handled special polytope families and explicit volume formulas. A global classification reduction remained a separate obstacle. The argument above handles arbitrary finite strip lists and then approximation, so it does not need a fixed bound on the number of vertices or facets.

This explains why an all-dimensional result can overtake a family-by-family program. It does not by itself decide whether the older formulas or constructions are novel or useful; those are separate mathematical questions.

## Where to inspect next

The original source sections are `ball.tex`, `planar.tex`, `realization.tex` and `approximation.tex` under the pinned directory linked above. Read them alongside [SEMANTICS.md](../evidence/machine/SEMANTICS.md) to keep the prose target and formal target aligned.

The finite numerical tests in `evidence/manual/diagnostics.json` are diagnostic samples, not interval certificates or a proof over an infinite parameter space. They are supplementary to the analytic reading and the later formal replay.
