"""R6 · Statistics: n beside every number, fences that find real values."""

from emergency import statistic


def test_describe_glucose(episodes):
    assert statistic.describe(episodes["glucose"]) == {
        "n": 948,
        "missing": 1117,
        "mean": 6.59,
        "median": 6.3,
        "std": 1.84,
        "q1": 5.4,
        "q3": 7.4,
        "iqr": 2.0,
        "low": 2.4,
        "high": 10.4,
        "outliers": 46,
    }


def test_outliers_are_the_described_ones(episodes):
    high = statistic.outliers(episodes)
    assert high.height == 46
    assert high["glucose"].min() > 10.4
    assert high.columns == ["visit_id", "ward", "triage", "glucose", "hba1c"]


def test_correlation_says_its_n(episodes):
    assert statistic.correlation(episodes) == {"n": 542, "r": 0.77}
