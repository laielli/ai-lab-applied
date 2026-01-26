"""EXP-022: YouCook2 Density Analysis.

Measures d_tripartite on YouCook2 to test whether narrow-domain datasets
naturally exhibit higher density than general-purpose video datasets.

Key insight: YouCook2's recipe_type field creates natural many-to-many
relevance structure where queries are relevant to all videos of the same
recipe category.
"""

from .data import load_youcook2_dataset, validate_schema
from .metrics import (
    compute_d_tripartite_recipe_based,
    compute_recipe_distribution,
    compute_per_recipe_density,
)

__all__ = [
    "load_youcook2_dataset",
    "validate_schema",
    "compute_d_tripartite_recipe_based",
    "compute_recipe_distribution",
    "compute_per_recipe_density",
]
