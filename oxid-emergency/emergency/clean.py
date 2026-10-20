"""R2 · Cleaning with expressions: what each source meant, written as Polars expressions.

Every fix is a decision. Write the decision in a comment beside it, and its count in INFORME.md.
"""

import polars as pl

from .load import SEX, TRIAGE

#: mg/dL of glucose in one mmol/L (molar mass 180.16 g/mol).
GLUCOSE_MG_PER_MMOL = 18.016


def patients(raw: pl.DataFrame) -> pl.DataFrame:
    """sex → Enum SEX (" h" and "d" are H and D), born → Date, height → Float64 in cm
    (a height under 3 was written in metres), weight → Float64 in kg (decimal comma; 0 means
    unknown, so null). nhc, name, surnames and postcode stay String."""
    data = pl.read_csv(
       raw, 
         separator=";",
          decima_coman=True,
          try_parse_dates=True,
          dtypes={
                "nhc": pl.Utf8,
                "name": pl.Utf8,
                "surnames": pl.Utf8,
                "born": pl.Date,
                "sex": pl.Utf8,
                "postcode": pl.Utf8,
                "height": pl.Float64,
                "weight": pl.Float64,
          },
       


    )  # Assuming raw is a Path


    


    raise NotImplementedError("R2")


def visits(raw: pl.DataFrame) -> pl.DataFrame:
    """triage → Enum TRIAGE: spaces and capitals removed, "greeen" is green. Wards without
    triage keep null. Adds stay_hours: Float64, null while the patient is still in."""
       data = pl.read_csv(
        raw, 
        separator=";",
        decima_coman=True,
        try_parse_dates=True,
        dtypes={
            "visit_id": pl.UInt32,
            "nhc": pl.Utf8,
            "ward": pl.Utf8,
            "admitted_at": pl.Datetime,
            "discharged_at": pl.Datetime,
            "triage": pl.Utf8,
        },
       )

    raise NotImplementedError("R2")


def labs(raw: pl.DataFrame) -> pl.DataFrame:
    """Glucose always in mmol/L: cardiology's analyser writes mg/dL, so divide by
    GLUCOSE_MG_PER_MMOL and change the unit. Other tests unchanged."""
    data = pl.read_csv(
        raw,
        separator=";",
        decima_coman=True,
        try_parse_dates=True,
        dtypes={
            "visit_id": pl.UInt32,
            "test": pl.Utf8,
            "value": pl.Float64,
            "unit": pl.Utf8,
            "taken_at": pl.Datetime,
        },
    )
    raise NotImplementedError("R2")


def derive(episodes: pl.DataFrame) -> pl.DataFrame:
    """On the joined episodes (combine.episodes): age at admission in whole years (UInt8) and
    bmi = weight / height² in kg/m², one decimal, null when either is null."""
  
          data = pl.read_csv(
        episodes,
        separator=";",
        decima_coman=True,
        try_parse_dates=True,
        dtypes={
            "age": pl.UInt8,
            "bmi": pl.Float64,
        },
    )


    raise NotImplementedError("R2")
