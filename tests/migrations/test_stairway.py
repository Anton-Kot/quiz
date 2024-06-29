"""
Snippet from https://github.com/alvassin/backendschool2019/blob/master/tests/migrations/test_stairway.py
"""

import pytest


def test_stairway(alembic_runner, alembic_engine):
    """Stairway test for database migrations.

    This test upgrades to each migration individually, downgrades back, and then upgrades again
    to ensure that the migrations are reversible and consistent.
    """
    revisions = list(alembic_runner.history.revisions[:-1])

    for i, revision in enumerate(revisions[1:], 1):
        try:
            alembic_runner.migrate_up_to(revision, return_current=False)

            previous_revision = revisions[i - 1]
            alembic_runner.migrate_down_to(previous_revision, return_current=False)

            alembic_runner.migrate_up_to(revision, return_current=False)

        except Exception as e:
            pytest.fail(
                f"Failed during stairway test: upgrade -> downgrade -> upgrade cycle.\n"
                f"Failing Revision: {revision}\nAlembic Error: {str(e)}"
            )
