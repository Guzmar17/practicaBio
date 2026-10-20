"""R3 · Validation: bad rows put aside with a reason, the rest checked by a Patito model."""

import patito as pt
import pytest

from emergency import clean, load, model


def test_rejected_with_their_reason(analysis):
    reasons = {name: frame.group_by("reason").len().rows() for name, frame in analysis.rejected.items()}
    assert reasons == {
        "patients": [("data de naixement sentinella", 3)],
        "visits": [("alta abans de l'ingrés", 2)],
        "labs": [("valor fora de rang", 2)],
    }


def test_split_keeps_every_row():
    visits = clean.visits(load.visits())
    kept, rejected = model.split(visits, model.VISIT_RULES)
    assert kept.height + rejected.height == visits.height
    assert kept.columns == visits.columns and "reason" in rejected.columns


def test_the_models_refuse_what_split_would_reject():
    with pytest.raises(pt.exceptions.DataFrameValidationError):
        model.Patient.validate(clean.patients(load.patients()))
    with pytest.raises(pt.exceptions.DataFrameValidationError):
        model.Visit.validate(clean.visits(load.visits()))
    with pytest.raises(pt.exceptions.DataFrameValidationError):
        model.Lab.validate(clean.labs(load.labs()))


def test_the_models_accept_what_split_kept():
    model.Patient.validate(model.split(clean.patients(load.patients()), model.PATIENT_RULES)[0])
    model.Visit.validate(model.split(clean.visits(load.visits()), model.VISIT_RULES)[0])
    model.Lab.validate(model.split(clean.labs(load.labs()), model.LAB_RULES)[0])
