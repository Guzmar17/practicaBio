"""R7 · Pseudonyms with a key, a release with k ≥ 5 counted in people."""

import os

import patito as pt
import polars as pl
import pytest

from emergency import privacy

IDENTIFIERS = {"nhc", "name", "surnames", "born", "postcode", "admitted_at", "discharged_at"}


def test_a_pseudonym_is_keyed_and_stable():
    a, b = privacy.pseudonym("04712344", b"k" * 32), privacy.pseudonym("04712344", b"k" * 32)
    assert a == b and len(a) == 12 and int(a, 16) >= 0
    assert privacy.pseudonym("04712344", b"j" * 32) != a, "another key, another pseudonym"
    assert privacy.pseudonym("04712345", b"k" * 32) != a


def test_no_key_no_pseudonyms(monkeypatch):
    monkeypatch.delenv(privacy.KEY_VARIABLE)
    with pytest.raises(RuntimeError, match=privacy.KEY_VARIABLE):  # say which variable is missing
        privacy.key()


def test_the_key_comes_from_the_environment():
    assert privacy.key() == bytes.fromhex(os.environ[privacy.KEY_VARIABLE])


def test_generalise_keeps_no_identifier(episodes):
    general = privacy.generalise(episodes, privacy.key())
    assert not IDENTIFIERS & set(general.columns)
    assert general.height == episodes.height
    assert general["zone"].str.contains(r"^\d{3}\*\*$").all()
    assert set(general["age_band"].unique()) <= {0, 20, 40, 60, 80}
    combinations = general.group_by("patient").agg(pl.struct(privacy.QUASI).n_unique().alias("n"))
    assert combinations["n"].max() == 1, "one person, one combination: a birthday must not split them"


def test_k_counts_people_not_rows():
    one_person_three_visits = pl.DataFrame(
        {"patient": ["a", "a", "a", "b"], "age_band": [20] * 4, "sex": ["D"] * 4, "zone": ["080**"] * 4}
    )
    assert privacy.k_anonymity(one_person_three_visits) == 2


def test_the_release(episodes):
    release, suppressed = privacy.anonymise(episodes, privacy.key())
    assert privacy.k_anonymity(release) >= privacy.K
    people = episodes["nhc"].n_unique()
    assert release["patient"].n_unique() + suppressed == people
    assert suppressed / people < 0.25


def test_the_release_model_refuses_an_identifier(episodes):
    release, _ = privacy.anonymise(episodes, privacy.key())
    with pytest.raises(pt.exceptions.DataFrameValidationError):
        privacy.Release.validate(release.with_columns(nhc=pl.lit("00000000")))
