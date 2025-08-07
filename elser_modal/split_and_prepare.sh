#!/bin/bash

# Name of the file to split
FILE="elser_model_2.pt"

# Size per part in MB (Outlook safe size)
PART_SIZE_MB=10

# Convert MB to bytes for `split`
PART_SIZE_BYTES=$((PART_SIZE_MB * 1024 * 1024))

# Split the file
echo "Splitting $FILE into $PART_SIZE_MB MB parts..."
split -b $PART_SIZE_BYTES "$FILE" "${FILE}.part_"

# Rename each part to .dat for email safety
for f in ${FILE}.part_*
do
    mv "$f" "${f}.dat"
done

echo "✅ Done. You can now email these .dat files."

