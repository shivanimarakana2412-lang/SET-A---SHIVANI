# Delivery Delay Analysis — Set A

End-to-end analysis of delivery performance across four routes and three hubs, using the same 12 clean fact rows in three parallel tools: **Python (pandas)**, **SQL (SQLite)**, and **Power BI**.

## Repository Structure

```
├── data/raw/
│   ├── deliveries.csv          # 13 raw rows (1 exact duplicate: record_id 12)
│   └── routes.csv              # 4 route lookup rows (route_id, route, service_type)
├── python/
│   └── analysis.py             # P1–P3: clean, merge, analyze, chart, export
├── sql/
│   ├── setup.sql                # creates schema, loads 12 clean rows + 4 routes
│   └── queries.sql              # S2a–S2c + S3 integrity check
├── DASHBOARD.pbix               # Power BI report (B1–B3)
├── outputs/
│   ├── clean_data.csv           # merged, cleaned dataset (12 rows)
│   ├── python_summary.csv       # service-type summary from Python
│   ├── python_chart.png         # monthly delay trend chart
│   ├── sql/
│   │   ├── s2a_delay_by_service_type.csv
│   │   ├── s2b_routes_significant_delay.csv
│   │   ├── s2c_top_hubs_by_delay.csv
│   │   └── diagnostic_unmatched_keys.csv
│   └── powerbi_dashboard.png
├── requirements.txt
└── README.md
```

## Setup & How to Run

**Python**
```bash
pip install -r requirements.txt
python python/analysis.py
```
Run from the repo root — the script resolves `data/raw/` and `outputs/` relative to its own location, so it also works if launched from an IDE.

**SQL (SQLite)**
```bash
sqlite3 outputs/delivery.db < sql/setup.sql
sqlite3 outputs/delivery.db < sql/queries.sql
```
Run `setup.sql` first to build the schema and load data, then `queries.sql` to generate the four CSV exports.

**Power BI**
Open `DASHBOARD.pbix` in Power BI Desktop.

## Data Cleaning Notes

- `deliveries.csv` has 13 raw rows; record_id 12 is an exact duplicate and is removed in every tool, leaving **12 clean fact rows**.
- `deliveries` is joined to `routes` on `route_id` (one-to-many, routes → deliveries). The integrity check (S3) confirms **0 unmatched keys** — every `route_id` in deliveries has a matching route.
- Derived field: `delay_days = MAX(actual_days − promised_days, 0)`, used consistently across Python, SQL, and the Power BI DAX measures.
- Month order is fixed as Jan → Feb → Mar (not alphabetical) throughout.

## Key Findings

1. **Overall delay incidence rate is 75%** (9 of 12 deliveries late). This splits unevenly by service type: **Standard is 83.33% late** (5 of 6) vs **Express at 66.67%** (4 of 6), and Standard also carries almost double the total delay days (22 vs 12).
2. **Rural Feeder (R4)** is the single worst route, with **14 total delay days** — more than any other route — and every one of its deliveries was late. **Mumbai** and **Delhi** are the top two hubs by total delay (15 and 14 delay-days respectively), and delays are heavily concentrated in **March** (17 delay-days vs 9 in Feb and 8 in Jan).

## Recommendation

Prioritize a capacity/scheduling review of the **Rural Feeder (R4)** route and **Standard-service** deliveries, with particular attention to the **Mumbai** and **Delhi** hubs — together they account for the bulk of March's delay spike.

## Outputs Reference

| File | Produced by | Contents |
|---|---|---|
| `clean_data.csv` | Python | Merged, deduplicated dataset with `delay_days` |
| `python_summary.csv` | Python | Delay totals & incidence rate by service type |
| `python_chart.png` | Python | Monthly total delay days (Jan→Feb→Mar) |
| `s2a_delay_by_service_type.csv` | SQL | Total delay days by service type |
| `s2b_routes_significant_delay.csv` | SQL | Routes with >8 total delay days |
| `s2c_top_hubs_by_delay.csv` | SQL | Top 2 hubs by total delay days |
| `diagnostic_unmatched_keys.csv` | SQL | Referential integrity check (0 rows expected) |
| `powerbi_dashboard.png` | Power BI | Screenshot of the unfiltered report page |
