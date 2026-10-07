# Reproduce the recorded audit

[English](REPRODUCE.en.md) | [中文](REPRODUCE.zh-CN.md) · [Home](../README.md)

There are two distinct operations: inspecting this archive and running a new mathematical proof check. Do not describe the first as the second.

## A. Inspect the public archive

From the repository root:

```bash
python scripts/check_bundle.py
python -m unittest discover -s tests -v
```

These commands use only Python's standard library. They read checksums, preserved statements, logs, exit statuses and axiom records. They do not invoke Lean or an LLM. The checker returns a nonzero status for a missing/tampered required file, a failed recorded run, a disallowed recorded axiom or inconsistent configuration.

The manifest verifies the bytes published in this edition. It is not a signature from the original runtime. Changing both data and a checksum can forge an archive; independent execution remains the way to obtain a fresh proof-checking result.

## B. Prepare a new formal check

Use a disposable Linux environment and a non-root account. Keep personal tokens, SSH keys, production mounts and other projects out of reach. Read the pinned [Comparator README](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md) before executing any Solution code. The project's `lakefile.lean` and trusted Challenge imports also need review: Lake configuration can execute code.

The archived scripts in `evidence/machine/` document the historical machine. They contain its absolute paths and are **not** portable installers. Do not run them blindly. No fresh replay or installation is performed by this package.

### Recorded versions

| Component | Version / commit |
|---|---|
| openai/math | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| Lean | `leanprover/lean4:v4.34.1` |
| Lean build commit | `5045d0056413266e57c625dcd7c365b10e377c52` |
| Comparator | `d03acab154d269c06e60e4de7e4cc85deebff94b` |
| lean4export | `076e8e57707e813375e8f9da8bf989799ace9680` |
| landrun | `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` |

Comparator's toolchain pin was aligned from 4.34.0 to 4.34.1; the original one-line patch is [archived](../evidence/machine/tool-patch-comparator-toolchain.diff). Build Comparator and lean4export with the matching Lean version. Do not silently upgrade packages to their latest releases. Record any installation differences as a new environment variant. See [VERSIONS.txt](../evidence/machine/VERSIONS.txt) for complete historical details.

### Get the mathematical source

```bash
git clone https://github.com/openai/math.git math
cd math
git checkout --detach adc7f1241b42e322a6451854ab7e4b4c146bf78a
git rev-parse HEAD
git status --porcelain
```

Before the first Lake command, review the Challenge files, two JSON configurations, `lean/lean-toolchain`, `lean/lakefile.lean` and `lean/lake-manifest.json`. The audited target configurations have no definition holes and allow only `propext`, `Quot.sound`, `Classical.choice`.

Prepare dependencies in the isolated audit account. The historical run used `lake exe cache get` from `math/lean/`, accepted the official Mathlib cache, retained the pinned manifest and did **not** run `lake update`. It did not reuse any prebuilt OAI proof objects. This is documented in the [machine report](../evidence/machine/REPORT.md) and [pre-audit note](../evidence/machine/PREAUDIT.md).

A source-only rebuild is a different, useful variant. Record it separately; do not compare its timing directly to the cached run. Do not directly build or execute the untrusted Solution before the protected Comparator invocation.

### Invoke Comparator

Preconditions: the version-matched `lean`, `lake`, `comparator`, `lean4export`, and real `landrun` are on PATH; the trusted dependency setup is complete; a working systemd user manager is available. Use the official isolation launch, adapted only for the two fixed configuration names.

From `math/lean/`, the following is an example of preserving each process's actual exit status:

```bash
# Choose a new output directory outside the upstream source tree.
# The operator is responsible for the prepared environment and sandbox preconditions.
mkdir -p "$HOME/mahler-replay-results"
OUT="$HOME/mahler-replay-results"
set +e
for name in MahlerConjecture SymmetricPolar; do
    cfg="ComparatorChallenges/$name.json"
    date -Is > "$OUT/$name.started.txt"
    systemd-run --property=RestrictAddressFamilies=~AF_UNIX \
      --user --pty -E PATH="$PATH" --working-directory "$(pwd)" -- \
      bash -c "lake env comparator $cfg" \
      > "$OUT/$name.stdout.log" 2> "$OUT/$name.stderr.log"
    rc=$?
    printf '%s\n' "$rc" > "$OUT/$name.exitcode"
    date -Is > "$OUT/$name.finished.txt"
    printf '%s: process exit %s (inspect full logs)\n' "$name" "$rc"
done
```

This is documentation for an operator-prepared environment, not an unattended installer. If systemd, Landlock, the toolchain or resources are unavailable, report `ENVIRONMENT_BLOCKED` or `BUILD_FAILED`. Do not substitute fake-landrun or disable isolation to produce a reassuring success.

The historical machine used a custom AF_UNIX seccomp wrapper because it lacked systemd. That source and self-tests are archived, with explicit review limits. Reusing it requires its own security review; this package does not certify the wrapper as a complete sandbox.

### Interpret and preserve the result

A successful process must reach both the default-kernel acceptance and the final Comparator success, with actual exit code 0. Check the unchanged target configurations and mathematical meaning, then preserve the entire execution record: stdout/stderr, environment versions, source diff, dependency changes, allowed and actual axioms, times, resource data and checksums. Do not paste a success message into a replacement log.

For additional `#print axioms` or semantic tests that load built `.olean` files, use the protected environment as described by upstream. Do not run them unprotected after a supposedly isolated build.

Classify failures precisely. Download errors, OOMs or incompatible toolchains are not mathematical counterexamples. A rejected export or axiom mismatch invalidates that formal verification attempt, but does not automatically disprove the mathematical statement.

The two supplied configs disable nanoda. An external-kernel run requires a separately documented compatible checker and configuration; it must be reported separately rather than being retroactively attached to the recorded single-kernel result.
