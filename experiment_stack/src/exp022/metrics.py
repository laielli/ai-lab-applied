"""Metrics computation for EXP-022: YouCook2 Density Analysis.

Implements recipe-based relevance density computation where a query is
relevant to a video if they share the same recipe_type ID.

Key formula:
    d_tripartite = |relevant_pairs| / (|Q| x |V|)

where relevant(q, v) = (recipe_type(q) == recipe_type(v))
"""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .data import YouCook2Data

logger = logging.getLogger(__name__)


@dataclass
class DensityResult:
    """Container for density computation results."""

    d_tripartite: float
    num_queries: int
    num_videos: int
    num_relevant_pairs: int
    avg_videos_per_query: float
    avg_queries_per_video: float

    def to_dict(self) -> dict:
        return {
            "d_tripartite": self.d_tripartite,
            "num_queries": self.num_queries,
            "num_videos": self.num_videos,
            "num_relevant_pairs": self.num_relevant_pairs,
            "avg_videos_per_query": self.avg_videos_per_query,
            "avg_queries_per_video": self.avg_queries_per_video,
        }


@dataclass
class RecipeDistribution:
    """Statistics about recipe distribution."""

    num_recipes: int
    videos_per_recipe: dict[str, int]
    mean_videos_per_recipe: float
    std_videos_per_recipe: float
    min_videos_per_recipe: int
    max_videos_per_recipe: int

    # Segment statistics
    segments_per_recipe: dict[str, int]
    mean_segments_per_recipe: float

    def to_dict(self) -> dict:
        return {
            "num_recipes": self.num_recipes,
            "mean_videos_per_recipe": self.mean_videos_per_recipe,
            "std_videos_per_recipe": self.std_videos_per_recipe,
            "min_videos_per_recipe": self.min_videos_per_recipe,
            "max_videos_per_recipe": self.max_videos_per_recipe,
            "mean_segments_per_recipe": self.mean_segments_per_recipe,
            "videos_per_recipe": self.videos_per_recipe,
            "segments_per_recipe": self.segments_per_recipe,
        }


@dataclass
class PerRecipeDensity:
    """Per-recipe density breakdown."""

    recipe_densities: dict[str, float]
    mean_density: float
    std_density: float
    min_density: float
    max_density: float

    # Top/bottom recipes by density
    top_recipes: list[tuple[str, float]]  # [(recipe_id, density), ...]
    bottom_recipes: list[tuple[str, float]]

    def to_dict(self) -> dict:
        return {
            "mean_density": self.mean_density,
            "std_density": self.std_density,
            "min_density": self.min_density,
            "max_density": self.max_density,
            "top_recipes": self.top_recipes,
            "bottom_recipes": self.bottom_recipes,
            "recipe_densities": self.recipe_densities,
        }


def compute_d_tripartite_recipe_based(
    data: YouCook2Data,
    level: str = "segment",
) -> DensityResult:
    """Compute d_tripartite using recipe-based relevance.

    Relevance rule: A query is relevant to a video if they share
    the same recipe_type ID.

    Args:
        data: YouCook2Data container
        level: Granularity level - "segment" (individual captions) or
               "video" (aggregate all captions per video)

    Returns:
        DensityResult with d_tripartite and supporting metrics
    """
    if level == "segment":
        return _compute_segment_level_density(data)
    elif level == "video":
        return _compute_video_level_density(data)
    else:
        raise ValueError(f"Unknown level: {level}. Use 'segment' or 'video'.")


def _compute_segment_level_density(data: YouCook2Data) -> DensityResult:
    """Compute density at segment level.

    Each segment caption is a query, each video is a candidate.
    A (segment, video) pair is relevant if they share recipe_type.
    """
    num_queries = data.num_segments  # Each segment is a query
    num_videos = data.num_videos

    # Count relevant pairs
    # For each segment, count how many videos share its recipe_type
    videos_per_query = []
    queries_per_video = {vid: 0 for vid in data.unique_videos}

    num_relevant_pairs = 0

    for seg_idx, recipe_type in enumerate(data.recipe_types):
        # Videos relevant to this segment's query
        relevant_videos = data.videos_by_recipe[recipe_type]
        num_relevant = len(relevant_videos)

        videos_per_query.append(num_relevant)
        num_relevant_pairs += num_relevant

        # Update queries per video
        for vid in relevant_videos:
            queries_per_video[vid] += 1

    # Compute d_tripartite
    total_pairs = num_queries * num_videos
    d_tripartite = num_relevant_pairs / total_pairs if total_pairs > 0 else 0.0

    # Average statistics
    avg_videos_per_query = np.mean(videos_per_query) if videos_per_query else 0.0
    avg_queries_per_video = np.mean(list(queries_per_video.values()))

    logger.info(
        f"Segment-level density: d={d_tripartite:.6f}, "
        f"relevant_pairs={num_relevant_pairs}, "
        f"avg_videos_per_query={avg_videos_per_query:.2f}"
    )

    return DensityResult(
        d_tripartite=d_tripartite,
        num_queries=num_queries,
        num_videos=num_videos,
        num_relevant_pairs=num_relevant_pairs,
        avg_videos_per_query=avg_videos_per_query,
        avg_queries_per_video=avg_queries_per_video,
    )


def _compute_video_level_density(data: YouCook2Data) -> DensityResult:
    """Compute density at video level.

    Each video is both a query (using all its captions) and a candidate.
    A (video_q, video_v) pair is relevant if they share recipe_type.
    """
    num_queries = data.num_videos  # Each video is a query
    num_videos = data.num_videos

    # Count relevant pairs
    # For each video, count how many other videos share its recipe_type
    videos_per_query = []
    queries_per_video = {vid: 0 for vid in data.unique_videos}

    num_relevant_pairs = 0

    for video_id in data.unique_videos:
        recipe_type = data.recipe_by_video[video_id]
        relevant_videos = data.videos_by_recipe[recipe_type]
        num_relevant = len(relevant_videos)  # Includes self

        videos_per_query.append(num_relevant)
        num_relevant_pairs += num_relevant

        # Update queries per video
        for vid in relevant_videos:
            queries_per_video[vid] += 1

    # Compute d_tripartite
    total_pairs = num_queries * num_videos
    d_tripartite = num_relevant_pairs / total_pairs if total_pairs > 0 else 0.0

    # Average statistics
    avg_videos_per_query = np.mean(videos_per_query) if videos_per_query else 0.0
    avg_queries_per_video = np.mean(list(queries_per_video.values()))

    logger.info(
        f"Video-level density: d={d_tripartite:.6f}, "
        f"relevant_pairs={num_relevant_pairs}, "
        f"avg_videos_per_query={avg_videos_per_query:.2f}"
    )

    return DensityResult(
        d_tripartite=d_tripartite,
        num_queries=num_queries,
        num_videos=num_videos,
        num_relevant_pairs=num_relevant_pairs,
        avg_videos_per_query=avg_videos_per_query,
        avg_queries_per_video=avg_queries_per_video,
    )


def compute_recipe_distribution(data: YouCook2Data) -> RecipeDistribution:
    """Compute statistics about recipe distribution.

    Args:
        data: YouCook2Data container

    Returns:
        RecipeDistribution with per-recipe video/segment counts
    """
    # Videos per recipe
    videos_per_recipe = {
        recipe: len(videos)
        for recipe, videos in data.videos_by_recipe.items()
    }

    # Segments per recipe (sum of segments across all videos in recipe)
    segments_per_recipe = {}
    for recipe, videos in data.videos_by_recipe.items():
        total_segments = sum(
            len(data.segments_by_video.get(vid, []))
            for vid in videos
        )
        segments_per_recipe[recipe] = total_segments

    video_counts = list(videos_per_recipe.values())
    segment_counts = list(segments_per_recipe.values())

    return RecipeDistribution(
        num_recipes=data.num_recipes,
        videos_per_recipe=videos_per_recipe,
        mean_videos_per_recipe=float(np.mean(video_counts)),
        std_videos_per_recipe=float(np.std(video_counts)),
        min_videos_per_recipe=int(np.min(video_counts)),
        max_videos_per_recipe=int(np.max(video_counts)),
        segments_per_recipe=segments_per_recipe,
        mean_segments_per_recipe=float(np.mean(segment_counts)),
    )


def compute_per_recipe_density(
    data: YouCook2Data,
    distribution: RecipeDistribution,
    top_k: int = 5,
) -> PerRecipeDensity:
    """Compute per-recipe density contribution.

    For each recipe, compute its contribution to overall density:
    d_recipe = |videos_in_recipe|^2 / (|V| x |V|)

    This shows which recipes contribute most to density.

    Args:
        data: YouCook2Data container
        distribution: Pre-computed recipe distribution
        top_k: Number of top/bottom recipes to report

    Returns:
        PerRecipeDensity with per-recipe density values
    """
    num_videos = data.num_videos
    total_pairs = num_videos * num_videos

    recipe_densities = {}

    for recipe, num_recipe_videos in distribution.videos_per_recipe.items():
        # Each video in recipe is relevant to all other videos in recipe
        # This creates num_recipe_videos^2 relevant pairs
        relevant_pairs = num_recipe_videos * num_recipe_videos
        d_recipe = relevant_pairs / total_pairs if total_pairs > 0 else 0.0
        recipe_densities[recipe] = d_recipe

    densities = list(recipe_densities.values())

    # Sort by density for top/bottom
    sorted_recipes = sorted(recipe_densities.items(), key=lambda x: x[1], reverse=True)
    top_recipes = sorted_recipes[:top_k]
    bottom_recipes = sorted_recipes[-top_k:]

    return PerRecipeDensity(
        recipe_densities=recipe_densities,
        mean_density=float(np.mean(densities)),
        std_density=float(np.std(densities)),
        min_density=float(np.min(densities)),
        max_density=float(np.max(densities)),
        top_recipes=top_recipes,
        bottom_recipes=bottom_recipes,
    )


def compute_expected_density(num_recipes: int, num_videos: int) -> float:
    """Compute expected density under uniform recipe distribution.

    If videos were uniformly distributed across recipes:
    - Each recipe has num_videos / num_recipes videos
    - Each video is relevant to all videos in its recipe
    - Expected d = 1 / num_recipes

    Args:
        num_recipes: Number of recipe categories
        num_videos: Total number of videos

    Returns:
        Expected d_tripartite under uniform distribution
    """
    if num_recipes == 0:
        return 0.0
    return 1.0 / num_recipes
