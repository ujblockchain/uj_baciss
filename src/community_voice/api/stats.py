"""Numbers for the dashboard."""

from collections import Counter, defaultdict

from pydantic import BaseModel

from community_voice.db.repository import PENDING
from community_voice.schemas.review import ReportRecord


class Stats(BaseModel):
    total: int
    by_status: dict[str, int]
    by_category: dict[str, int]
    by_department: dict[str, int]
    by_urgency: dict[str, int]
    urgent: list[ReportRecord]  # critical or high, still waiting
    duplicate_clusters: dict[str, list[str]]  # original id -> duplicate ids


def build_stats(reports: list[ReportRecord]) -> Stats:
    clusters = defaultdict(list)
    for report in reports:
        if report.duplicate_of:
            clusters[report.duplicate_of].append(report.id)
    return Stats(
        total=len(reports),
        by_status=Counter(r.status for r in reports),
        by_category=Counter(r.category for r in reports),
        by_department=Counter(r.department for r in reports),
        by_urgency=Counter(r.urgency for r in reports),
        urgent=[
            r
            for r in reports
            if r.urgency in ("critical", "high") and r.status in PENDING
        ],
        duplicate_clusters=dict(clusters),
    )
