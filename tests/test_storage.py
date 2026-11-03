from datetime import date

from app.models import Opportunity, Status
from app.storage import load_opportunities, save_opportunities


def test_save_then_load_gives_the_same_data(tmp_path):
    path = tmp_path / "opportunities.json"
    opportunity = Opportunity(
        id=1,
        name="Test Grant",
        deadline=date(2026, 12, 1),
        status=Status.PREPARING,
        owner="Alex",
    )

    save_opportunities([opportunity], path)

    assert load_opportunities(path) == [opportunity]


def test_missing_file_is_created_with_sample_data(tmp_path):
    path = tmp_path / "opportunities.json"

    opportunities = load_opportunities(path)

    assert path.exists()
    assert len(opportunities) > 0
