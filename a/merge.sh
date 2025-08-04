#!/bin/bash

# Define output file name
OUTPUT_FILE="elser_model_2.pt"

# Remove any existing output file to avoid appending accidentally
if [ -f "$OUTPUT_FILE" ]; then
  echo "Removing existing $OUTPUT_FILE to avoid duplication..."
  rm "$OUTPUT_FILE"
fi

# Find and concatenate all parts in sorted order
echo "Reassembling files into $OUTPUT_FILE..."
cat elser_model_2.pt.part_*.dat >> "$OUTPUT_FILE"

# Final check
echo "✅ Done. Reassembled file:"
ls -lh "$OUTPUT_FILE"
