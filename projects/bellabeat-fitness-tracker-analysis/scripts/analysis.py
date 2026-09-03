"""Bellabeat Fitness Tracker Data Analysis Pipeline.

Ingests, cleans, and transforms personal fitness tracker data to evaluate physical activity,
caloric expenditure, and sleep latency patterns for digital health product strategy.
"""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "visualizations"
DOCS_DIR = PROJECT_ROOT / "docs"

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ACTIVITY_ORDER = [
    "Sedentary (<5k)",
    "Lightly Active (5k-7.4k)",
    "Fairly Active (7.5k-9.9k)",
    "Very Active (>=10k)",
]

PALETTE = {
    "Sedentary (<5k)": "#E76F51",
    "Lightly Active (5k-7.4k)": "#F4A261",
    "Fairly Active (7.5k-9.9k)": "#2A9D8F",
    "Very Active (>=10k)": "#264653",
}


def configure_visualization_style() -> None:
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 16,
    })


def categorize_steps(steps: float) -> str:
    if steps < 5000:
        return "Sedentary (<5k)"
    elif steps < 7500:
        return "Lightly Active (5k-7.4k)"
    elif steps < 10000:
        return "Fairly Active (7.5k-9.9k)"
    return "Very Active (>=10k)"


def load_daily_activity(data_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(data_dir / "dailyActivity_merged.csv")
    df["ActivityDate"] = pd.to_datetime(df["ActivityDate"], format="%m/%d/%Y")
    df["Date"] = df["ActivityDate"]
    df["TotalActiveMinutes"] = (
        df["VeryActiveMinutes"] + df["FairlyActiveMinutes"] + df["LightlyActiveMinutes"]
    )
    df["DayOfWeek"] = pd.Categorical(df["Date"].dt.day_name(), categories=DAY_ORDER, ordered=True)
    df["ActivityCategory"] = pd.Categorical(
        df["TotalSteps"].apply(categorize_steps), categories=ACTIVITY_ORDER, ordered=True
    )
    return df


def load_sleep_records(data_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(data_dir / "sleepDay_merged.csv")
    df["SleepDay"] = pd.to_datetime(df["SleepDay"], format="%m/%d/%Y %I:%M:%S %p")
    df["Date"] = df["SleepDay"].dt.normalize()
    df = df.drop_duplicates(subset=["Id", "Date"]).copy()
    df["SleepEfficiency"] = (df["TotalMinutesAsleep"] / df["TotalTimeInBed"]) * 100
    df["TimeAwakeInBed"] = df["TotalTimeInBed"] - df["TotalMinutesAsleep"]
    return df


def build_user_personas(activity_df: pd.DataFrame) -> pd.DataFrame:
    user_df = activity_df.groupby("Id")["TotalSteps"].mean().reset_index()
    user_df["Category"] = pd.Categorical(
        user_df["TotalSteps"].apply(categorize_steps), categories=ACTIVITY_ORDER, ordered=True
    )
    return user_df


def plot_step_calories(activity_df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=activity_df,
        x="TotalSteps",
        y="Calories",
        hue="ActivityCategory",
        hue_order=ACTIVITY_ORDER,
        palette=PALETTE,
        alpha=0.75,
        s=60,
        edgecolor="w",
        linewidth=0.5,
        ax=ax,
    )
    
    valid = activity_df.dropna(subset=["TotalSteps", "Calories"])
    slope, intercept = np.polyfit(valid["TotalSteps"], valid["Calories"], 1)
    ax.plot(
        np.sort(valid["TotalSteps"]),
        slope * np.sort(valid["TotalSteps"]) + intercept,
        color="#2b2d42",
        linestyle="--",
        linewidth=2,
        label=f"Trendline ({slope:.2f} kcal/step)",
    )

    corr = activity_df["TotalSteps"].corr(activity_df["Calories"])
    ax.text(
        0.05,
        0.92,
        f"Pearson r = {corr:.2f}\nSample: {len(activity_df):,} daily records ({activity_df['Id'].nunique()} users)",
        transform=ax.transAxes,
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#ced4da", alpha=0.9),
    )

    ax.set_title("Total Steps vs. Caloric Expenditure by Activity Segment", pad=15, fontweight="bold")
    ax.set_xlabel("Daily Steps")
    ax.set_ylabel("Calories Burned (kcal)")
    ax.legend(title="Activity Segment", frameon=True, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_sleep_latency(sleep_df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=sleep_df,
        x="TotalTimeInBed",
        y="TotalMinutesAsleep",
        scatter_kws={"color": "#457B9D", "alpha": 0.55, "s": 50},
        line_kws={"color": "#1D3557", "linewidth": 2.5, "label": "Linear Fit"},
        ax=ax,
    )
    
    ax.axhline(420, color="#E63946", linestyle=":", linewidth=1.8, label="CDC Sleep Target (7 hrs / 420 min)")
    
    avg_sleep = sleep_df["TotalMinutesAsleep"].mean()
    avg_awake = sleep_df["TimeAwakeInBed"].mean()
    efficiency = sleep_df["SleepEfficiency"].mean()
    ax.text(
        0.05,
        0.82,
        f"Mean Sleep: {avg_sleep:.0f} mins ({avg_sleep/60:.1f} hrs)\n"
        f"Mean Latency / Awake: {avg_awake:.0f} mins\n"
        f"Mean Efficiency: {efficiency:.1f}%\n"
        f"Sample: {len(sleep_df)} records ({sleep_df['Id'].nunique()} users)",
        transform=ax.transAxes,
        fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#ced4da", alpha=0.9),
    )

    ax.set_title("Total Time in Bed vs. Duration Asleep", pad=15, fontweight="bold")
    ax.set_xlabel("Time in Bed (minutes)")
    ax.set_ylabel("Minutes Asleep (minutes)")
    ax.legend(frameon=True, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_activity_segmentation(
    user_df: pd.DataFrame, activity_df: pd.DataFrame, output_path: Path
) -> None:
    user_counts = user_df["Category"].value_counts().reindex(ACTIVITY_ORDER)
    log_counts = activity_df["ActivityCategory"].value_counts().reindex(ACTIVITY_ORDER)
    colors = [PALETTE[cat] for cat in ACTIVITY_ORDER]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    wedges1, _, autotexts1 = ax1.pie(
        user_counts,
        labels=[f"{cat.split()[0]} ({v})" for cat, v in zip(ACTIVITY_ORDER, user_counts)],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for at in autotexts1:
        at.set_fontsize(10)
        at.set_weight("bold")
    ax1.set_title(f"Unique User Personas\n(N = {len(user_df)} users by mean daily steps)", fontweight="bold", pad=12)

    wedges2, _, autotexts2 = ax2.pie(
        log_counts,
        labels=[f"{cat.split()[0]} ({v})" for cat, v in zip(ACTIVITY_ORDER, log_counts)],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for at in autotexts2:
        at.set_fontsize(10)
        at.set_weight("bold")
    ax2.set_title(f"Daily Activity Records\n(N = {len(activity_df):,} logged days)", fontweight="bold", pad=12)

    fig.suptitle("Activity Distribution: Distinct User Personas vs. Daily Record Volume", fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_weekly_step_patterns(activity_df: pd.DataFrame, output_path: Path) -> None:
    avg_steps = activity_df.groupby("DayOfWeek", observed=True)["TotalSteps"].mean().reindex(DAY_ORDER)
    overall_mean = activity_df["TotalSteps"].mean()

    fig, ax = plt.subplots(figsize=(11, 6))
    bar_colors = [
        "#457B9D" if day not in ["Saturday", "Sunday"] else ("#2A9D8F" if day == "Saturday" else "#E76F51")
        for day in DAY_ORDER
    ]
    bars = ax.bar(DAY_ORDER, avg_steps.values, color=bar_colors, width=0.62, edgecolor="#2b2d42", linewidth=0.8)

    ax.axhline(overall_mean, color="#333333", linestyle="--", linewidth=1.5, label=f"Weekly Mean ({overall_mean:,.0f} steps)")
    ax.axhline(10000, color="#2A9D8F", linestyle=":", linewidth=1.5, label="10,000 Step Target")

    for bar in bars:
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 120,
            f"{yval:,.0f}",
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
        )

    sat_steps = avg_steps["Saturday"]
    sun_steps = avg_steps["Sunday"]
    ax.annotate(
        f"Peak Day\n({sat_steps:,.0f} steps)",
        xy=(5, sat_steps),
        xytext=(4.3, sat_steps + 1100),
        arrowprops=dict(facecolor="#2A9D8F", shrink=0.08, width=1.5, headwidth=7),
        fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F8F5", edgecolor="#2A9D8F"),
    )
    ax.annotate(
        f"Rest / Recovery Day\n({sun_steps:,.0f} steps)",
        xy=(6, sun_steps),
        xytext=(5.6, sun_steps + 1200),
        arrowprops=dict(facecolor="#E76F51", shrink=0.08, width=1.5, headwidth=7),
        fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FDEDEC", edgecolor="#E76F51"),
    )

    ax.set_title("Mean Daily Step Volume by Day of Week", pad=15, fontweight="bold")
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Mean Total Steps")
    ax.set_ylim(0, 11500)
    ax.legend(loc="upper left", frameon=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def export_summary_metrics(activity_df: pd.DataFrame, sleep_df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_activity = [
        "TotalSteps",
        "TotalDistance",
        "VeryActiveMinutes",
        "FairlyActiveMinutes",
        "LightlyActiveMinutes",
        "SedentaryMinutes",
        "TotalActiveMinutes",
        "Calories",
    ]
    metrics_sleep = [
        "TotalSleepRecords",
        "TotalMinutesAsleep",
        "TotalTimeInBed",
        "TimeAwakeInBed",
        "SleepEfficiency",
    ]

    summary_act = activity_df[metrics_activity].describe().T
    summary_act["Dataset"] = f"Daily Activity (N={len(activity_df)}, {activity_df['Id'].nunique()} users)"

    summary_slp = sleep_df[metrics_sleep].describe().T
    summary_slp["Dataset"] = f"Sleep Records (N={len(sleep_df)}, {sleep_df['Id'].nunique()} users)"

    combined = pd.concat([summary_act, summary_slp])
    combined.to_csv(output_path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_visualization_style()

    daily_activity = load_daily_activity(DATA_DIR)
    sleep_records = load_sleep_records(DATA_DIR)
    user_personas = build_user_personas(daily_activity)

    plot_step_calories(daily_activity, OUTPUT_DIR / "steps_vs_calories.png")
    plot_sleep_latency(sleep_records, OUTPUT_DIR / "bed_vs_sleep.png")
    plot_activity_segmentation(user_personas, daily_activity, OUTPUT_DIR / "user_type_distribution.png")
    plot_weekly_step_patterns(daily_activity, OUTPUT_DIR / "avg_steps_by_day.png")

    export_summary_metrics(daily_activity, sleep_records, DOCS_DIR / "summary_statistics.csv")
    print(f"Processed {len(daily_activity)} activity records and {len(sleep_records)} sleep records.")


if __name__ == "__main__":
    main()
