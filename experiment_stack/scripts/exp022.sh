#!/bin/bash
# EXP-022: YouCook2 Density Analysis
# Part A: Ground-truth density with recipe-based relevance (CPU-only)
#
# Usage:
#   ./experiment_stack/scripts/exp022.sh
#   ./experiment_stack/scripts/exp022.sh --sample-size 100  # Quick test
#
# Expected runtime: <5 minutes on CPU (val split ~3K segments)
# Output: experiment_stack/results/exp022_results.json

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
EXPERIMENT_DIR="$REPO_ROOT/experiment_stack"
OUTPUT_DIR="$EXPERIMENT_DIR/results"
CONFIG_PATH="$EXPERIMENT_DIR/src/exp022/config.yaml"

# Default arguments
SPLIT="val"
SAMPLE_SIZE=""
SEED=42

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --split)
            SPLIT="$2"
            shift 2
            ;;
        --sample-size)
            SAMPLE_SIZE="$2"
            shift 2
            ;;
        --seed)
            SEED="$2"
            shift 2
            ;;
        --config)
            CONFIG_PATH="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Log experiment start
echo "=================================================="
echo "EXP-022: YouCook2 Density Analysis"
echo "=================================================="
echo "Start time: $(date -Iseconds)"
echo "Git commit: $(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
echo ""
echo "Configuration:"
echo "  Split: $SPLIT"
echo "  Sample size: ${SAMPLE_SIZE:-full}"
echo "  Seed: $SEED"
echo "  Output dir: $OUTPUT_DIR"
echo ""

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Build command
CMD="python -m exp022.run"
CMD+=" --split $SPLIT"
CMD+=" --output-dir $OUTPUT_DIR"
CMD+=" --seed $SEED"

if [[ -n "$SAMPLE_SIZE" ]]; then
    CMD+=" --sample-size $SAMPLE_SIZE"
fi

if [[ -f "$CONFIG_PATH" ]]; then
    CMD+=" --config $CONFIG_PATH"
fi

# Run from experiment source directory
cd "$EXPERIMENT_DIR/src"

echo "Running: $CMD"
echo ""

# Execute
$CMD

# Log completion
echo ""
echo "=================================================="
echo "EXP-022 Complete"
echo "End time: $(date -Iseconds)"
echo "Results: $OUTPUT_DIR/exp022_results.json"
echo "=================================================="
