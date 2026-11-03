"""Fictional sample data. All names are made up."""

from datetime import date

from app.models import Opportunity

SAMPLE_ROWS = [
    {
        "name": "Student Innovation Fund",
        "organization": "Campus Innovation Office",
        "link": "https://example.org/innovation-fund",
        "amount": 5000,
        "deadline": date(2026, 11, 3),
        "status": "Preparing",
        "owner": "Alex",
        "next_step": "Finish project proposal",
    },
    {
        "name": "Campus Startup Competition",
        "organization": "Student Entrepreneurship Club",
        "link": "https://example.org/startup-competition",
        "amount": 10000,
        "deadline": date(2026, 11, 6),
        "status": "Interested",
        "owner": "Maya",
        "next_step": "Check eligibility",
    },
    {
        "name": "Green Tech Challenge",
        "organization": "Northgate Climate Fund",
        "link": None,
        "amount": 2500,
        "deadline": date(2026, 11, 9),
        "status": "Preparing",
        "owner": "Jordan",
        "next_step": "Record the 2-minute pitch video",
    },
    {
        "name": "Local Company Sponsorship",
        "organization": "Harbour Software Ltd.",
        "link": None,
        "amount": None,
        "deadline": date(2026, 11, 2),
        "status": "Submitted",
        "owner": "Sam",
        "next_step": "Wait for their reply",
    },
    {
        "name": "Hackathon Prize",
        "organization": "Campus Coding Society",
        "link": None,
        "amount": 1000,
        "deadline": date(2026, 11, 5),
        "status": "Successful",
        "owner": "Sam",
        "next_step": "Send a thank-you email",
    },
    {
        "name": "Downtown Pitch Night",
        "organization": "Westside Business Association",
        "link": None,
        "amount": 1500,
        "deadline": date(2026, 11, 7),
        "status": "Submitted",
        "owner": "Jordan",
        "next_step": "Practise the pitch",
    },
    {
        "name": "Community Impact Grant",
        "organization": "Riverbend Community Foundation",
        "link": None,
        "amount": 3000,
        "deadline": date(2026, 11, 1),
        "status": "Interested",
        "owner": "Alex",
        "next_step": "Ask if late applications are accepted",
    },
    {
        "name": "Spring Incubator Cohort",
        "organization": "Lakeside Startup Hub",
        "link": "https://example.org/incubator",
        "amount": None,
        "deadline": date(2026, 11, 23),
        "status": "Interested",
        "owner": "Maya",
        "next_step": "Read the program guide",
    },
    {
        "name": "Regional Pitch Competition",
        "organization": "Valley Founders Network",
        "link": None,
        "amount": 2000,
        "deadline": date(2026, 10, 24),
        "status": "Unsuccessful",
        "owner": "Jordan",
        "next_step": "Ask the judges for feedback",
    },
]


def make_sample_opportunities() -> list[Opportunity]:
    """Build the sample opportunities."""
    opportunities = []
    for number, row in enumerate(SAMPLE_ROWS, start=1):
        opportunities.append(Opportunity(id=number, **row))
    return opportunities
