#!/usr/bin/env python3
"""Main orchestrator for EXP-022: YouCook2 Density Analysis.

Part A: Ground-truth density analysis using recipe-based relevance (CPU-only).

Usage:
    python -m exp022.run --config config.yaml
    python -m exp022.run --split val --output-dir results
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from .data import load_youcook2_dataset, SchemaValidationError
from .metrics import (
    compute_d_tripartite_recipe_based,
    compute_recipe_distribution,
    compute_per_recipe_density,
    compute_expected_density,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_density_analysis(
    split: str = "val",
    sample_size: Optional[int] = None,
    output_dir: Path = Path("results"),
    seed: int = 42,
) -> dict:
    """Run Part A: Ground-truth density analysis for YouCook2.

    This is CPU-only - no embeddings required. Uses recipe_type field
    to determine query-video relevance.

    Args:
        split: Dataset split (val, test)
        sample_size: If set, use only this many segments
        output_dir: Directory for output files
        seed: Random seed

    Returns:
        Dict with all results
    """
    logger.info("=" * 60)
    logger.info("EXP-022: YouCook2 Density Analysis (Part A)")
    logger.info("=" * 60)

    start_time = time.time()

    results = {
        "experiment_id": "EXP-022",
        "description": "YouCook2 d_tripartite analysis with recipe-based relevance",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "split": split,
            "sample_size": sample_size,
            "seed": seed,
        },
    }

    # 1. Load and validate data
    logger.info("\n--- Step 1: Load and Validate Data ---")
    try:
        data = load_youcook2_dataset(
            split=split,
            sample_size=sample_size,
            seed=seed,
        )
    except SchemaValidationError as e:
        logger.error(f"Schema validation failed: {e}")
        results["error"] = str(e)
        results["status"] = "FAILED"
        _save_results(results, output_dir)
        return results
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        results["error"] = str(e)
        results["status"] = "FAILED"
        _save_results(results, output_dir)
        return results

    # Log actual counts
    results["data_summary"] = {
        "num_segments": data.num_segments,
        "num_videos": data.num_videos,
        "num_recipes": data.num_recipes,
        "avg_segments_per_video": data.num_segments / data.num_videos if data.num_videos > 0 else 0,
        "avg_videos_per_recipe": data.num_videos / data.num_recipes if data.num_recipes > 0 else 0,
    }

    # 2. Compute recipe distribution
    logger.info("\n--- Step 2: Recipe Distribution Analysis ---")
    distribution = compute_recipe_distribution(data)
    results["recipe_distribution"] = distribution.to_dict()

    logger.info(f"  Recipes: {distribution.num_recipes}")
    logger.info(f"  Videos per recipe: {distribution.mean_videos_per_recipe:.2f} +/- {distribution.std_videos_per_recipe:.2f}")
    logger.info(f"  Range: [{distribution.min_videos_per_recipe}, {distribution.max_videos_per_recipe}]")
    logger.info(f"  Segments per recipe: {distribution.mean_segments_per_recipe:.2f}")

    # 3. Compute d_tripartite at segment level
    logger.info("\n--- Step 3: Segment-Level Density ---")
    segment_density = compute_d_tripartite_recipe_based(data, level="segment")
    results["segment_level"] = segment_density.to_dict()

    logger.info(f"  d_tripartite: {segment_density.d_tripartite:.6f}")
    logger.info(f"  Relevant pairs: {segment_density.num_relevant_pairs:,}")
    logger.info(f"  Avg videos per query: {segment_density.avg_videos_per_query:.2f}")

    # 4. Compute d_tripartite at video level
    logger.info("\n--- Step 4: Video-Level Density ---")
    video_density = compute_d_tripartite_recipe_based(data, level="video")
    results["video_level"] = video_density.to_dict()

    logger.info(f"  d_tripartite: {video_density.d_tripartite:.6f}")
    logger.info(f"  Relevant pairs: {video_density.num_relevant_pairs:,}")
    logger.info(f"  Avg videos per query: {video_density.avg_videos_per_query:.2f}")

    # 5. Per-recipe density breakdown
    logger.info("\n--- Step 5: Per-Recipe Density ---")
    per_recipe = compute_per_recipe_density(data, distribution, top_k=5)
    results["per_recipe_density"] = per_recipe.to_dict()

    logger.info(f"  Mean per-recipe density: {per_recipe.mean_density:.6f}")
    logger.info(f"  Std: {per_recipe.std_density:.6f}")
    logger.info("  Top 5 high-density recipes:")
    for recipe, d in per_recipe.top_recipes:
        num_vids = distribution.videos_per_recipe[recipe]
        logger.info(f"    Recipe {recipe}: d={d:.6f} ({num_vids} videos)")

    # 6. Expected vs actual density
    logger.info("\n--- Step 6: Expected vs Actual ---")
    expected_d = compute_expected_density(data.num_recipes, data.num_videos)
    results["expected_density_uniform"] = expected_d
    results["density_ratio_vs_expected"] = video_density.d_tripartite / expected_d if expected_d > 0 else 0

    logger.info(f"  Expected (uniform): {expected_d:.6f}")
    logger.info(f"  Actual (video-level): {video_density.d_tripartite:.6f}")
    logger.info(f"  Ratio: {results['density_ratio_vs_expected']:.2f}x")

    # 7. Comparison with baselines
    logger.info("\n--- Step 7: Comparison with Baselines ---")
    baselines = {
        "MSR-VTT": 0.001,
        "ActivityNet": 0.0002,
    }
    results["baseline_comparison"] = {}

    for name, baseline_d in baselines.items():
        ratio = video_density.d_tripartite / baseline_d if baseline_d > 0 else 0
        results["baseline_comparison"][name] = {
            "baseline_d": baseline_d,
            "youcook2_d": video_density.d_tripartite,
            "ratio": ratio,
        }
        logger.info(f"  vs {name}: {ratio:.1f}x higher density")

    # 8. Determine success criteria
    logger.info("\n--- Step 8: Success Criteria Evaluation ---")
    d_video = video_density.d_tripartite

    if d_video > 0.05:
        decision = "GO"
        rationale = f"d={d_video:.4f} > 0.05: Significant density increase. Use YouCook2 as natural dense benchmark."
    elif d_video >= 0.01:
        decision = "PARTIAL"
        rationale = f"d={d_video:.4f} in [0.01, 0.05]: Moderate density. YouCook2 useful for analysis but may need augmentation."
    else:
        decision = "NO-GO"
        rationale = f"d={d_video:.4f} < 0.01: Minimal density. Recipe structure doesn't create sufficient density."

    results["decision"] = {
        "outcome": decision,
        "rationale": rationale,
        "thresholds": {
            "GO": "> 0.05",
            "PARTIAL": "[0.01, 0.05]",
            "NO-GO": "< 0.01",
        }
    }

    logger.info(f"  Decision: {decision}")
    logger.info(f"  {rationale}")

    # Timing
    elapsed = time.time() - start_time
    results["elapsed_seconds"] = elapsed
    results["status"] = "SUCCESS"

    logger.info(f"\nTotal time: {elapsed:.1f}s")

    # Save results
    _save_results(results, output_dir)

    return results


def _save_results(results: dict, output_dir: Path) -> Path:
    """Save results to JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "exp022_results.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Results saved to: {output_path}")
    return output_path


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="EXP-022: YouCook2 Density Analysis"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config YAML file",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="val",
        help="Dataset split (val, test)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Sample size for testing (None for full dataset)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Output directory for results",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )

    args = parser.parse_args()

    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)

    # Override with command line args
    split = args.split or config.get("split", "val")
    sample_size = args.sample_size or config.get("sample_size")
    output_dir = Path(args.output_dir or config.get("output_dir", "results"))
    seed = args.seed or config.get("seed", 42)

    results = run_density_analysis(
        split=split,
        sample_size=sample_size,
        output_dir=output_dir,
        seed=seed,
    )

    logger.info("\n" + "=" * 60)
    logger.info("EXP-022 Complete")
    logger.info("=" * 60)

    # Print summary
    if results.get("status") == "SUCCESS":
        logger.info(f"\nSUMMARY:")
        logger.info(f"  Video-level d_tripartite: {results['video_level']['d_tripartite']:.6f}")
        logger.info(f"  Segment-level d_tripartite: {results['segment_level']['d_tripartite']:.6f}")
        logger.info(f"  Decision: {results['decision']['outcome']}")

    return results


if __name__ == "__main__":
    main()
