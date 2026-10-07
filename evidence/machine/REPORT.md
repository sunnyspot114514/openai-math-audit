> PUBLICATION COPY: host identifiers or unrelated host paths have been pseudonymized. See docs/PROVENANCE.en.md and evidence/provenance/publication_map.json. Verification results and target statements are unchanged.

# Independent Comparator replay — openai/math @ adc7f1241b42e322a6451854ab7e4b4c146bf78a

Date: 2026-10-07 (times are UTC+8). Machine: Debian 13 container, kernel 6.12.94+, 8 vCPU, 16 GB RAM, no swap.
Every statement here is backed by a file in this directory.

## 1. Verdicts

| Target | Config | Theorem | Verdict | Comparator exit code | Wall time | Max RSS* | CPU (user+sys) |
|---|---|---|---|---|---|---|---|
| 1 | `ComparatorChallenges/MahlerConjecture.json` | `OAI.SymmetricMahler.symmetric_mahler` | **VERIFIED** | **0** (`mahler.exitcode`) | 11:21 (681.2 s) | 5,092,760 KB (≈4.9 GiB) | 1440.7 s + 674.5 s |
| 2 | `ComparatorChallenges/SymmetricPolar.json` | `OAI.SymmetricPolar.symmetric_polar_main` | **VERIFIED** | **0** (`polar.exitcode`) | 47:52 (2872.4 s) | 4,932,756 KB (≈4.7 GiB) | 1043.6 s + 732.7 s |

*GNU time `-v` max RSS = largest single process in the waited tree, not the sum. Lowest sampled MemAvailable during
runs: 3.2 GB (Mahler), 4.8 GB (Polar) (`*.memsamples.txt`). No OOM.

Final lines of both stdout logs: `Running Lean default kernel on solution.` / `Lean default kernel accepts the solution` /
`Your solution is okay!`. stderr (33 lines each) contains only lake's `repository … has local changes` warnings for
11 patched packages (§6). The only `sorry` warning is the Challenge goal placeholder
(`ComparatorChallenges/<X>.lean: declaration uses 'sorry'`), which is expected.

What Comparator checked (comparator source `Main.lean`, `compareIt`/`verifyMatch`): Challenge and Solution each built with
`lake build` inside landrun, exported with lean4export inside landrun; then (a) every constant in the theorem statements,
the permitted axioms and kernel primitives match between Challenge and Solution exports; (b) the theorem's transitive axiom
set ⊆ {propext, Quot.sound, Classical.choice}; (c) the whole Solution export is replayed into the Lean 4.34.1 kernel. No
second kernel: both configs have `enable_nanoda: false` and no `external_kernels`; configs were run unmodified.

## 2. Axioms
- Comparator `checkAxioms` passed for both (it would have aborted with a non-zero exit otherwise).
- Independent post-hoc `#print axioms`, run in a separate `lean` process **inside landrun** (read-only FS except `/dev`,
  no network, AF_UNIX restricted) because it loads sandbox-built oleans (`axcheck-run.sh`, `axcheck-*.out`, exit codes in
  `axcheck-exitcodes.txt`):
  - `OAI.SymmetricMahler.symmetric_mahler` depends on axioms: `[propext, Classical.choice, Quot.sound]`
  - `OAI.SymmetricPolar.symmetric_polar_main` depends on axioms: `[propext, Classical.choice, Quot.sound]`
  - No `sorryAx`, nothing outside the permitted set. The printed Solution types are the Challenge statements.
  (A first attempt of `DefsMahler` failed only because my own sanity lemma used a wrong Mathlib lemma name — kept as
  `axcheck-DefsMahler.attempt1-out.txt`; fixed rerun exit 0.)
- No repo-wide grep was used to decide correctness.

## 3. Environment and isolation
- **Separate UID**: all audit work ran as `mathaudit` (uid 1001, gid 1001, no supplementary groups, no sudo:
  `sudo -n true` → "a password is required"), with an empty fresh HOME `/home/mathaudit` (mode 700), launched as
  `sudo -u mathaudit env -i HOME=… USER=… LOGNAME=… SHELL=/bin/bash LANG=C.UTF-8 PATH=~/.elan/bin:~/go/bin:~/bin:/usr/local/bin:/usr/bin:/bin bash -c …`
  (`ma.sh`; full env of each run saved at the top of `*.cmd.txt`). The box user's sudo was used only to create this
  user, install `acl`/`time` from Debian apt, and add an ACL.
- **Credential reachability** (`credential-readability-scan.txt`): for uid 1001, `/home/host-user` (mode 700, contains
  `~/.config/gh/hosts.yml` with the live GitHub token) is **not readable**; `/home/host-user/.ssh` does not exist; `/root` not
  readable; `/workspace` (other projects, incl. `/workspace/other-project`) is **not readable** thanks to an ACL
  `user:mathaudit:---` added on `/workspace` for this audit (still in place; remove with `sudo setfacl -x u:mathaudit /workspace`).
  A by-name scan found no credential files readable outside the audit HOME. Still readable (world-readable): `/tmp` contents
  of other work (e.g. Python venvs, a file named `/tmp/unrelated-host-entry` whose content was not read), `/exec-daemon`,
  `/opt`, system dirs. Comparator's landrun policy grants read access to the whole FS by design, so the UID separation is
  what keeps the gh token and the projects unreachable.
- **landrun (real Landlock, no fake-landrun)**: `Zouuup/landrun` main @ `811cfff5`, v0.1.18, built from source with Go 1.24.4.
  Kernel LSMs `capability,landlock,selinux`; Landlock ABI **6** (`landlock_create_ruleset` VERSION query). Comparator invokes
  `landrun --best-effort --ro / --rw /dev -ldd -add-exec [--env …] --ro <project> --rwx <project>/.lake --rox <lean prefix> --rox <git> -- lake build <module>`
  (build) and a no-write variant for lean4export. go-landlock requests V9; best-effort downgrades to the kernel's ABI 6, which
  still enforces FS access rights, TCP bind/connect (ABI ≥4) and abstract-UNIX-socket/signal scoping (ABI 6). Self-test as
  uid 1001 (`landrun-selftest.log`): write outside allowed dir → `Permission denied` (rc 2); write inside `--rwx` dir → rc 0;
  TCP connect to github.com:443 → "Could not connect" (rc 7); landrun reports "Landlock restrictions applied successfully".
- **AF_UNIX restriction (README's systemd-run line)**: the README launch is
  `systemd-run --property=RestrictAddressFamilies=~AF_UNIX --user --pty -E PATH="$PATH" --working-directory $(pwd) -- bash -c 'lake env comparator …'`.
  This host has no systemd (PID 1 = `tini`, no `/run/systemd`), so `systemd-run --user` cannot run. Instead of skipping it,
  I wrote `restrict-af-unix` (`restrict_af_unix.c`, 50 lines, gcc 14.2): sets `PR_SET_NO_NEW_PRIVS`, installs a seccomp-BPF
  filter (TSYNC) that makes `socket(2)` with domain `AF_UNIX` fail with `EAFNOSUPPORT`, kills non-x86_64 arch syscalls and
  answers x32-ABI syscalls with ENOSYS, then `execvp`s the command; the filter is inherited by every descendant (lake,
  comparator, landrun, lean, lean4export) and cannot be removed. This mirrors systemd's documented semantics
  (`systemd-RestrictAddressFamilies-doc-excerpt.txt`: only `socket(2)` is restricted; `socketpair()` unaffected). Tested:
  AF_UNIX socket → `[Errno 97] Address family not supported`, AF_INET ok, socketpair ok, `/proc/self/status` shows
  `Seccomp: 2`, `NoNewPrivs: 1`. Deviation from the README: a custom wrapper instead of systemd-run (`--pty` and the
  systemd transient unit are not reproduced; neither is a sandboxing property). Isolation was never disabled or weakened.
- **Lean**: repo `lean/lean-toolchain` = `leanprover/lean4:v4.34.1`; actually used = Lean 4.34.1 (commit
  `5045d0056413266e57c625dcd7c365b10e377c52`), Lake 5.0.0-src+5045d00, from a **fresh elan 4.2.4** install in the audit HOME
  (box toolchains not reused). Mathlib's own `lean-toolchain` is also v4.34.1.
- **Tools** (`VERSIONS.txt`): comparator `d03acab154d269c06e60e4de7e4cc85deebff94b` + lean-toolchain pin v4.34.0→v4.34.1;
  lean4export `076e8e57707e813375e8f9da8bf989799ace9680` (= tag v4.34.0), built with v4.34.1; landrun `811cfff5`; nanoda not used.
  No prior binaries from `/workspace/other-project` were reused (not even readable by uid 1001).

### Comparator tool patch (separate from the repo under test)
`tool-patch-comparator-toolchain.diff` is a one-line change to comparator's `lean-toolchain`
(`leanprover/lean4:v4.34.0` → `leanprover/lean4:v4.34.1`). No Lean source changed. Reason: lean4export reads the project's
`.olean` files, which Lean only accepts from the identical Lean build, so lean4export (and comparator, which shares the
workspace) must be compiled with v4.34.1; upstream has no v4.34.1 tag, d03acab is the last v4.34.x commit, and
`d03acab..master` contains only toolchain bumps (README byte-identical — `comparator-README-d03acab.md`, `comparator-README-master-ca04cfc.md`).
Effect: the checking logic is unchanged; the in-process kernel replay uses the v4.34.1 kernel, i.e. the same Lean the
project targets. It aligns the checker with the project and does not relax any check.

## 4. Procedure and exact commands
1. `git clone https://github.com/openai/math.git && git checkout adc7f1241b42e322a6451854ab7e4b4c146bf78a`;
   `git rev-parse HEAD` = adc7f124…; `git status --porcelain` empty (`git-log-1.txt`).
2. Pre-audit read of lakefile, manifest, toolchain, both configs, both Challenge files, docs/087.md before any build
   (`PREAUDIT.md`, `preaudit-copies/` with SHA256SUMS). Challenges import only `Mathlib`; no `run_cmd`/`elab`/`macro`/
   `initialize`/`extern`/`implemented_by`/`native_decide`/`unsafe`/`axiom` in them. Solution import closures (static): Mathlib + 229
   (Mahler) / 46 (Polar) local OAI modules.
3. Dependencies: `lake exe cache get` from `lean/` (exit 0, 2:58, `deps-cache-get.*`): Mathlib cache from
   `https://cache.mathlib.org/mathlib4-master`, 8908 files, built by Mathlib's own cache tool @ d13f23b7…. **No `lake update`**
   (manifest unchanged). No OAI oleans from anywhere; `lean/.lake/build` did not exist before the Comparator runs. Note: the repo
   README says `lake update`; it was skipped per task instructions, and its only extra effect (post_update patches of 12
   packages) concerns packages outside both targets' import closures (`DEPENDENCIES.txt`).
4. Runs (`run_comparator.sh`; exact command and env in `mahler.cmd.txt` / `polar.cmd.txt`), from `lean/`, as uid 1001:
   ```
   /usr/bin/time -v -o out/mahler.time.txt restrict-af-unix bash -c 'lake env comparator ComparatorChallenges/MahlerConjecture.json' > out/mahler.stdout.log 2> out/mahler.stderr.log ; echo $? > out/mahler.exitcode
   /usr/bin/time -v -o out/polar.time.txt  restrict-af-unix bash -c 'lake env comparator ComparatorChallenges/SymmetricPolar.json'  > out/polar.stdout.log  2> out/polar.stderr.log  ; echo $? > out/polar.exitcode
   ```
   No `tee`; stdout and stderr redirected straight to files; the exit code is `$?` of `/usr/bin/time`, which passes through the
   child's status (`Exit status: 0` also in `*.time.txt`); `bash -c` hands back `lake env`'s status, which is comparator's.
   Mahler 19:35:12–19:46:33, Polar 19:46:43–20:34:36 (UTC+8), run one after the other.
5. After the runs: built OAI oleans = 277 = 2 Challenge + 229 + 46 Solution modules, exactly the static closures; only
   Mathlib-closure packages have build outputs (from the cache).

## 5. Semantics (details in `SEMANTICS.md`)
No mismatch found. Mahler: all n ≥ 1; compact, convex, origin-symmetric, nonempty interior; standard Lebesgue `volume` on
`Fin n → ℝ` (checked `= Measure.pi volume` by rfl, unit cube volume 1); polar by standard dot product; conclusion
`4^n/n! ≤ |K|·|K°|` (via `toReal`, finite here; it could not make the statement vacuous). Polar product: n ≥ 2; same body
hypotheses on `EuclideanSpace ℝ (Fin n)`; Euclidean polar; U = int K × int K°; ball `π(|q|²+|p|²) < c` (capacity πr²);
ω₀ = Σ dq_j∧dp_j; C^∞ (`∞ = ↑⊤ : WithTop ℕ∞`, not analytic) topological embedding with ω₀-preserving derivative; Gromov
width = sSup; conclusion = width 4 and embeddings for every 0<c<4, nothing at c=4. This matches paper Theorem 1.1 and docs/087.md.
The Mahler equality classification is not part of target 1 (out of scope).

## 6. "repository … has local changes" warnings
Packages: belyi, formal-schemes, elliptic-curves, tempered-fundamental-groups, oka, orbicurve-cores, pi1, heights, genl,
tate-curves-theta, iut. Cause: the **repo's own lakefile `run_cmd`** cloned each at its pinned commit and applied
`lean/patches/<pkg>-lean4341.patch` (log: `deps-cache-get.log`, "applied compatibility patch before dependency resolution").
Not from the Mathlib cache and not from any auditor edit: each HEAD equals the manifest rev and each working-tree diff is
exactly the repo patch (`git apply --check --reverse` OK; changed paths = patch files; no untracked files —
`package-local-changes.txt`). None of these packages is imported by either Challenge or either Solution, and none received
build output. The trusted Challenge closure (Mathlib, batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient,
plausible) has 0 tracked changes.

## 7. Workspace diff
`workspace-diff.txt`: `git status --porcelain` empty, `git diff` empty after both runs; only ignored `lean/.lake/` present.
No code change was needed, so there is only one (original) run per target. `PATCHES.txt`: repo none; verification-tool
toolchain pin only.

## 8. Limitations
- systemd-run replaced by a custom but equivalent seccomp wrapper (§3), because the host has no systemd.
- Landlock ABI 6 kernel (< the Linux 7.1 fix the comparator README mentions); the AF_UNIX restriction is the README's own
  mitigation for that and was applied.
- Comparator's sandbox can read the whole FS (by design); world-readable `/tmp` entries of other work stay readable by
  uid 1001 (no credentials found there by name scan). gh token, `/home/host-user` and `/workspace` were not readable.
- Single kernel (Lean 4.34.1); nanoda not run because the configs do not ask for it.
- Trust in the Mathlib binary cache (official cache.mathlib.org, Mathlib's own tool) as the Comparator README permits;
  Mathlib was not rebuilt from source.
- The proofs themselves (e.g. the in-repo nonsqueezing development) were kernel-checked, not read by a human.
- `lake update` (README step) was skipped per instructions; justified in §4.3.
