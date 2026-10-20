"""R4 · Joins: three systems become one table of episodes, and nothing is lost without a count.

A join is not a lookup. Every lookup here is declared `validate="m:1"`, so a duplicated key
raises instead of multiplying rows.
"""

import polars as pl


def unique_wards(wards: pl.DataFrame) -> pl.DataFrame:
    """One row per code. URG appears twice (the ward was renamed and the old row kept):
    keep the first, which is the name the hospital uses today."""
    raise NotImplementedError("R4")


def unmatched(visits: pl.DataFrame, patients: pl.DataFrame) -> dict[str, int]:
    """How many rows each side loses in an inner join on nhc:
    {"visits_without_patient": …, "patients_without_visit": …} — anti joins, both ways."""
    raise NotImplementedError("R4")


def episodes(visits: pl.DataFrame, patients: pl.DataFrame, wards: pl.DataFrame) -> pl.DataFrame:
    """One row per visit whose patient is known: the visit's columns, the patient's
    (name, surnames, born, sex, postcode, height, weight) and ward_name, ward_floor.
    The ward is joined on visits.ward = wards.code."""
    raise NotImplementedError("R4")


def with_labs(episodes: pl.DataFrame, labs: pl.DataFrame) -> pl.DataFrame:
    """Each episode with one column per test (glucose, hba1c, creatinine): that visit's
    value, null when it was not measured. A visit has at most one result per test."""
    raise NotImplementedError("R4")
