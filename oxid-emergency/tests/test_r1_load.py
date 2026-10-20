"""R1 · Loading: the files read typed, nothing lost, codes kept as text."""

import polars as pl

from emergency import load


def test_patients_keep_their_codes_as_text():
    patients = load.patients()
    assert patients.shape == (800, 8)
    assert patients.columns == ["nhc", "name", "surnames", "born", "sex", "postcode", "height", "weight"]
    assert patients.schema["nhc"] == pl.String and patients.schema["postcode"] == pl.String
    assert patients["nhc"].str.starts_with("0").sum() == 113, "an nhc read as a number loses its leading zeros"
    assert patients["postcode"].str.starts_with("08").all()
    assert patients["weight"].null_count() == 30, '"n/a" is a missing weight'


def test_visits_have_datetimes():
    visits = load.visits()
    assert visits.height == 2089
    assert visits.schema["visit_id"] == pl.UInt32
    assert visits.schema["admitted_at"] == pl.Datetime("us")
    assert visits["discharged_at"].null_count() == 8, "a visit with no discharge is still in"


def test_labs_values_are_numbers_and_missing_is_null():
    labs = load.labs()
    assert labs.height == 2956
    assert labs.schema["value"] == pl.Float64
    assert labs.schema["test"] == load.TEST
    assert labs["value"].null_count() == 39, '"NA" and "" are both missing'


def test_wards_as_the_file_has_them():
    wards = load.wards()
    assert wards.height == 6, "loading fixes nothing: the duplicated ward is still there"
    assert wards.schema["floor"] == pl.UInt8
