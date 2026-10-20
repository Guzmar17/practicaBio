"""R8 · The server: the analysis runs once when a worker starts, and only aggregates and
anonymised points ever leave it. Not one route answers a name, an nhc or a pseudonym.

    uv run oxid serve app --server server.py        # while you work (OXID_SERVER_RUNTIME=cpython)
    uv run oxid build app --out www && uv run oxid-server server.py --runtime cpython
"""

import polars as pl
from oxid import render_to_string
from oxid.chart import X, Y, chart
from oxid_server import App, HTTPError, Response

from emergency import pipeline, privacy, statistic, summary

app = App(title="ecb-emergency", static="www")

#: The analysis, once per worker. A missing ECB_EMERGENCY_KEY stops the server here, on purpose.
ANALYSIS = pipeline.run()
RELEASE, SUPPRESSED = privacy.anonymise(ANALYSIS.episodes, privacy.key())
WARDS = summary.by_ward(ANALYSIS.episodes).drop("patients")
WEEKLY = summary.weekly(ANALYSIS.episodes).with_columns(pl.col("week").dt.strftime("%Y-%m-%d"))
GLUCOSE = None  # TODO R8: glucose buckets of 1 mmol/L: bucket, visits


@app.get("/api/wards")
async def wards():
    """One row per ward: visits, mean and median stay in hours, share of severe triage."""
    raise NotImplementedError("R8")


@app.get("/api/weekly")
async def weekly(ward: str = "URG"):
    """Visits per week in one ward, every week of the half year; 404 for a ward that does not exist."""
    raise NotImplementedError("R8")


@app.get("/api/statistic")
async def statistic_():
    """The glucose described (statistic.describe), the hba1c–glucose correlation, and the release's k and suppressed people."""
    raise NotImplementedError("R8")


@app.get("/api/points")
async def points():
    """hba1c and glucose of every released visit that measured both — the two columns the scatter draws, nothing else."""
    raise NotImplementedError("R8")


@app.get("/api/glucose.svg")
async def glucose_svg():
    """The glucose histogram, drawn here: an <img> needs no Python in the page."""
    raise NotImplementedError("R8")
