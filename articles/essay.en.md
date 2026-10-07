# When generation gets cheaper, verification and explanation matter more

**SUNNY99 · October 7, 2026**  
[中文](zhihu.zh-CN.md) · [Repository home](../README.md)

My first plan was the same as before: check the results, then comment on the announcement.

I have argued this several times already: **as AI makes it cheaper to produce candidate ideas, proofs and papers, verification and explanation deserve more of our attention.**

Writing a manuscript is one stage of research. We still need to establish what it proves, whether the argument survives independent checking, how it relates to prior work, which mathematical structure does the real work, and whether another researcher can use it.

Then I opened OpenAI's mathematical repository and found something rather personal. A direction I had spent about two months exploring with AI had just been overtaken by a general result.

In July, I discussed AI tackling open mathematical problems on Zhihu. An August reply proposed Viterbo/Mahler as a challenge: let the AI enthusiasts try that, perhaps starting with symmetric Viterbo.

I actually tried. I worked from GPT-5.6 Pro through GPT-6 Pro, repeatedly generating candidates, checking steps and discarding failed routes. I jokingly called it “gacha”—sampling attempts—but the process involved checking those attempts rather than keeping only the most persuasive output. After two months, I had some candidate results for special cases, not a complete proof. This release included a general result covering the target I had been working toward.

**There is a little disappointment, but my overall reaction is positive.**

I have long expected AI to produce substantive results on increasingly difficult mathematical problems. Which problems would fall first, who would solve them and how soon were much harder to predict. This time, the development happened to land in a direction I had personally spent time on.

That made it a natural case to investigate closely.

## 1. More than an LLM saying that a proof looks right

I first used GPT-6 Pro to examine the main argument. The reading focused on possible failure points: uniform estimates near endpoints, global rather than merely local embedding properties, symplectic scaling, and the passage from finite polytopes to arbitrary convex bodies.

No specific gap was found in that reading. But a model's favorable review was not enough.

I then had a Grok bot run Lean/Comparator under a separately configured non-privileged audit account. It returned original logs, exit codes, versions, axiom outputs and modification records. GPT-assisted work then cross-checked the delivered package. The [audit overview](../docs/AUDIT.en.md) explains the division of work.

**Grok executed the run. The Lean kernel checked the formal proof. GPT assisted with reading and review. This was not simply two models agreeing with each other.**

The audited `openai/math` commit was fixed:

```text
adc7f1241b42e322a6451854ab7e4b4c146bf78a
```

The first target was the symmetric Mahler inequality in every positive dimension:

$$
|K|\,|K^\circ|\geq\frac{4^n}{n!}.
$$

Here $K$ is any compact, convex, origin-symmetric body with nonempty interior. There is no extra bound on its vertices or facets, no smooth-boundary requirement and no special coordinate symmetry. In dimension four, the constant is $32/3$, the bound I had been working with. See the [fixed statement](../evidence/machine/preaudit-copies/MahlerConjecture.lean).

The second target was the width of symmetric polar products:

$$
c_G\!\left(\operatorname{int}K\times\operatorname{int}K^\circ\right)=4,
\qquad n\geq2.
$$

It also includes smooth symplectic embeddings for every ball capacity $0<c<4$. The objects, capacity normalization and embedding definitions were checked against the mathematical target. See the [statement](../evidence/machine/preaudit-copies/SymmetricPolar.lean) and [semantic review](../evidence/machine/SEMANTICS.md).

Both recorded runs succeeded:

| Target | Comparator exit | Recorded wall time | Result |
|---|---:|---:|---|
| Symmetric Mahler inequality | 0 | 11 minutes 21 seconds | Default Lean kernel accepted |
| Symmetric polar-product width | 0 | 47 minutes 52 seconds | Default Lean kernel accepted |

These are verification times after dependency preparation, with an official Mathlib cache. They are neither complete clean-machine setup times nor proof-discovery times. The [machine report](../evidence/machine/REPORT.md) gives the details.

Both original stdout logs end with:

```text
Running Lean default kernel on solution.
Lean default kernel accepts the solution
Your solution is okay!
```

Those messages are in the execution records, not only in the bot's summary: [Mahler log](../evidence/machine/mahler.stdout.log) and [polar-product log](../evidence/machine/polar.stdout.log).

Comparator matters because ordinary compilation alone is not the full claim. Under its documented trust assumptions, it checks correspondence with the fixed target, permitted axiom use and kernel replay of the exported solution. Its [documentation](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md) specifies that contract.

The separate axiom outputs contain only `propext`, `Classical.choice` and `Quot.sound`. There is no `sorryAx` or added assumption that the Mahler conjecture is true. See the [Mahler output](../evidence/machine/axcheck-AxMahler.out) and [polar output](../evidence/machine/axcheck-AxPolar.out).

The limits remain important. This was one Lean kernel, not a dual-kernel check. Cache use and isolation adaptations are disclosed. The audit account shared a host with other work; it was not a certified clean standalone virtual machine. The final cross-check reviewed the delivered evidence and did not run Lean again. Those qualifications are retained in the [audit overview](../docs/AUDIT.en.md).

**For these two precise statements, I now regard the evidence as sufficient to accept the results.**

That does not extend the audit to the entire repository, general nonsymmetric Mahler, Hanner equality cases or every version of Viterbo's conjecture.

## 2. What does “722 manuscripts” mean?

**It does not mean 722 mutually independent open conjectures.**

The upstream collection groups the manuscripts into 372 families. A family can include a principal result, a companion argument, a consequence or another proof. The verification status also varies; not every manuscript has a Lean formalization. This is explicit in the [pinned README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md).

That does not diminish results that are correct. It means the claims should be examined individually. I checked two targets and draw conclusions about those two targets.

The “Quasi-Riemann” label in the headline should not be substituted for the full Riemann hypothesis. I did not conduct an equivalent replay of that part of the release, so my Mahler audit is not evidence that it has passed the same check.

OpenAI also describes an internal frontier model and a compute-equivalence estimate of roughly three hours. That is not a promise that a current public Pro subscription can reproduce the discovery in three hours. See the [official announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/).

**Whether a result is correct and whether the public can reproduce its discovery process are separate questions.**

## 3. Verification and explanation need resources too

This experience makes a familiar concern much more concrete.

The supply of candidate results can grow quickly. The supply of trustworthy knowledge does not automatically grow at the same rate.

A proof may fail at an unobtrusive step. A theorem may already exist in another language or formulation. A successful formalization may still need a careful check that it expresses the intended question rather than a weaker one.

I would like research resources and evaluation to recognize these tasks more seriously. Precise statements, stable versions, preserved verification logs, literature checks, corrections and readable exposition all deserve sustained effort. A small number of volunteers should not have to absorb the whole cost of making large releases usable.

**By explanation, I mean more than smoother prose.**

Here I am talking about mathematical understanding, not merely access to a model's internal activations or a transcript of its reasoning. Why does the construction work? How does it avoid the earlier obstacle? Which assumptions are essential? Which steps can be transferred to another problem?

My own earlier difficulty was the passage from special classes to arbitrary convex bodies. The new route works with arbitrary finite-strip bodies and then uses approximation in the polar. I therefore care about why it does not need the finite classification reduction I was trying to obtain, not only about the final inequality. The [proof map](../docs/EXPLANATION.en.md) summarizes that distinction.

These explanations affect how later researchers choose questions and tools. Even a verified result must be understood, taught and compared before it becomes knowledge that others can use fluently.

I agree with the parts of AGMAI's recommendations that call for careful attribution and exposition, formal artifacts where possible, and support for community understanding. Its document also opposes testing advanced mathematical problems on proprietary models. That is a separate position and should not be conflated with my broadly positive reaction to this release; supporting the responsibilities above is not an endorsement of every recommendation. See the [AGMAI document](https://agmai.org/general-sep29/).

**AI can help with verification and explanation as well.**

I am not proposing a protected category of work that must be reserved for humans. This audit used AI extensively for reading, environment preparation, log handling, semantic checks and cross-review.

What matters is what each stage checks, what it relies on and what evidence it leaves. Use a formal checker where it applies. Carry out separate reviews of mathematical meaning, literature connections and scope. Another reassuring model answer does not automatically complete those stages.

Original exploration remains valuable. Good questions and new connections still matter. But when generation accelerates, verification, explanation and knowledge organization should not remain afterthoughts.

## 4. My overall assessment is positive

A stronger general result overtaking two months of partial work brings some disappointment. The older formulas, constructions and certificates may still merit attention, but that should be decided individually rather than by promising in advance that every piece is publishable.

I accepted the original challenge because I believed AI was already worth using seriously for this kind of exploration. Now there is a more complete result, supported by a much stronger verification record. The reasonable response is to acknowledge it, understand it and decide what to do next.

**Not obtaining the first proof and having been right that the direction was worth exploring can both be true.**

I hope the discussion increasingly moves from how many problems were announced to the individual results.

Check the proofs. Explain the key ideas. Make the results usable by other researchers. As generation improves, those activities should become a more deliberate part of research infrastructure.

I already regarded that as an important direction. This release simply gave me an unusually personal example.

---

**Evidence:** [repository home](../README.md) · [audit overview](../docs/AUDIT.en.md) · [new Lean replay guide](../docs/REPRODUCE.en.md) · [provenance](../docs/PROVENANCE.en.md).

The personal chronology is the author's account. Audit conclusions are limited to the fixed targets, records and trust assumptions documented here. Relative links are intended for GitHub; when republishing elsewhere, replace them with the actual published repository URLs.
