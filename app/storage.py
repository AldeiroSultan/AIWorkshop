import json
from pathlib import Path

from app.models import Opportunity
from app.sample_data import make_sample_opportunities

DATA_FILE = Path(__file__).parent.parent / "data" / "opportunities.json"


def load_opportunities(path: Path = DATA_FILE) -> list[Opportunity]:
    """Load all opportunities from the JSON file.

    If the file doesn't exist yet, it is created with sample data.
    """
    if not path.exists():
        save_opportunities(make_sample_opportunities(), path)

    with open(path, encoding="utf-8") as file:
        rows = json.load(file)
    return [Opportunity(**row) for row in rows]


def save_opportunities(opportunities: list[Opportunity], path: Path = DATA_FILE) -> None:
    """Save all opportunities to the JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [opportunity.model_dump(mode="json") for opportunity in opportunities]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)
