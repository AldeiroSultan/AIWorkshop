# AGENTS.md

Rules for AI tools working in this repo.

## The project

A team dashboard for funding opportunities: grants, startup competitions, incubators and company sponsorships. All data is fictional.

## Run and test

- Install: `python -m pip install -r requirements.txt`
- Run: `python -m uvicorn app.main:app --reload`, then open http://localhost:8000
- Test: `python -m pytest`

## Files

- `app/main.py`: the server
- `app/dates.py`: `days_left()` counts the days until a deadline
- `static/deadlines.js` and `static/deadlines.css`: empty for now
- `TEAM_NOTES.md`: notes from the team
- `app/sample_data.py`: the example rows. The app copies them to `data/opportunities.json` on first run.

## Data

- Fields: `id`, `name`, `organization`, `link`, `amount`, `deadline`, `status`, `owner`, `next_step`
- Statuses: `Interested`, `Preparing`, `Submitted`, `Successful`, `Unsuccessful`
- The server adds `days_left` to every row: `0` on the deadline day, `1` the day before, `-1` the day after.

## Team rules (agreed with the client)

- Deadline labels go by `days_left` only, whatever the status.

## Rules

- Keep the code simple. A beginner must be able to read it.
- Don't add new libraries.
- Plain JavaScript only. No React, no build step.
- `days_left()` in `app/dates.py` is tested and correct. Always reuse it. Never count days another way.
- Don't change `app/dates.py` or `tests/test_dates.py`. Other team apps use them.
