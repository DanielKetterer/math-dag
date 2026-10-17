#!/usr/bin/env sh
# Download the open Learning Commons Knowledge Graph export (about 950 MB total)
# into a scratch directory, then extract the math subset into the repo.
#   sh scripts/fetch_learning_commons.sh /path/to/scratch
set -eu
VERSION=v1.15.0
DEST=${1:?usage: fetch_learning_commons.sh <scratch_dir>}
mkdir -p "$DEST"
for f in nodes.jsonl relationships.jsonl; do
  curl -sSL "https://cdn.learningcommons.org/knowledge-graph/$VERSION/exports/$f?ref=docs_curl" -o "$DEST/$f"
done
python3 -I "$(dirname "$0")/extract_learning_commons.py" "$DEST" "$(dirname "$0")/../sources/learning-commons"
