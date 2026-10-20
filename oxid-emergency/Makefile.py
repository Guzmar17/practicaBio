"""Tasks for the C044 A1 emergency-data practice.

The repository is a student scaffold: a fresh checkout builds the Oxid page, but
the acceptance tests remain red until the student completes R1–R9.

    mk sync       create .venv exactly from uv.lock
    mk test       run all acceptance tests, or selected pytest arguments
    mk lint       check Python style and the Oxid page
    mk check      the full local gate: lint, tests and a production page build
    mk build      build the Oxid page into www/
    mk dev        serve the unfinished frontend locally on port 8600
    mk dev --full serve it with server.py after completing R1–R8
"""

# /// script
# requires-python = ">=3.11"
# dependencies = ["mkrun>=0.4"]
# ///

from __future__ import annotations

from make import note, sh, task


@task(requires=["uv"])
def sync() -> None:
    """Create or refresh .venv from the committed lockfile."""
    sh("uv", "sync", "--frozen")


@task(requires=["uv"])
def test(*args: str) -> None:
    """Run the acceptance suite; extra arguments are passed to pytest.

    For example, ``mk test -- tests/test_r1_load.py -x`` works on R1 only.
    """
    sh("uv", "run", "--frozen", "pytest", *args)


@task(requires=["uv"])
def lint() -> None:
    """Check Python formatting, useful lint rules, and the Oxid page.

    F401 and PIE790 are excluded because the scaffold deliberately imports APIs
    and leaves model bodies ready for the student's later requirements.
    """
    sh("uv", "run", "--frozen", "ruff", "check", "--ignore", "F401,PIE790", ".")
    sh("uv", "run", "--frozen", "ruff", "format", "--check", ".")
    sh("uv", "run", "--frozen", "oxid", "check", "app/app.py")
    sh("uv", "run", "--frozen", "oxid", "check", "scaffold/app.py")


@task(requires=["uv"])
def build() -> None:
    """Build the production Oxid page into www/."""
    sh("uv", "run", "--frozen", "oxid", "build", "app", "--out", "www")


@task(needs=[lint, test, build])
def check() -> None:
    """Run the complete local gate used before submission."""
    note("format, lint, Oxid build and all acceptance tests passed")


@task(requires=["uv"])
def dev(port: int = 8600, *, full: bool = False) -> None:
    """Serve the frontend scaffold, optionally with its completed Python backend.

    The default deliberately does not import ``server.py``, so the page can run
    while R1–R8 still contain the student's placeholders. Use ``mk dev --full``
    once those requirements are complete; that mode also requires
    ECB_EMERGENCY_KEY in the environment.

    Args:
        full: load server.py and serve the API as well as the page
    """
    directory = "app" if full else "scaffold"
    backend = ["--server", "server.py"] if full else ["--no-server"]
    sh(
        "uv",
        "run",
        "--frozen",
        "oxid",
        "serve",
        directory,
        *backend,
        "--port",
        str(port),
        env={"OXID_SERVER_RUNTIME": "cpython"},
    )
