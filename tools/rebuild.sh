#!/bin/sh
# Rebuild every node file from the run data, in order, then the derived outputs.
#   sh tools/rebuild.sh
# merge_run rewrites the node files of its run; retarget re-points edges at
# retired ids and must come after every merge.
set -e
cd "$(dirname "$0")/.."
for r in pilot/run pilot/run/prek pilot/run/fixes pilot/run/p1; do
  if [ -f "$r/critic/_mapping.json" ] && ls "$r"/critic/verdicts-*.json >/dev/null 2>&1; then
    python3 tools/merge_run.py "$r" > /dev/null
    echo "merged $r"
  fi
done
if [ -f pilot/run/p1/retarget/out.json ]; then
  python3 tools/retarget.py apply pilot/run/p1
fi
python3 tools/check.py | sed -n '1,14p'
