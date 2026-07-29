"""Reproducible Cyclistic/Divvy trip analysis.

Downloads the URLs in data/source_urls.csv, validates trip records in chunks,
creates aggregate tables, charts, and a concise executive narrative.
"""
from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Keep matplotlib's cache inside the project so the script works in restricted profiles.
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for CI and headless environments.
import matplotlib.pyplot as plt
import pandas as pd
import requests

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
MANIFEST = ROOT / "data" / "source_urls.csv"
COLORS = {"casual": "#E76F51", "member": "#264653"}
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze public Divvy trip data.")
    parser.add_argument("--months", type=int, default=None, help="Analyze only the first N manifest months.")
    parser.add_argument("--skip-download", action="store_true", help="Reuse ZIPs already in data/raw.")
    parser.add_argument("--min-minutes", type=float, default=1, help="Minimum valid ride duration (default: 1).")
    parser.add_argument("--max-hours", type=float, default=24, help="Maximum valid ride duration (default: 24).")
    return parser.parse_args()


def download(url: str, destination: Path) -> None:
    """Stream a public ZIP to disk, avoiding a large in-memory response."""
    if destination.exists():
        print(f"Using cached {destination.name}")
        return
    print(f"Downloading {url}")
    with requests.get(url, stream=True, timeout=90) as response:
        response.raise_for_status()
        with destination.open("wb") as file:
            for block in response.iter_content(chunk_size=1024 * 1024):
                if block:
                    file.write(block)


def csv_in_zip(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        csvs = [name for name in archive.namelist() if name.lower().endswith(".csv") and not name.startswith("__MACOSX/")]
    if len(csvs) != 1:
        raise ValueError(f"Expected one CSV in {path.name}; found {csvs}")
    return csvs[0]


def cleaned_chunks(zip_path: Path, min_minutes: float, max_hours: float):
    """Yield cleaned chunks and a per-chunk quality-count dictionary."""
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(csv_in_zip(zip_path)) as binary:
            for chunk in pd.read_csv(binary, chunksize=200_000, low_memory=False):
                initial = len(chunk)
                chunk = chunk.rename(columns={"member_casual": "rider_type", "started_at": "started_at", "ended_at": "ended_at"})
                required = {"started_at", "ended_at", "rider_type", "rideable_type"}
                missing = required - set(chunk.columns)
                if missing:
                    raise ValueError(f"{zip_path.name} is missing required columns: {sorted(missing)}")

                chunk["started_at"] = pd.to_datetime(chunk["started_at"], errors="coerce")
                chunk["ended_at"] = pd.to_datetime(chunk["ended_at"], errors="coerce")
                valid_timestamps = chunk["started_at"].notna() & chunk["ended_at"].notna()
                valid_type = chunk["rider_type"].isin(["member", "casual"])
                chunk["ride_minutes"] = (chunk["ended_at"] - chunk["started_at"]).dt.total_seconds() / 60
                valid_duration = chunk["ride_minutes"].between(min_minutes, max_hours * 60, inclusive="both")
                keep = valid_timestamps & valid_type & valid_duration
                quality = {
                    "input_rows": initial,
                    "invalid_timestamp_rows": int((~valid_timestamps).sum()),
                    "invalid_rider_type_rows": int((~valid_type).sum()),
                    "duration_outside_rule_rows": int((valid_timestamps & ~valid_duration).sum()),
                    "kept_rows": int(keep.sum()),
                }
                data = chunk.loc[keep, ["started_at", "rider_type", "rideable_type", "ride_minutes"]].copy()
                data["month"] = data["started_at"].dt.to_period("M").astype(str)
                data["weekday"] = pd.Categorical(data["started_at"].dt.day_name(), categories=DAY_ORDER, ordered=True)
                data["is_weekend"] = data["weekday"].isin(["Saturday", "Sunday"])
                data["hour"] = data["started_at"].dt.hour
                yield data, quality


def aggregate_frame(frame: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    return frame.groupby(keys, observed=True).agg(rides=("ride_minutes", "size"), total_minutes=("ride_minutes", "sum")).reset_index()


def finish_aggregate(parts: list[pd.DataFrame], keys: list[str]) -> pd.DataFrame:
    result = pd.concat(parts, ignore_index=True).groupby(keys, as_index=False, observed=True)[["rides", "total_minutes"]].sum()
    result["average_ride_minutes"] = result["total_minutes"] / result["rides"]
    return result


def make_charts(monthly: pd.DataFrame, daily: pd.DataFrame, bike: pd.DataFrame) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    for rider in ("member", "casual"):
        view = monthly[monthly.rider_type.eq(rider)]
        ax.plot(view.month, view.rides, marker="o", linewidth=2.5, color=COLORS[rider], label=rider.title())
    ax.set(title="Ride volume by membership type", xlabel="Month", ylabel="Trips")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(frameon=True, title="Rider type")
    fig.tight_layout(); fig.savefig(FIGURES / "monthly_ride_volume.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for rider in ("member", "casual"):
        view = daily[daily.rider_type.eq(rider)].set_index("weekday").reindex(DAY_ORDER).reset_index()
        ax.plot(view.weekday, view.average_ride_minutes, marker="o", linewidth=2.5, color=COLORS[rider], label=rider.title())
    ax.set(title="Average ride duration by day of week", xlabel="Day", ylabel="Average minutes")
    ax.tick_params(axis="x", rotation=25)
    ax.legend(frameon=True, title="Rider type")
    fig.tight_layout(); fig.savefig(FIGURES / "average_duration_by_day.png", dpi=180); plt.close(fig)

    pivot = bike.pivot(index="rideable_type", columns="rider_type", values="rides").fillna(0)
    pivot = pivot.reindex(columns=[c for c in ("member", "casual") if c in pivot.columns])
    ax = pivot.plot(kind="bar", figsize=(10, 5), color=[COLORS.get(c, "#777777") for c in pivot.columns])
    ax.set(title="Bike-type mix by membership type", xlabel="Bike type", ylabel="Trips")
    ax.legend(title="Rider type")
    plt.xticks(rotation=0); plt.tight_layout(); plt.savefig(FIGURES / "bike_type_mix.png", dpi=180); plt.close()


def write_summary(monthly: pd.DataFrame, daily: pd.DataFrame, quality: pd.DataFrame, source_months: list[str]) -> None:
    totals = monthly.groupby("rider_type", as_index=False).agg(rides=("rides", "sum"), total_minutes=("total_minutes", "sum"))
    totals["average_ride_minutes"] = totals.total_minutes / totals.rides
    weekday = daily[daily.weekday.isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])].groupby("rider_type").rides.sum()
    weekend = daily[daily.weekday.isin(["Saturday", "Sunday"])].groupby("rider_type").rides.sum()
    total_by_type = totals.set_index("rider_type").rides
    weekend_share = (weekend / total_by_type * 100).round(1)
    casual_duration = totals.set_index("rider_type").loc["casual", "average_ride_minutes"]
    member_duration = totals.set_index("rider_type").loc["member", "average_ride_minutes"]
    kept = int(quality.kept_rows.sum())
    rejected = int(quality.input_rows.sum() - kept)

    lines = [
        "# Cyclistic/Divvy analysis summary", "",
        f"**Trip-start window:** {monthly.month.min()} to {monthly.month.max()}  ",
        f"**Archive files processed:** {source_months[0]} to {source_months[-1]}  ",
        f"**Cleaned trips analyzed:** {kept:,}  ",
        f"**Rows excluded by documented rules:** {rejected:,}", "",
        "## What the data shows", "",
        "| Rider type | Trips | Average ride (minutes) | Weekend share |",
        "|---|---:|---:|---:|",
    ]
    for row in totals.sort_values("rider_type").itertuples():
        lines.append(f"| {row.rider_type.title()} | {row.rides:,.0f} | {row.average_ride_minutes:.1f} | {weekend_share.get(row.rider_type, 0):.1f}% |")
    lines += ["", "## Interpretation", "", f"Casual rides average **{casual_duration:.1f} minutes**, versus **{member_duration:.1f} minutes** for members. Compare the monthly-volume and weekday-duration charts before deciding campaign timing; these descriptive results show behavior patterns, not why any individual purchased a pass.", "", "## Recommended next experiments", "", "1. Offer repeat weekend casual riders an in-app membership-value comparison after their second or third ride.", "2. Test a spring/fall weekday-commute trial against a standard annual-membership offer.", "3. Hold out a randomized control group and assess incremental conversion, retention, and contribution margin.", "", "## Reproducibility notes", "", "Source URLs are recorded in `data/source_urls.csv`. Quality counts, including invalid timestamps and duration-rule exclusions, are in `data/processed/data_quality_report.csv`. The pipeline uses no personally identifying fields."]
    (ROOT / "reports" / "analysis_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    RAW.mkdir(parents=True, exist_ok=True); PROCESSED.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(MANIFEST, dtype=str)
    if args.months:
        manifest = manifest.head(args.months)
    if manifest.empty:
        raise ValueError("The selected manifest is empty.")

    aggregates = {"monthly": [], "daily": [], "bike": [], "hour": []}
    quality_rows = []
    for source in manifest.itertuples(index=False):
        local_zip = RAW / f"{source.month.replace('-', '')}-divvy-tripdata.zip"
        if not args.skip_download:
            download(source.url, local_zip)
        if not local_zip.exists():
            raise FileNotFoundError(f"Missing {local_zip}; rerun without --skip-download.")
        for data, quality in cleaned_chunks(local_zip, args.min_minutes, args.max_hours):
            quality["source_month"] = source.month
            quality_rows.append(quality)
            aggregates["monthly"].append(aggregate_frame(data, ["month", "rider_type"]))
            aggregates["daily"].append(aggregate_frame(data, ["weekday", "rider_type"]))
            aggregates["bike"].append(aggregate_frame(data, ["rideable_type", "rider_type"]))
            aggregates["hour"].append(aggregate_frame(data, ["hour", "rider_type"]))

    monthly = finish_aggregate(aggregates["monthly"], ["month", "rider_type"])
    daily = finish_aggregate(aggregates["daily"], ["weekday", "rider_type"])
    bike = finish_aggregate(aggregates["bike"], ["rideable_type", "rider_type"])
    hour = finish_aggregate(aggregates["hour"], ["hour", "rider_type"])
    quality = pd.DataFrame(quality_rows).groupby("source_month", as_index=False).sum(numeric_only=True)
    monthly.to_csv(PROCESSED / "monthly_member_summary.csv", index=False)
    daily.to_csv(PROCESSED / "day_member_summary.csv", index=False)
    bike.to_csv(PROCESSED / "rideable_member_summary.csv", index=False)
    hour.to_csv(PROCESSED / "hour_member_summary.csv", index=False)
    quality.to_csv(PROCESSED / "data_quality_report.csv", index=False)
    make_charts(monthly, daily, bike)
    write_summary(monthly, daily, quality, manifest.month.tolist())
    print(f"Done. Analyzed {quality.kept_rows.sum():,} cleaned trips from {len(manifest)} month(s).")


if __name__ == "__main__":
    main()
