"""R3 · Validation with Patito: a row that breaks a rule is kept aside with its reason, never
dropped in silence, and what is left is validated by a model that states the same rules.

The two lines of defence are on purpose: `split` decides, the models check that it did.
"""

from datetime import date, datetime
from typing import Literal

import patito as pt
import polars as pl

#: Plausible ranges per test, in the units clean.labs leaves (glucose mmol/L, HbA1c %, creatinine mg/dL).
RANGES = {"glucose": (2, 30), "hba1c": (3, 20), "creatinine": (0.1, 15)}

IN_RANGE = pl.lit(True)  # TODO R3: true when the value is within RANGES for its test

#: A rule is the reason (Catalan, as INFORME.md will quote it) and an expression true for a bad row.
PATIENT_RULES: dict[str, pl.Expr] = {
    # TODO R3: "reason": expression true for a bad row
}
VISIT_RULES: dict[str, pl.Expr] = {
    # TODO R3
}
LAB_RULES: dict[str, pl.Expr] = {
    # TODO R3
}


def split(df: pl.DataFrame, rules: dict[str, pl.Expr]) -> tuple[pl.DataFrame, pl.DataFrame]:
    """(kept, rejected). rejected has every column of df plus `reason`, the names of every rule
    the row broke joined by "; ". A rule that evaluates to null does not reject the row."""
    raise NotImplementedError("R3")


class Patient(pt.Model):
    """A patient as clean.patients leaves them, after split(PATIENT_RULES)."""

    pass  # TODO R3: one annotated field per column, with its Field(...) rules


class Visit(pt.Model):
    """A visit as clean.visits leaves it, after split(VISIT_RULES)."""

    pass  # TODO R3: one annotated field per column, with its Field(...) rules


class Lab(pt.Model):
    """A result as clean.labs leaves it, after split(LAB_RULES)."""

    pass  # TODO R3: one annotated field per column, with its Field(...) rules
