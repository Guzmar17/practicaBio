"""R2 · Cleaning: each source's habits undone with expressions."""

import polars as pl

from emergency import clean, load


def test_patients_typed():
    patients = clean.patients(load.patients())
    assert patients.schema["sex"] == load.SEX
    assert patients["sex"].null_count() == 6, "an empty sex is unknown, not a third value"
    assert patients.schema["born"] == pl.Date
    assert patients.schema["height"] == pl.Float64 and patients.schema["weight"] == pl.Float64
    assert patients["height"].min() > 40, "1,72 was metres: 172 cm"
    assert patients["weight"].null_count() == 32, "n/a and 0 kg are both unknown"
    assert patients.filter(pl.col("nhc") == "74648253")["sex"].item() == "H", '"h" is H'


def test_triage_is_an_ordered_enum():
    visits = clean.visits(load.visits())
    assert visits.schema["triage"] == load.TRIAGE
    assert visits["triage"].drop_nulls().n_unique() == 5, "Green, greeen and ' yellow' are green and yellow"
    assert visits["triage"].null_count() == 1027, "only URG triages"
    assert visits.filter(pl.col("triage") >= "orange").height == 274
    assert visits["stay_hours"].null_count() == 8


def test_glucose_in_one_unit():
    labs = clean.labs(load.labs())
    glucose = labs.filter(pl.col("test") == "glucose")
    assert glucose["unit"].unique().to_list() == ["mmol/L"]
    assert glucose["value"].drop_nulls().quantile(0.99) < 15, "cardiology's mg/dL are mmol/L now"
    assert glucose["value"].max() == 680, "the missing decimal point is R3's to reject, not R2's to guess"
    assert labs.filter(pl.col("test") == "creatinine")["unit"].unique().to_list() == ["mg/dL"]


def test_age_and_bmi(episodes):
    assert episodes.schema["age"] == pl.UInt8
    assert episodes["age"].max() < 100
    assert episodes["bmi"].null_count() == episodes["weight"].null_count()
    one = episodes.filter(pl.col("visit_id") == 1).row(0, named=True)
    assert one["bmi"] == round(one["weight"] / (one["height"] / 100) ** 2, 1)
