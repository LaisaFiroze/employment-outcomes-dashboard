# Employment Outcomes Dashboard

Power BI dashboard tracking placement trends and KPIs across an active caseload of 100+ clients on a government-contracted employment programme.

## Background

Managing a large caseload manually in spreadsheets made it hard to spot which sectors, referral routes, and intervention types were actually driving placements. This dashboard pulls that together in one place so I can review progress weekly instead of rebuilding pivot tables every time.

## What it does

- Tracks client progression through the programme stages, from initial engagement to sustained employment
- Breaks down placement outcomes by sector, referral source, and time on programme
- Flags clients who are falling behind expected milestones so I can prioritise outreach
- Refreshes automatically so the numbers are current without manual re-exports

## Tools used

- Power BI (data model, visuals, report design)
- DAX (KPI measures, time intelligence)
- Power Query (data cleaning and transformation)
- Automated refresh scheduling

## Approach

Raw case management exports arrive messy: inconsistent date formats, duplicate client records from re-referrals, free-text outcome fields. Power Query handles the cleanup and shaping. The data model is a simple star schema (fact table of client events, dimension tables for sector, adviser, and time) which keeps the DAX manageable and the report responsive.

Sample data in this repo is synthetic and was generated to mirror the shape of the real dataset without containing any real client information.

## Files in this repo

- `power_query_transform.pq` — the M code used to clean and reshape the raw export
- `dax_measures.txt` — the core DAX measures behind the KPI cards
- `generate_sample_data.py` — generates a GDPR-safe sample dataset in the same structure as the real one, so you can see the model working end to end
- `sample_client_events.csv` — output of the generator, ready to load into Power BI

## Screenshot

![Dashboard screenshot](images/dashboard_screenshot.png)

## Note on data

All data in this repository is synthetic and generated for demonstration purposes. No real participant, client, or caseload data is included anywhere in this repo.
