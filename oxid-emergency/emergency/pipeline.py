"""The whole analysis in order, once: load → clean → split and validate → join → derive.

Given complete. Read it to see which of your functions feeds which; run it with
`uv run python -m emergency.pipeline` to print the counts INFORME.md asks for.
"""

from dataclasses import dataclass, field

import polars as pl

from . import clean, combine, load, model, privacy, statistic, summary


@dataclass
class Analysis:
    episodes: pl.DataFrame
    rejected: dict[str, pl.DataFrame]
    lost: dict[str, int]
    counts: dict[str, int] = field(default_factory=dict)


def run() -> Analysis:
    raw = {"patients": load.patients(), "visits": load.visits(), "labs": load.labs()}
    patients, bad_patients = model.split(clean.patients(raw["patients"]), model.PATIENT_RULES)
    visits, bad_visits = model.split(clean.visits(raw["visits"]), model.VISIT_RULES)
    labs, bad_labs = model.split(clean.labs(raw["labs"]), model.LAB_RULES)
    model.Patient.validate(patients)
    model.Visit.validate(visits)
    model.Lab.validate(labs)

    wards = combine.unique_wards(load.wards())
    lost = combine.unmatched(visits, patients)
    episodes = clean.derive(combine.with_labs(combine.episodes(visits, patients, wards), labs))
    counts = {name: frame.height for name, frame in raw.items()} | {"episodes": episodes.height}
    rejected = {"patients": bad_patients, "visits": bad_visits, "labs": bad_labs}
    return Analysis(episodes, rejected, lost, counts)


def main() -> None:
    analysis = run()
    print("rows read:", analysis.counts)
    print("rejected:", {name: frame.height for name, frame in analysis.rejected.items()})
    for name, frame in analysis.rejected.items():
        if frame.height:
            print(f"  {name}:", frame.group_by("reason").len().sort("reason").rows())
    print("lost in the join:", analysis.lost)
    with pl.Config(tbl_rows=10, tbl_cols=-1, tbl_width_chars=140):
        print(summary.by_ward(analysis.episodes))
    print("glucose:", statistic.describe(analysis.episodes["glucose"]))
    print("hba1c ~ glucose:", statistic.correlation(analysis.episodes))
    try:
        release, suppressed = privacy.anonymise(analysis.episodes, privacy.key())
    except RuntimeError as error:
        print("release: skipped,", error)
    else:
        print(f"release: {release.height} rows, k = {privacy.k_anonymity(release)}, {suppressed} people suppressed")


if __name__ == "__main__":
    main()
