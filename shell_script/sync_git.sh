#!/bin/bash

DEST=$1

if [ -z "$DEST" ]; then
    echo "Usage: $0 <destination_path>"
    echo "Example: $0 ~/CO2_dft/"
    exit 1
fi

rsync -avR \
  --include='*/' \
  --include='INCAR' \
  --include='CONTCAR' \
  --include='OUTCAR' \
  --include='.jl' \
  --include='*.sh' \
  --include='*.py' \
  --include='README.md' \
  --exclude='*' \
  . "$DEST"

echo "------------------------------------------"
echo "Sync completed to: $DEST"
