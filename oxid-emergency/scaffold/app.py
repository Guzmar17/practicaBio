"""Development landing page used before the student completes the API requirements."""

from oxid import h, mount


def page():
    return h.main(
        h.h1("C044 A1 · Urgències de l'Hospital de Vallnova"),
        h.p("La bastida funciona. Les dades i els gràfics formen part de l'examen."),
        h.h2("Continua l'examen"),
        h.p("Implementa R1–R8 i comprova cada requisit amb `mk test`."),
        h.p("Quan l'API estigui completa, executa `mk dev --full` per obrir l'aplicació sencera."),
    )


mount(page, "#app")
