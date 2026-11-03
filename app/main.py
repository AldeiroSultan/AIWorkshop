from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.dates import days_left
from app.storage import load_opportunities

STATIC_DIR = Path(__file__).parent.parent / "static"

app = FastAPI(title="Capstone Funding Tracker")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    """Serve the dashboard page."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/opportunities")
def list_opportunities():
    """List all opportunities, with days_left added to each one."""
    result = []
    for opportunity in load_opportunities():
        row = opportunity.model_dump(mode="json")
        row["days_left"] = days_left(opportunity.deadline)
        result.append(row)
    return result
