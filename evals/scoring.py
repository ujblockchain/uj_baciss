"""Scores for the labelled reports. Plain functions: no AI, no network."""

from collections import defaultdict

LEVELS = ["low", "medium", "high", "critical"]
TOLERANCE = 0.10  # a score may fall this far below the baseline


def _score(key: str, passed: bool) -> dict:
    return {"key": key, "score": float(passed)}


def language(outputs: dict, reference_outputs: dict) -> dict:
    return _score("language", outputs["language"] == reference_outputs["language"])


def category(outputs: dict, reference_outputs: dict) -> dict:
    return _score("category", outputs["category"] == reference_outputs["category"])


def urgency(outputs: dict, reference_outputs: dict) -> dict:
    return _score("urgency", outputs["urgency"] == reference_outputs["urgency"])


def urgency_within_one(outputs: dict, reference_outputs: dict) -> dict:
    gap = abs(
        LEVELS.index(outputs["urgency"]) - LEVELS.index(reference_outputs["urgency"])
    )
    return _score("urgency_within_one", gap <= 1)


def critical_safe(outputs: dict, reference_outputs: dict) -> dict:
    """A critical report must never be rated below high. Others are not scored."""
    if reference_outputs["urgency"] != "critical":
        return {"results": []}
    return _score("critical_safe", outputs["urgency"] in ("high", "critical"))


def municipality(outputs: dict, reference_outputs: dict) -> dict:
    same = outputs["municipality"] == reference_outputs["municipality"]
    return _score("municipality", same)


def department(outputs: dict, reference_outputs: dict) -> dict:
    """The expected name must appear in the answer (the agent may add words).

    Not scored when the area is unknown (there is no right department).
    """
    expected = reference_outputs["department"]
    if expected is None:
        return {"results": []}
    return _score("department", expected.lower() in outputs["department"].lower())


def needs_human(outputs: dict, reference_outputs: dict) -> dict:
    """Ask a human exactly when the area is unknown."""
    return _score(
        "needs_human", outputs["needs_human"] == reference_outputs["needs_human"]
    )


EVALUATORS = [
    language,
    category,
    urgency,
    urgency_within_one,
    critical_safe,
    municipality,
    department,
    needs_human,
]


def summarize(rows: list[dict]) -> dict[str, float]:
    """Mean score per metric over the rows of an experiment."""
    scores = defaultdict(list)
    for row in rows:
        for item in row["evaluation_results"]["results"]:
            scores[item.key].append(item.score)
    return {key: round(sum(v) / len(v), 3) for key, v in scores.items()}


def regressions(
    scores: dict[str, float], baseline: dict[str, float], tolerance: float = TOLERANCE
) -> list[str]:
    """Metrics that fell more than `tolerance` below the baseline."""
    return [
        f"{key}: {scores.get(key, 0.0):.2f} (baseline {value:.2f})"
        for key, value in baseline.items()
        if scores.get(key, 0.0) < value - tolerance
    ]
