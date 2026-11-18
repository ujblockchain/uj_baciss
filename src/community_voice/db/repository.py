"""Reports and reviews in SQLite (plain sqlite3, no ORM)."""

import sqlite3
from contextlib import closing
from datetime import UTC, datetime

from community_voice.core.config import DB_PATH
from community_voice.schemas.review import ReportRecord, ReviewDecision
from community_voice.schemas.user import StoredUser, User

# Statuses that still wait for a reviewer ("approved" waits for the draft decision).
PENDING = ("ready_for_review", "fast_track", "duplicate", "needs_human", "approved")

SCHEMA = """
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    status TEXT NOT NULL,
    category TEXT NOT NULL,
    urgency TEXT NOT NULL,
    municipality TEXT NOT NULL,
    department TEXT NOT NULL,
    duplicate_of TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT NOT NULL,
    action TEXT NOT NULL,
    category TEXT,
    urgency TEXT,
    department TEXT,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS report_owners (
    report_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS drafts (
    report_id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def save_report(
    report_id: str,
    text: str,
    status: str,
    category: str,
    urgency: str,
    municipality: str,
    department: str,
    duplicate_of: str | None = None,
) -> None:
    """Insert a report, or update it if the id exists."""
    now = _now()
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            INSERT INTO reports (id, text, status, category, urgency, municipality,
                                 department, duplicate_of, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status, category = excluded.category,
                urgency = excluded.urgency, municipality = excluded.municipality,
                department = excluded.department, duplicate_of = excluded.duplicate_of,
                updated_at = excluded.updated_at
            """,
            (
                report_id,
                text,
                status,
                category,
                urgency,
                municipality,
                department,
                duplicate_of,
                now,
                now,
            ),
        )


def get_report(report_id: str) -> ReportRecord | None:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT * FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
    return ReportRecord(**dict(row)) if row else None


def list_pending() -> list[ReportRecord]:
    """Reports waiting for review, most urgent first."""
    marks = ", ".join("?" * len(PENDING))
    query = f"""
        SELECT * FROM reports WHERE status IN ({marks})
        ORDER BY CASE urgency WHEN 'critical' THEN 0 WHEN 'high' THEN 1
                              WHEN 'medium' THEN 2 ELSE 3 END, created_at
    """
    with closing(_connect()) as connection:
        rows = connection.execute(query, PENDING).fetchall()
    return [ReportRecord(**dict(row)) for row in rows]


def list_reports() -> list[ReportRecord]:
    """Every report, newest first."""
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT * FROM reports ORDER BY created_at DESC"
        ).fetchall()
    return [ReportRecord(**dict(row)) for row in rows]


def save_review(report_id: str, decision: ReviewDecision, status: str) -> None:
    """Record a review and apply its corrections to the report."""
    now = _now()
    category = decision.category.value if decision.category else None
    urgency = decision.urgency.value if decision.urgency else None
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            INSERT INTO reviews (report_id, action, category, urgency, department,
                                 note, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_id,
                decision.action,
                category,
                urgency,
                decision.department,
                decision.note,
                now,
            ),
        )
        connection.execute(
            """
            UPDATE reports SET status = ?, updated_at = ?,
                category = COALESCE(?, category), urgency = COALESCE(?, urgency),
                department = COALESCE(?, department)
            WHERE id = ?
            """,
            (status, now, category, urgency, decision.department, report_id),
        )


def list_reviews(report_id: str) -> list[dict]:
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT * FROM reviews WHERE report_id = ? ORDER BY id", (report_id,)
        ).fetchall()
    return [dict(row) for row in rows]


def save_draft(report_id: str, body: str) -> None:
    """Save a drafted reply as pending."""
    now = _now()
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            INSERT INTO drafts (report_id, body, status, created_at, updated_at)
            VALUES (?, ?, 'pending', ?, ?)
            ON CONFLICT(report_id) DO UPDATE SET
                body = excluded.body, status = 'pending',
                updated_at = excluded.updated_at
            """,
            (report_id, body, now, now),
        )


def get_draft(report_id: str) -> dict | None:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT * FROM drafts WHERE report_id = ?", (report_id,)
        ).fetchone()
    return dict(row) if row else None


def finish_draft(report_id: str, body: str, status: str) -> None:
    """Record the final draft and set the report's final status."""
    now = _now()
    with closing(_connect()) as connection, connection:
        connection.execute(
            "UPDATE drafts SET body = ?, status = ?, updated_at = ? "
            "WHERE report_id = ?",
            (body, status, now, report_id),
        )
        connection.execute(
            "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, report_id),
        )


def create_user(email: str, name: str, password_hash: str, role: str) -> None:
    with closing(_connect()) as connection, connection:
        connection.execute(
            "INSERT INTO users (email, name, password_hash, role, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (email.lower(), name, password_hash, role, _now()),
        )


def find_user(email: str) -> StoredUser | None:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower(),)
        ).fetchone()
    return StoredUser(**dict(row)) if row else None


def get_user(user_id: int) -> User | None:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT id, email, name, role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return User(**dict(row)) if row else None


def set_owner(report_id: str, user_id: int) -> None:
    with closing(_connect()) as connection, connection:
        connection.execute(
            "INSERT OR REPLACE INTO report_owners (report_id, user_id) VALUES (?, ?)",
            (report_id, user_id),
        )


def get_owner(report_id: str) -> int | None:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT user_id FROM report_owners WHERE report_id = ?", (report_id,)
        ).fetchone()
    return row["user_id"] if row else None


def list_reports_of(user_id: int) -> list[ReportRecord]:
    """A citizen's own reports (those already saved), newest first."""
    with closing(_connect()) as connection:
        rows = connection.execute(
            """
            SELECT reports.* FROM reports
            JOIN report_owners ON report_owners.report_id = reports.id
            WHERE report_owners.user_id = ? ORDER BY reports.created_at DESC
            """,
            (user_id,),
        ).fetchall()
    return [ReportRecord(**dict(row)) for row in rows]


def reset_database() -> None:
    """Delete all reports, reviews and drafts."""
    with closing(_connect()) as connection, connection:
        connection.execute("DELETE FROM drafts")
        connection.execute("DELETE FROM reviews")
        connection.execute("DELETE FROM reports")
        connection.execute("DELETE FROM report_owners")
