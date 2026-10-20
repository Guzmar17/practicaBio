"""R5 · Aggregations: one row per group, the group's size beside every figure, and the groups
that had no rows still shown.
"""

from datetime import datetime

import polars as pl

#: The half year the data covers: Monday 5 January to Sunday 28 June 2026, 25 weeks.
FIRST_WEEK = datetime(2026, 1, 5)
LAST_WEEK = datetime(2026, 6, 22)


def by_ward(episodes: pl.DataFrame) -> pl.DataFrame:
    """One row per ward, sorted by ward: ward, ward_name, visits, patients (distinct nhc),
    stay_mean and stay_median (hours, one decimal, finished stays only) and severe — the share
    of triaged visits that were orange or red, null for a ward that does no triage."""
    raise NotImplementedError("R5")


def weekly(episodes: pl.DataFrame) -> pl.DataFrame:
    """Visits per ward and week (week: the Monday, Datetime), every ward × every one of the 25
    weeks, a week with no visits as 0 — never a missing row. Sorted by ward, week."""
    raise NotImplementedError("R5")


def repeat_patients(episodes: pl.DataFrame) -> pl.DataFrame:
    """Patients with two or more glucose results: nhc, results, first and last glucose (by
    admission time, from the same rows — never min/max of separate columns) and change =
    last − first. Sorted by change, highest first, then nhc."""
    raise NotImplementedError("R5")


def above_ward(episodes: pl.DataFrame) -> pl.DataFrame:
    """Every episode with a glucose, plus ward_mean (that ward's mean glucose, `over`) and
    above = glucose − ward_mean, one decimal. Same rows as the input's measured ones."""
    raise NotImplementedError("R5")
