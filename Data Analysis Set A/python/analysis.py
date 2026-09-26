# """
# python/analysis.py
# Delivery Delay Analysis — Set A
# Run from the repository root:  python python/analysis.py
# All paths below are relative to the repo root.
# """

# import pandas as pd
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt

# # ------------------------------------------------------------------
# # P1 — Load, Clean & Merge
# # ------------------------------------------------------------------
# deliveries = pd.read_csv("E:\SHIVANI\data-analysis-set-a-YOUR-STUDENT-ID\data\raw\deliveries.csv")
# routes = pd.read_csv("E:\SHIVANI\data-analysis-set-a-YOUR-STUDENT-ID\data\raw\routes.csv")

# # Confirm numeric types
# deliveries["promised_days"] = pd.to_numeric(deliveries["promised_days"])
# deliveries["actual_days"] = pd.to_numeric(deliveries["actual_days"])

# before_count = len(deliveries)
# deliveries = deliveries.drop_duplicates()
# after_count = len(deliveries)
# print(f"Row count before de-duplication: {before_count}")
# print(f"Row count after de-duplication:  {after_count}")
# assert after_count == 12, "Expected exactly 12 unique fact rows after de-duplication"

# merged = deliveries.merge(routes, on="route_id", how="left")
# assert len(merged) == 12, "Merged frame must contain exactly 12 rows"
# assert merged["service_type"].isna().sum() == 0, "Found unmatched route_id (NaN service_type)"
# print("Merge check passed: 12 rows, 0 unmatched route_id values.")

# # Preserve month order Jan -> Feb -> Mar throughout
# month_order = ["Jan", "Feb", "Mar"]
# merged["month"] = pd.Categorical(merged["month"], categories=month_order, ordered=True)

# # ------------------------------------------------------------------
# # P2 — Derived Field & Service-Type Analysis
# # ------------------------------------------------------------------
# merged["delay_days"] = (merged["actual_days"] - merged["promised_days"]).clip(lower=0)

# merged["is_late"] = merged["actual_days"] > merged["promised_days"]

# service_summary = (
#     merged.groupby("service_type", observed=True)
#     .agg(total_delay_days=("delay_days", "sum"),
#          late_count=("is_late", "sum"),
#          record_count=("is_late", "count"))
#     .reset_index()
# )
# service_summary["delay_incidence_rate_pct"] = (
#     service_summary["late_count"] / service_summary["record_count"] * 100
# ).round(2)
# service_summary = service_summary.sort_values("total_delay_days", ascending=False)

# print("\nService-type summary:")
# print(service_summary[["service_type", "total_delay_days", "delay_incidence_rate_pct"]]
#       .to_string(index=False))

# overall_total_delay = merged["delay_days"].sum()
# route_totals = merged.groupby("route_id")["delay_days"].sum().sort_values(ascending=False)
# top_route = route_totals.index[0]
# top_route_delay = route_totals.iloc[0]
# top_route_share_pct = round(top_route_delay / overall_total_delay * 100, 2)

# print(f"\nRoute with greatest summed delay_days: {top_route} "
#       f"({top_route_delay} delay-days, {top_route_share_pct}% of overall total "
#       f"{overall_total_delay} delay-days)")

# overall_incidence_rate = round(merged["is_late"].sum() / len(merged) * 100, 2)
# print(f"Overall delay incidence rate: {overall_incidence_rate}% "
#       f"({int(merged['is_late'].sum())} of {len(merged)} records)")

# # ------------------------------------------------------------------
# # P3 — Chart & Exports
# # ------------------------------------------------------------------
# monthly_totals = (
#     merged.groupby("month", observed=True)["delay_days"].sum().reindex(month_order)
# )

# plt.figure(figsize=(7, 5))
# plt.bar(monthly_totals.index.astype(str), monthly_totals.values, color="#305496")
# plt.title("Monthly Total Delay Days (Jan -> Feb -> Mar)")
# plt.xlabel("Month")
# plt.ylabel("Total delay_days")
# plt.tight_layout()
# plt.savefig("outputs/python_chart.png", dpi=150)
# plt.close()
# print("\nSaved chart to outputs/python_chart.png")

# export_cols = ["record_id", "month", "route_id", "hub", "promised_days", "actual_days",
#                "route", "service_type", "delay_days"]
# merged_export = merged[export_cols].sort_values("record_id")
# merged_export.to_csv("outputs/clean_data.csv", index=False)

# service_summary.to_csv("outputs/python_summary.csv", index=False)
# print("Saved outputs/clean_data.csv and outputs/python_summary.csv")



"""
python/analysis.py
Delivery Delay Analysis — Set A

Works from ANY working directory (repo root, the python/ folder, or run
from an IDE's Run button) — the script locates the repository root itself
from its own file location, so no manual `cd` is required.

Preferred (matches exam instructions): run from the repository root:
    python python/analysis.py
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Resolve paths relative to the REPO ROOT, not the current working
# directory. This file lives at <repo_root>/python/analysis.py, so its
# parent's parent is always the repo root, regardless of where the
# script is launched from.
# ------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

def rp(relative_path):
    """Resolve a path that is written relative to the repo root."""
    return os.path.join(REPO_ROOT, relative_path)

os.makedirs(rp("outputs"), exist_ok=True)

# ------------------------------------------------------------------
# P1 — Load, Clean & Merge
# ------------------------------------------------------------------
deliveries = pd.read_csv(rp("data/raw/deliveries.csv"))
routes = pd.read_csv(rp("data/raw/routes.csv"))

# Confirm numeric types
deliveries["promised_days"] = pd.to_numeric(deliveries["promised_days"])
deliveries["actual_days"] = pd.to_numeric(deliveries["actual_days"])

before_count = len(deliveries)
deliveries = deliveries.drop_duplicates()
after_count = len(deliveries)
print(f"Row count before de-duplication: {before_count}")
print(f"Row count after de-duplication:  {after_count}")
assert after_count == 12, "Expected exactly 12 unique fact rows after de-duplication"

merged = deliveries.merge(routes, on="route_id", how="left")
assert len(merged) == 12, "Merged frame must contain exactly 12 rows"
assert merged["service_type"].isna().sum() == 0, "Found unmatched route_id (NaN service_type)"
print("Merge check passed: 12 rows, 0 unmatched route_id values.")

# Preserve month order Jan -> Feb -> Mar throughout
month_order = ["Jan", "Feb", "Mar"]
merged["month"] = pd.Categorical(merged["month"], categories=month_order, ordered=True)

# ------------------------------------------------------------------
# P2 — Derived Field & Service-Type Analysis
# ------------------------------------------------------------------
merged["delay_days"] = (merged["actual_days"] - merged["promised_days"]).clip(lower=0)

merged["is_late"] = merged["actual_days"] > merged["promised_days"]

service_summary = (
    merged.groupby("service_type", observed=True)
    .agg(total_delay_days=("delay_days", "sum"),
         late_count=("is_late", "sum"),
         record_count=("is_late", "count"))
    .reset_index()
)
service_summary["delay_incidence_rate_pct"] = (
    service_summary["late_count"] / service_summary["record_count"] * 100
).round(2)
service_summary = service_summary.sort_values("total_delay_days", ascending=False)

print("\nService-type summary:")
print(service_summary[["service_type", "total_delay_days", "delay_incidence_rate_pct"]]
      .to_string(index=False))

overall_total_delay = merged["delay_days"].sum()
route_totals = merged.groupby("route_id")["delay_days"].sum().sort_values(ascending=False)
top_route = route_totals.index[0]
top_route_delay = route_totals.iloc[0]
top_route_share_pct = round(top_route_delay / overall_total_delay * 100, 2)

print(f"\nRoute with greatest summed delay_days: {top_route} "
      f"({top_route_delay} delay-days, {top_route_share_pct}% of overall total "
      f"{overall_total_delay} delay-days)")

overall_incidence_rate = round(merged["is_late"].sum() / len(merged) * 100, 2)
print(f"Overall delay incidence rate: {overall_incidence_rate}% "
      f"({int(merged['is_late'].sum())} of {len(merged)} records)")

# ------------------------------------------------------------------
# P3 — Chart & Exports
# ------------------------------------------------------------------
monthly_totals = (
    merged.groupby("month", observed=True)["delay_days"].sum().reindex(month_order)
)

plt.figure(figsize=(7, 5))
plt.bar(monthly_totals.index.astype(str), monthly_totals.values, color="#305496")
plt.title("Monthly Total Delay Days (Jan -> Feb -> Mar)")
plt.xlabel("Month")
plt.ylabel("Total delay_days")
plt.tight_layout()
plt.savefig(rp("outputs/python_chart.png"), dpi=150)
plt.close()
print("\nSaved chart to outputs/python_chart.png")

export_cols = ["record_id", "month", "route_id", "hub", "promised_days", "actual_days",
               "route", "service_type", "delay_days"]
merged_export = merged[export_cols].sort_values("record_id")
merged_export.to_csv(rp("outputs/clean_data.csv"), index=False)

service_summary.to_csv(rp("outputs/python_summary.csv"), index=False)
print("Saved outputs/clean_data.csv and outputs/python_summary.csv")
