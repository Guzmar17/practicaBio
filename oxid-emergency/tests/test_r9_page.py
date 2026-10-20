"""R9 · The page, mounted without a browser, its fetches answered by the real routes."""

import sys

import oxid.runtime
import pytest
from oxid.testing import App
from oxid_server.testing import Client

from conftest import ROOT

URLS = ["/api/wards", "/api/points", "/api/statistic"] + [
    f"/api/weekly?ward={w}" for w in ["URG", "MI", "CAR", "PED", "TRA"]
]


class Answer:
    def __init__(self, text):
        self._text = text

    async def text(self):
        return self._text


class Window:
    """window.fetch, answered from what server.py really answers."""

    def __init__(self, answers):
        self.answers = answers

    async def fetch(self, url):
        return Answer(self.answers[url])


@pytest.fixture
def page(monkeypatch):
    import server  # here, not at the top: until R1–R8 work it cannot import, and R9 fails alone

    with Client(server.app) as client:
        answers = {url: client.get(url).text() for url in URLS}
    monkeypatch.setattr(oxid.runtime, "window", Window(answers))
    monkeypatch.syspath_prepend(str(ROOT / "app"))
    sys.modules.pop("app", None)
    app = App.from_module("app")
    yield app
    app.dispose()


@pytest.mark.filterwarnings("ignore:zoom, brush")
def test_three_charts_and_the_summary(page):
    assert len(page.find_all("svg")) == 3
    assert "k = " in page.text and "n = 948" in page.text


@pytest.mark.filterwarnings("ignore:zoom, brush")
def test_a_ward_button_redraws_the_week(page):
    page.click("button.ward-PED")
    assert "Visites per setmana · PED" in page.text
    assert page.find("button.ward-PED").attrs["aria-pressed"] == "true"
