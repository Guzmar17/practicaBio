"""R1 · Loading: each file read once, typed, and renamed to English. Nothing is fixed here.

The four files come from three systems (data/README.md). Loading answers "what does the file
say?"; cleaning (clean.py) answers "what did they mean?". Keep the two apart: a test can then
check that the load lost nothing.
"""

from pathlib import Path

import polars as pl

DATA = Path(__file__).resolve().parent.parent / "data"

#: Manchester triage, least to most urgent: an Enum sorts and compares in this order.
TRIAGE = pl.Enum(["blue", "green", "yellow", "orange", "red"])
SEX = pl.Enum(["D", "H"])
TEST = pl.Enum(["glucose", "hba1c", "creatinine"])


def patients(path: Path = DATA / "patients.csv") -> pl.DataFrame:
    """The admissions export: `;`, decimal comma, dd/mm/yyyy, Catalan headers.

    Columns: nhc, name, surnames, born, sex, postcode, height, weight — all String except
    none: an nhc and a postcode are codes, never numbers ("08001" is not 8001).
    """
    frame = pl.read_csv(path, separator=";", infer_schema_length=0, null_values=["NA"])
    aliases = {
        "NHC": "nhc", "Nom": "name", "Nombre": "name",
        "Cognoms": "surnames", "Apellidos": "surnames",
        "Data de naixement": "born", "Data_naixement": "born",
        "Fecha de nacimiento": "born", "Naixement": "born",
        "Sexe": "sex", "Sexo": "sex", "Codi postal": "postcode",
        "Codi_postal": "postcode", "Código postal": "postcode", "CP": "postcode",
        "Alçada": "height", "Altura": "height", "Pes": "weight", "Peso": "weight",
    }
    frame = frame.rename({c: aliases[c] for c in frame.columns if c in aliases})
    born = pl.coalesce(
        pl.col("born").str.strptime(pl.Date, "%d/%m/%Y", strict=False),
        pl.col("born").str.strptime(pl.Date, "%Y-%m-%d", strict=False),
    )
    return frame.with_columns(
        born.alias("born"),
        pl.col("sex").cast(SEX, strict=False),
        pl.col("height").str.replace_all(",", ".").cast(pl.Float64, strict=False),
        pl.col("weight").str.replace_all(",", ".").cast(pl.Float64, strict=False),
    )


def visits(path: Path = DATA / "visits.csv") -> pl.DataFrame:
    """The emergency system's visits. visit_id UInt32, nhc String, ward String,
    admitted_at and discharged_at Datetime (discharged_at null: still in), triage String."""
    frame = pl.read_csv(path, infer_schema_length=0, null_values=["NA", ""])
    aliases = {
        "id_visita": "visit_id", "id visita": "visit_id", "nhc": "nhc",
        "llit": "ward", "ingressat": "admitted_at", "data_ingres": "admitted_at",
        "alta": "discharged_at", "data_alta": "discharged_at", "triage": "triage",
        "triaje": "triage",
    }
    frame = frame.rename({c: aliases[c] for c in frame.columns if c in aliases})
    def datetime(column: str) -> pl.Expr:
        return pl.coalesce(
            pl.col(column).str.strptime(pl.Datetime, "%d/%m/%Y %H:%M", strict=False),
            pl.col(column).str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False),
            pl.col(column).str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S", strict=False),
        )
    return frame.with_columns(
        pl.col("visit_id").cast(pl.UInt32, strict=False),
        datetime("admitted_at"), datetime("discharged_at"),
    )


def labs(path: Path = DATA / "labs.csv") -> pl.DataFrame:
    """The laboratory's results. visit_id UInt32, test Enum TEST, value Float64 (null when
    the lab wrote nothing or NA), unit String, taken_at Datetime."""
    frame = pl.read_csv(path, infer_schema_length=0, null_values=["NA", ""])
    aliases = {
        "id_visita": "visit_id", "prova": "test", "valor": "value",
        "unitat": "unit", "data_hora": "taken_at", "pres_at": "taken_at",
    }
    frame = frame.rename({c: aliases[c] for c in frame.columns if c in aliases})
    taken = pl.coalesce(
        pl.col("taken_at").str.strptime(pl.Datetime, "%d/%m/%Y %H:%M", strict=False),
        pl.col("taken_at").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False),
        pl.col("taken_at").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S", strict=False),
    )
    return frame.with_columns(
        pl.col("visit_id").cast(pl.UInt32, strict=False),
        pl.col("test").cast(TEST, strict=False),
        pl.col("value").str.replace_all(",", ".").cast(pl.Float64, strict=False),
        taken.alias("taken_at"),
    )


def wards(path: Path = DATA / "wards.csv") -> pl.DataFrame:
    """The hospital's ward list: code, name, floor (UInt8). As the file has it."""
    frame = pl.read_csv(path, infer_schema_length=0)
    aliases = {"codi": "code", "nom": "name", "planta": "floor"}
    frame = frame.rename({c: aliases[c] for c in frame.columns if c in aliases})
    return frame.with_columns(pl.col("floor").cast(pl.UInt8, strict=False))
