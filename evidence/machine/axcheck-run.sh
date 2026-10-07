#!/bin/bash
# Independent post-hoc axiom / definition check. Loads oleans built inside Comparator's sandbox,
# so the lean process itself runs inside landrun (read-only FS except /dev, no network), AF_UNIX restricted.
set -u
OUT=/home/mathaudit/audit/out
cd /home/mathaudit/audit/math/lean
export LEAN_PATH=$(lake env printenv LEAN_PATH 2>/dev/null)
PFX=$(lean --print-prefix)
rm -f $OUT/axcheck-exitcodes.txt
for f in AxMahler AxPolar DefsMahler DefsPolar; do
  restrict-af-unix landrun --best-effort --ro / --rw /dev -ldd -add-exec --env PATH --env HOME --env LEAN_PATH --rox "$PFX" -- \
    "$PFX/bin/lean" /home/mathaudit/audit/axcheck/$f.lean > $OUT/axcheck-$f.out 2>&1
  echo "$f exit=$?" | tee -a $OUT/axcheck-exitcodes.txt
done
