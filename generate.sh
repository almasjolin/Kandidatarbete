#!/bin/bash

# List of Python scripts and their labels
declare -A script_labels=(
    ["testgenerator.py"]="test"
)

# Number of times each script should run
N=1

# Seed for reproducible random numbers
SEED=6215

# Function to generate a deterministic random filename
generate_seeded_name() {
    local label=$1
    local index=$2
    local seed=$SEED
    # Use awk to generate a deterministic random number based on the seed and index
    local random_part=$2
    echo "${label}_${random_part}"
}

# Iterate over each Python script
for script in "${!script_labels[@]}"; do
    label=${script_labels[$script]}
    echo "Running $script ($label) $N times starting with seed $SEED..."
    current_seed=$((SEED + N))
    random_name=$(generate_seeded_name "$label" "$N").txt
    python "utils/$script" --seed "$current_seed" > "tests/$random_name"
    echo "Output saved to tests/$random_name with seed $current_seed"
done

echo "All scripts executed."
