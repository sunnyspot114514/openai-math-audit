#!/bin/bash
# Usage: run_comparator.sh <name> <config-relative-to-lean/>
# Runs Comparator under the AF_UNIX-restricted launch (systemd-run RestrictAddressFamilies=~AF_UNIX equivalent).
set -u
name="$1"; cfg="$2"
OUT=/home/mathaudit/audit/out
cd /home/mathaudit/audit/math/lean || exit 99
CMD=(restrict-af-unix bash -c "lake env comparator $cfg")
{
  echo "date_start=$(date -Is)"
  echo "cwd=$(pwd)"
  echo "id=$(id)"
  echo "which: comparator=$(command -v comparator) lean4export=$(command -v lean4export) landrun=$(command -v landrun) restrict-af-unix=$(command -v restrict-af-unix) lake=$(command -v lake)"
  echo "--- env (scrubbed with env -i) ---"; env | sort
  echo "--- command ---"
  printf '/usr/bin/time -v -o %q' "$OUT/$name.time.txt"; printf ' %q' "${CMD[@]}"; echo " > $OUT/$name.stdout.log 2> $OUT/$name.stderr.log"
} > "$OUT/$name.cmd.txt"
# memory sampler
( while true; do echo "$(date -Is) $(grep -E 'MemAvailable' /proc/meminfo | tr -s ' ')"; sleep 30; done ) > "$OUT/$name.memsamples.txt" 2>&1 &
SAMPLER=$!
t0=$(date +%s.%N)
/usr/bin/time -v -o "$OUT/$name.time.txt" "${CMD[@]}" > "$OUT/$name.stdout.log" 2> "$OUT/$name.stderr.log"
rc=$?
t1=$(date +%s.%N)
kill $SAMPLER 2>/dev/null
echo "$rc" > "$OUT/$name.exitcode"
echo "wall_seconds=$(awk "BEGIN{printf \"%.1f\", $t1 - $t0}") date_end=$(date -Is) exit_code=$rc" >> "$OUT/$name.cmd.txt"
echo "done $name rc=$rc"
