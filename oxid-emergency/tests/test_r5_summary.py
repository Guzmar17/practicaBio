"""R5 · Aggregations: group sizes beside the figures, and the week that had no visits."""

from datetime import datetime

import polars as pl

from emergency import summary


def test_by_ward(episodes):
    wards = summary.by_ward(episodes)
    assert wards["ward"].to_list() == ["CAR", "MI", "PED", "TRA", "URG"]
    assert wards["visits"].sum() == episodes.height
    urg = wards.filter(pl.col("ward") == "URG").row(0, named=True)
    assert (urg["visits"], urg["patients"], urg["stay_median"], urg["severe"]) == (1053, 587, 5.0, 0.259)
    assert wards.filter(pl.col("ward") != "URG")["severe"].null_count() == 4
    assert (wards["stay_mean"] > wards["stay_median"]).all(), "stays are skewed: the mean is above the median"


def test_weekly_has_every_week(episodes):
    weekly = summary.weekly(episodes)
    assert weekly.height == 5 * 25
    assert weekly["visits"].sum() == episodes.height
    easter = weekly.filter((pl.col("ward") == "PED") & (pl.col("week") == datetime(2026, 3, 30)))
    assert easter["visits"].to_list() == [0], "a week with no visits is a 0, not a missing row"


def test_first_and_last_come_from_real_rows(episodes):
    repeat = summary.repeat_patients(episodes)
    assert repeat.height == 243
    top = repeat.row(0, named=True)
    rows = episodes.filter((pl.col("nhc") == top["nhc"]) & pl.col("glucose").is_not_null()).sort("admitted_at")
    assert (top["first"], top["last"]) == (rows["glucose"][0], rows["glucose"][-1])
    assert repeat["change"].is_sorted(descending=True)


def test_above_ward_is_relative_to_its_own_ward(episodes):
    above = summary.above_ward(episodes)
    assert above.height == 948
    means = above.group_by("ward").agg(pl.col("above").mean())
    assert means["above"].abs().max() < 0.1
