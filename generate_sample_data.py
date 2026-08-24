"""
Generates a synthetic client events dataset shaped like the real caseload
data used in the employment outcomes dashboard. Nothing here is real -
it's just enough structure to load into Power BI and show the model working.

Run: python generate_sample_data.py
Output: sample_client_events.csv
"""

import random
from datetime import datetime, timedelta
import csv

random.seed(42)

SECTORS = [
    "Retail", "Hospitality", "Health & Social Care", "Construction",
    "Warehousing & Logistics", "Admin & Office", "Customer Service", "Education"
]

REFERRAL_SOURCES = ["Jobcentre Plus", "Self-referral", "Partner organisation", "Re-referral"]

STAGES = [
    "Engaged", "Action Plan Agreed", "In Training", "Job Ready",
    "Placed", "Sustained (13 weeks)", "Sustained (26 weeks)"
]

ADVISERS = ["Adviser A", "Adviser B", "Adviser C", "Adviser D"]

N_CLIENTS = 420
START_DATE = datetime(2024, 1, 1)


def random_date(start, max_days_forward):
    return start + timedelta(days=random.randint(0, max_days_forward))


def build_client_record(client_id):
    engagement_date = random_date(START_DATE, 540)
    sector = random.choice(SECTORS)
    referral = random.choices(REFERRAL_SOURCES, weights=[0.45, 0.2, 0.25, 0.1])[0]
    adviser = random.choice(ADVISERS)

    # weight outcomes so most clients progress partway, fewer reach full sustainment
    stage_weights = [0.10, 0.15, 0.15, 0.10, 0.25, 0.15, 0.10]
    current_stage = random.choices(STAGES, weights=stage_weights)[0]
    stage_index = STAGES.index(current_stage)

    placed_date = None
    if stage_index >= 4:  # reached "Placed" or beyond
        placed_date = engagement_date + timedelta(days=random.randint(30, 200))

    days_on_programme = (datetime(2026, 8, 24) - engagement_date).days

    return {
        "client_id": f"CL{client_id:04d}",
        "engagement_date": engagement_date.strftime("%Y-%m-%d"),
        "sector": sector,
        "referral_source": referral,
        "adviser": adviser,
        "current_stage": current_stage,
        "placed_date": placed_date.strftime("%Y-%m-%d") if placed_date else "",
        "days_on_programme": days_on_programme,
    }


def main():
    rows = [build_client_record(i) for i in range(1, N_CLIENTS + 1)]

    fieldnames = list(rows[0].keys())
    with open("sample_client_events.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    placed_count = sum(1 for r in rows if r["placed_date"])
    print(f"Generated {len(rows)} sample client records.")
    print(f"{placed_count} reached placement or beyond ({placed_count / len(rows):.0%}).")
    print("Saved to sample_client_events.csv")


if __name__ == "__main__":
    main()
