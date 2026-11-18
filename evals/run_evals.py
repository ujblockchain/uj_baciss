"""Score triage and routing on the labelled reports.

uv run python -m evals.run_evals                  run and upload to LangSmith
uv run python -m evals.run_evals --local          run without uploading
Options: --limit N (quick try), --refresh (re-upload the labels),
         --save-baseline (accept these scores as the baseline).
"""

import argparse
import json
import sys
from datetime import UTC, datetime
from uuid import uuid4

from langsmith import Client, evaluate
from langsmith.schemas import Example

from community_voice.agents.routing import route
from community_voice.agents.triage import triage
from community_voice.core.config import PROJECT_ROOT, get_settings
from community_voice.core.tracing import load_env
from community_voice.schemas.report import ReportIn
from evals import scoring

LABELS = PROJECT_ROOT / "data" / "evals" / "labelled_reports.json"
BASELINE = PROJECT_ROOT / "evals" / "baseline.json"
DATASET = "community-voice-triage-routing"


def load_examples() -> list[dict]:
    """The labelled reports as LangSmith examples."""
    examples = []
    for item in json.loads(LABELS.read_text(encoding="utf-8")):
        examples.append(
            {
                "inputs": {"id": item["id"], "text": item["text"]},
                "outputs": {
                    "language": item["language"],
                    "category": item["expected_category"],
                    "urgency": item["expected_urgency"],
                    "municipality": item["expected_municipality"],
                    "department": item["expected_department"],
                    "needs_human": item["expected_municipality"] == "unknown",
                },
            }
        )
    return examples


def target(inputs: dict) -> dict:
    """The part of the app being scored: triage, then routing."""
    triaged = triage(ReportIn(text=inputs["text"]))
    routed = route(triaged)
    return {
        "language": triaged.language.value,
        "category": triaged.category.value,
        "urgency": triaged.urgency.value,
        "municipality": routed.municipality,
        "department": routed.department,
        "needs_human": routed.needs_human,
    }


def upload(client: Client, examples: list[dict], refresh: bool) -> None:
    if refresh and client.has_dataset(dataset_name=DATASET):
        client.delete_dataset(dataset_name=DATASET)
    if not client.has_dataset(dataset_name=DATASET):
        dataset = client.create_dataset(DATASET, description="Fictional SA reports")
        client.create_examples(dataset_id=dataset.id, examples=examples)


def local_examples(examples: list[dict]) -> list[Example]:
    return [
        Example(
            id=uuid4(),
            dataset_id=uuid4(),
            created_at=datetime.now(UTC),
            inputs=item["inputs"],
            outputs=item["outputs"],
        )
        for item in examples
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--save-baseline", action="store_true")
    args = parser.parse_args()

    load_env()
    examples = load_examples()
    client = None
    if args.local:
        data = local_examples(examples[: args.limit])
    else:
        client = Client()
        upload(client, examples, args.refresh)
        data = list(client.list_examples(dataset_name=DATASET, limit=args.limit))

    settings = get_settings()
    results = evaluate(
        target,
        data=data,
        evaluators=scoring.EVALUATORS,
        experiment_prefix="triage-routing",
        metadata={
            "triage_model": settings.gemini_model,
            "routing_model": settings.groq_model,
        },
        client=client,
        upload_results=not args.local,
    )
    rows = list(results)
    scores = scoring.summarize(rows)

    print(f"\nScored {len(rows)} of {len(data)} reports")
    for key, value in scores.items():
        print(f"  {key:20} {value:.2f}")
    for row in rows:
        got, expected = row["run"].outputs, row["example"].outputs
        for result in row["evaluation_results"]["results"]:
            if result.score == 0:
                print(
                    f"  missed {row['example'].inputs['id']} {result.key}: "
                    f"got {got[result.key]!r}, expected {expected[result.key]!r}"
                )

    if args.save_baseline:
        BASELINE.write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
        print(f"Baseline saved to {BASELINE.relative_to(PROJECT_ROOT)}")
    elif args.limit:
        print("Quick try: no baseline check.")
    elif not BASELINE.exists():
        print("No baseline yet. Run again with --save-baseline.")
    elif problems := scoring.regressions(scores, json.loads(BASELINE.read_text())):
        print("REGRESSION:\n  " + "\n  ".join(problems))
        sys.exit(1)
    else:
        print("No regression against the baseline.")


if __name__ == "__main__":
    main()
