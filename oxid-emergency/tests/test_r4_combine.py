"""R4 · Joins: declared, counted, and refusing a duplicated key."""

import polars as pl
import pytest

from emergency import clean, combine, load, model


def kept(frame, rules):
    return model.split(frame, rules)[0]


@pytest.fixture(scope="module")
def sides():
    patients = kept(clean.patients(load.patients()), model.PATIENT_RULES)
    visits = kept(clean.visits(load.visits()), model.VISIT_RULES)
    return visits, patients


def test_a_duplicated_ward_is_refused_not_multiplied(sides):
    visits, patients = sides
    with pytest.raises(pl.exceptions.ComputeError):
        combine.episodes(visits, patients, load.wards())


def test_unique_wards():
    assert combine.unique_wards(load.wards())["code"].to_list() == ["URG", "MI", "CAR", "PED", "TRA"]
    assert combine.unique_wards(load.wards()).filter(pl.col("code") == "URG")["name"].item() == "Urgències"


def test_what_the_inner_join_loses(sides):
    visits, patients = sides
    assert combine.unmatched(visits, patients) == {"visits_without_patient": 22, "patients_without_visit": 0}


def test_episodes(episodes, sides):
    visits, _ = sides
    assert episodes.height == visits.height - 22 == 2065
    assert {"name", "postcode", "ward_name", "ward_floor", "glucose", "hba1c", "creatinine"} <= set(episodes.columns)
    assert episodes["ward_name"].null_count() == 0
    assert episodes["visit_id"].is_unique().all()
    assert episodes["glucose"].drop_nulls().len() == 948
