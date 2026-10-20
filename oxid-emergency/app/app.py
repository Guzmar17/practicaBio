"""R9 · The page: four charts of the half year, from the server's routes.

Only this folder goes to the browser. It never imports emergency/ or server.py: what the page
knows arrives through /api, already aggregated and anonymised.
"""

import json

from oxid import Loading, Resource, Signal, h, mount
from oxid.chart import X, Y, chart
from oxid.runtime import window

WARDS = ["URG", "MI", "CAR", "PED", "TRA"]


async def load(path):
    response = await window.fetch("/api" + path)
    return json.loads(await response.text())


ward = Signal("URG")
picked = Signal(None)


def visits_by_ward(wards):
    """Bars: visits per ward, from /api/wards. Marks expected: 5, one per ward."""
    return h.p("TODO R9: visites per unitat")


def choose(name):
    def handler(ev):
        ward.set(name)

    return handler


def pressed(name):
    def value():
        return "true" if ward() == name else "false"

    return value


def week_title():
    return f"Visites per setmana · {ward()}"


def visits_by_week(weekly):
    """A line: the chosen ward's visits per week, from /api/weekly. Marks expected: one line, 25 weeks."""
    return h.p("TODO R9: visites per setmana de la unitat triada")


def scatter(points):
    """Points: hba1c against glucose from /api/points, with a brush. Marks expected: one per row."""
    return h.p("TODO R9: dispersió HbA1c–glucosa amb brush")


def selected():
    return "TODO R9: quantes visites hi ha dins el requadre"


def summary_line(stats):
    s = stats()
    g = s["glucose"]
    return (
        f"Glucosa: n = {g['n']}, mitjana {g['mean']}, mediana {g['median']} mmol/L, "
        f"{g['outliers']} valors per sobre de {g['high']}. "
        f"r(HbA1c, glucosa) = {s['correlation']['r']} (n = {s['correlation']['n']}). "
        f"Publicació amb k = {s['k']}; {s['suppressed']} persones suprimides."
    )


def hole(view, resource):
    """A hole that redraws when the resource arrives or changes: `view(resource)` is read inside it."""

    def draw():
        return view(resource)

    return draw


def page():
    # Made here, in the component, not at import: a Resource starts loading when it is created.
    wards = Resource(lambda: load("/wards"))
    weekly = Resource(lambda name: load("/weekly?ward=" + name), source=ward)
    points = Resource(lambda: load("/points"))
    stats = Resource(lambda: load("/statistic"))
    return h.main(
        h.h1("Urgències de l'Hospital de Vallnova · gener–juny 2026"),
        h.p("Dades inventades. Cap persona d'aquestes dades existeix.", class_="note"),
        Loading(h.p("Carregant…"), h.p(hole(summary_line, stats), class_="note")),
        h.h2("Unitats"),
        Loading(h.p("Carregant…"), h.div(hole(visits_by_ward, wards))),
        h.h2("Setmana a setmana"),
        h.nav(
            *[
                h.button(name, class_="ward-" + name, on_click=choose(name), aria_pressed=pressed(name))
                for name in WARDS
            ]
        ),
        Loading(h.p("Carregant…"), h.div(hole(visits_by_week, weekly))),
        h.h2("Glucosa"),
        h.img(src="/api/glucose.svg", alt="Histograma de la glucosa a l'arribada, en trams d'1 mmol/L"),
        h.h2("HbA1c i glucosa"),
        Loading(h.p("Carregant…"), h.div(hole(scatter, points))),
        h.p(selected),
    )


mount(page, "#app")
