"""R6 · Statistics: a handful of numbers that describe the glucose, and n beside every one."""

import polars as pl


def describe(values: pl.Series) -> dict[str, float | int]:
    """n (non-null), missing, mean, median, std (sample), q1, q3 (linear), iqr, low and high
    (the 1.5·IQR fences) and outliers (how many values fall outside them). Floats to 2 decimals."""
    raise NotImplementedError("R6")


def outliers(episodes: pl.DataFrame) -> pl.DataFrame:
    """The episodes whose glucose is above the high fence, highest first: visit_id, ward, triage,
    glucose, hba1c. An outlier is not an error: the high ones are mostly diabetic patients."""
    raise NotImplementedError("R6")


def correlation(episodes: pl.DataFrame) -> dict[str, float | int]:
    """Pearson's r between hba1c and glucose over the visits that measured both, and that n."""
    raise NotImplementedError("R6")
