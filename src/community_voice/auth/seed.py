"""Create the test accounts. Run: uv run python -m community_voice.auth.seed

These passwords are public (they are in the README). Use them for demos only.
"""

from community_voice.auth.security import hash_password
from community_voice.db.repository import create_user, find_user

TEST_ACCOUNTS = [
    ("admin@communityvoice.test", "Test Admin", "AdminPass123", "admin"),
    ("citizen1@communityvoice.test", "Test Citizen One", "Citizen1Pass123", "citizen"),
    ("citizen2@communityvoice.test", "Test Citizen Two", "Citizen2Pass123", "citizen"),
]


def seed() -> list[str]:
    """Add any missing test account. Returns the emails created."""
    created = []
    for email, name, password, role in TEST_ACCOUNTS:
        if find_user(email) is None:
            create_user(email, name, hash_password(password), role)
            created.append(email)
    return created


if __name__ == "__main__":
    created = seed()
    print("Created:", ", ".join(created) if created else "nothing (already there)")
