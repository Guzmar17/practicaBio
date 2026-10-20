"""R8 · The server answers aggregates and anonymous points, and never an identifier."""

import pytest
from oxid_server.testing import Client

from emergency import privacy

ROUTES = ["/api/wards", "/api/weekly?ward=URG", "/api/weekly?ward=PED", "/api/statistic", "/api/points"]


@pytest.fixture(scope="module")
def client():
    import server  # here, not at the top: until R1–R7 work it cannot import, and R8 fails alone

    with Client(server.app) as c:
        yield c


def test_every_route_answers(client):
    for route in ROUTES + ["/api/glucose.svg"]:
        assert client.get(route).status == 200, route


def test_weekly(client):
    rows = client.get("/api/weekly?ward=PED").json()
    assert len(rows) == 25 and rows[0] == {"week": "2026-01-05", "visits": rows[0]["visits"]}
    assert client.get("/api/weekly?ward=XYZ").status == 404


def test_points_send_what_the_chart_draws(client):
    points = client.get("/api/points").json()
    assert set(points[0]) == {"hba1c", "glucose"}
    assert len(points) == 435


def test_the_svg_is_drawn_on_the_server(client):
    answer = client.get("/api/glucose.svg")
    assert answer.header("content-type").startswith("image/svg+xml")
    assert answer.text().startswith("<svg")


def test_statistic(client):
    body = client.get("/api/statistic").json()
    assert body["glucose"]["n"] == 948 and body["k"] >= 5


def test_no_route_answers_an_identifier(client, episodes):
    nhcs = set(episodes["nhc"])
    surnames = set(episodes["surnames"])
    pseudonyms = set(privacy.generalise(episodes, privacy.key())["patient"])
    for route in ROUTES:
        text = client.get(route).text()
        leaked = [v for v in nhcs | surnames | pseudonyms if v in text]
        assert not leaked, f"{route} answers {leaked[:3]}"
