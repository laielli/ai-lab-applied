"""Dataset loading utilities for EXP-022: YouCook2 Density Analysis.

Loads YouCook2 from HuggingFace and validates the required schema fields
for recipe-based relevance computation.
"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class YouCook2Data:
    """Container for loaded YouCook2 data with pre-computed groupings."""

    # Raw data
    segments: list[dict]

    # Identifiers
    video_ids: list[str]
    unique_videos: list[str]
    recipe_types: list[str]
    unique_recipes: list[str]
    captions: list[str]

    # Groupings
    videos_by_recipe: dict[str, list[str]]  # recipe_type -> [video_ids]
    recipe_by_video: dict[str, str]  # video_id -> recipe_type
    segments_by_video: dict[str, list[int]]  # video_id -> [segment indices]

    @property
    def num_segments(self) -> int:
        return len(self.segments)

    @property
    def num_videos(self) -> int:
        return len(self.unique_videos)

    @property
    def num_recipes(self) -> int:
        return len(self.unique_recipes)


class SchemaValidationError(Exception):
    """Raised when required fields are missing from dataset."""
    pass


def validate_schema(sample: dict) -> tuple[bool, list[str]]:
    """Validate that sample contains required fields for EXP-022.

    Required fields:
    - youtube_id: Video identifier
    - recipe_type: Recipe category ID for grouping
    - sentence: Caption/description text

    Args:
        sample: Single item from HuggingFace dataset

    Returns:
        Tuple of (is_valid, list of missing fields)
    """
    required_fields = ["youtube_id", "recipe_type", "sentence"]
    missing = [f for f in required_fields if f not in sample]
    return len(missing) == 0, missing


def load_youcook2_dataset(
    split: str = "val",
    sample_size: Optional[int] = None,
    seed: int = 42,
) -> YouCook2Data:
    """Load YouCook2 dataset from HuggingFace.

    Args:
        split: Dataset split (val, test)
        sample_size: If set, load only this many segments
        seed: Random seed for sampling

    Returns:
        YouCook2Data container with segments and pre-computed groupings

    Raises:
        SchemaValidationError: If required fields are missing
        ImportError: If datasets library is not installed
    """
    try:
        from datasets import load_dataset
    except ImportError:
        raise ImportError("datasets library required: pip install datasets")

    logger.info(f"Loading YouCook2 {split} split from HuggingFace...")

    # Load dataset
    dataset = load_dataset("lmms-lab/YouCook2", split=split)

    # Validate schema on first sample
    if len(dataset) == 0:
        raise ValueError(f"Empty dataset for split: {split}")

    sample = dataset[0]
    is_valid, missing = validate_schema(sample)
    if not is_valid:
        raise SchemaValidationError(
            f"YouCook2 dataset missing required fields: {missing}. "
            f"Available fields: {list(sample.keys())}"
        )

    logger.info(f"Schema validation passed. Available fields: {list(sample.keys())}")

    # Optionally sample
    if sample_size is not None and sample_size < len(dataset):
        logger.info(f"Sampling {sample_size} segments (seed={seed})")
        dataset = dataset.shuffle(seed=seed).select(range(sample_size))

    # Extract data
    segments = []
    video_ids = []
    recipe_types = []
    captions = []

    videos_by_recipe: dict[str, set[str]] = defaultdict(set)
    recipe_by_video: dict[str, str] = {}
    segments_by_video: dict[str, list[int]] = defaultdict(list)

    for idx, item in enumerate(dataset):
        video_id = str(item["youtube_id"])
        recipe_type = str(item["recipe_type"])
        caption = str(item["sentence"])

        segments.append(item)
        video_ids.append(video_id)
        recipe_types.append(recipe_type)
        captions.append(caption)

        # Build groupings
        videos_by_recipe[recipe_type].add(video_id)
        recipe_by_video[video_id] = recipe_type
        segments_by_video[video_id].append(idx)

    # Convert sets to sorted lists for determinism
    videos_by_recipe_list = {k: sorted(v) for k, v in videos_by_recipe.items()}

    unique_videos = sorted(set(video_ids))
    unique_recipes = sorted(set(recipe_types))

    logger.info(
        f"Loaded YouCook2: {len(segments)} segments, "
        f"{len(unique_videos)} videos, {len(unique_recipes)} recipes"
    )
    logger.info(
        f"  Average videos per recipe: {len(unique_videos) / len(unique_recipes):.2f}"
    )
    logger.info(
        f"  Average segments per video: {len(segments) / len(unique_videos):.2f}"
    )

    return YouCook2Data(
        segments=segments,
        video_ids=video_ids,
        unique_videos=unique_videos,
        recipe_types=recipe_types,
        unique_recipes=unique_recipes,
        captions=captions,
        videos_by_recipe=videos_by_recipe_list,
        recipe_by_video=recipe_by_video,
        segments_by_video=dict(segments_by_video),
    )
