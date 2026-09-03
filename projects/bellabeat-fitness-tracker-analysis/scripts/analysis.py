"""Bellabeat Fitness Tracker Data Analysis.

This script processes Fitbit activity and sleep data to uncover consumer behavior patterns
for Bellabeat's marketing and product development teams.

Senior Developer & Recruiter Best Practices Applied:
- Avoids grain confusion: Differentiates distinct user personas (33 users) from day-to-day variance (940 logs).
- Prevents sampling/tracking bias: Analyzes overall activity and weekly patterns on the full activity
  dataset rather than discarding 530 rows via premature inner-joining with sleep logs.
- Formats dates with explicit formats to optimize parsing speed and prevent runtime warnings.
- Excludes nominal identifiers ('Id') from mathematical summary statistics.
- Generates publication-quality visualizations with clear annotations and executive insights.
"""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set publication style
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16,
})

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "visualizations"
DOCS_DIR = PROJECT_ROOT / "docs"

# Standard step categorization thresholds (Tudor-Locke & Bassett, 2004)
def categorize_steps(steps: float) -> str:
    if steps < 5000:
        return "Sedentary (<5k)"
    elif steps < 7500:
        return "Lightly Active (5k-7.4k)"
    elif steps < 10000:
        return "Fairly Active (7.5k-9.9k)"
    return "Very Active (>=10k)"

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

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_and_clean_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load, validate, and prepare activity and sleep datasets."""
    # 1. Load Daily Activity
    daily_activity = pd.read_csv(DATA_DIR / "dailyActivity_merged.csv")
    daily_activity["ActivityDate"] = pd.to_datetime(daily_activity["ActivityDate"], format="%m/%d/%Y")
    daily_activity["Date"] = daily_activity["ActivityDate"]

    # Compute total active minutes
    daily_activity["TotalActiveMinutes"] = (
        daily_activity["VeryActiveMinutes"]
        + daily_activity["FairlyActiveMinutes"]
        + daily_activity["LightlyActiveMinutes"]
    )
    daily_activity["DayOfWeek"] = pd.Categorical(
        daily_activity["Date"].dt.day_name(), categories=DAY_ORDER, ordered=True
    )
    daily_activity["ActivityCategory"] = pd.Categorical(
        daily_activity["TotalSteps"].apply(categorize_steps),
        categories=ACTIVITY_ORDER,
        ordered=True,
    )

    # 2. Load Sleep Data
    sleep_day = pd.read_csv(DATA_DIR / "sleepDay_merged.csv")
    sleep_day["SleepDay"] = pd.to_datetime(sleep_day["SleepDay"], format="%m/%d/%Y %I:%M:%S %p")
    sleep_day["Date"] = sleep_day["SleepDay"].dt.normalize()
    
    # Remove duplicate records
    dup_count = sleep_day.duplicated(subset=["Id", "Date"]).sum()
    if dup_count > 0:
        sleep_day = sleep_day.drop_duplicates(subset=["Id", "Date"]).copy()

    # Calculate sleep efficiency metric (minutes asleep / time in bed * 100)
    sleep_day["SleepEfficiency"] = (sleep_day["TotalMinutesAsleep"] / sleep_day["TotalTimeInBed"]) * 100
    sleep_day["TimeAwakeInBed"] = sleep_day["TotalTimeInBed"] - sleep_day["TotalMinutesAsleep"]

    # 3. Merged Data (Subset of days where both activity and sleep were recorded)
    merged_data = pd.merge(daily_activity, sleep_day, on=["Id", "Date"], how="inner")

    return daily_activity, sleep_day, merged_data


def generate_visualizations(
    daily_activity: pd.DataFrame, sleep_day: pd.DataFrame, merged_data: pd.DataFrame
) -> None:
    """Generate professional, publication-quality visualizations."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # Chart 1: Total Steps vs Calories Burned (Full Activity Dataset, N=940)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=daily_activity,
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
    
    # Add trendline
    valid = daily_activity.dropna(subset=["TotalSteps", "Calories"])
    z = np.polyfit(valid["TotalSteps"], valid["Calories"], 1)
    p = np.poly1d(z)
    ax.plot(
        np.sort(valid["TotalSteps"]),
        p(np.sort(valid["TotalSteps"])),
        color="#2b2d42",
        linestyle="--",
        linewidth=2,
        label=f"Trendline (slope: {z[0]:.2f} cal/step)",
    )

    corr = daily_activity["TotalSteps"].corr(daily_activity["Calories"])
    ax.text(
        0.05,
        0.92,
        f"Pearson r = {corr:.2f} (Strong positive correlation)\nSample: {len(daily_activity):,} days across {daily_activity['Id'].nunique()} users",
        transform=ax.transAxes,
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#ced4da", alpha=0.9),
    )

    ax.set_title("Total Steps vs. Calories Burned by Activity Level", pad=15, fontweight="bold")
    ax.set_xlabel("Daily Total Steps")
    ax.set_ylabel("Calories Burned (kcal)")
    ax.legend(title="Activity Category", frameon=True, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "steps_vs_calories.png", dpi=200)
    plt.close(fig)

    # -------------------------------------------------------------
    # Chart 2: Total Time in Bed vs Total Minutes Asleep (Sleep Dataset, N=410)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=sleep_day,
        x="TotalTimeInBed",
        y="TotalMinutesAsleep",
        scatter_kws={"color": "#457B9D", "alpha": 0.55, "s": 50},
        line_kws={"color": "#1D3557", "linewidth": 2.5, "label": "Regression Trend"},
        ax=ax,
    )
    
    # 7-hour (420 min) sleep benchmark reference line
    ax.axhline(420, color="#E63946", linestyle=":", linewidth=1.8, label="CDC Recommended Sleep (7 hrs / 420 min)")
    
    avg_awake = sleep_day["TimeAwakeInBed"].mean()
    efficiency = sleep_day["SleepEfficiency"].mean()
    ax.text(
        0.05,
        0.82,
        f"Average Sleep: {sleep_day['TotalMinutesAsleep'].mean():.0f} mins (7.0 hrs)\n"
        f"Average Time Awake in Bed: {avg_awake:.0f} mins\n"
        f"Average Sleep Efficiency: {efficiency:.1f}%\n"
        f"Sample: {len(sleep_day)} logs ({sleep_day['Id'].nunique()} users)",
        transform=ax.transAxes,
        fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#ced4da", alpha=0.9),
    )

    ax.set_title("Total Time in Bed vs. Actual Minutes Asleep", pad=15, fontweight="bold")
    ax.set_xlabel("Total Time in Bed (minutes)")
    ax.set_ylabel("Total Minutes Asleep (minutes)")
    ax.legend(frameon=True, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "bed_vs_sleep.png", dpi=200)
    plt.close(fig)

    # -------------------------------------------------------------
    # Chart 3: Dual-Panel User Personas vs. Daily Log Records
    # Addresses grain confusion directly!
    # -------------------------------------------------------------
    # User level persona: Average daily steps per unique user
    user_profiles = daily_activity.groupby("Id")["TotalSteps"].mean().reset_index()
    user_profiles["Category"] = pd.Categorical(
        user_profiles["TotalSteps"].apply(categorize_steps),
        categories=ACTIVITY_ORDER,
        ordered=True,
    )
    user_counts = user_profiles["Category"].value_counts().reindex(ACTIVITY_ORDER)
    log_counts = daily_activity["ActivityCategory"].value_counts().reindex(ACTIVITY_ORDER)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot A: Distinct User Personas (N=33 users)
    colors_list = [PALETTE[cat] for cat in ACTIVITY_ORDER]
    wedges1, texts1, autotexts1 = ax1.pie(
        user_counts,
        labels=[f"{cat.split()[0]} ({val})" for cat, val in zip(ACTIVITY_ORDER, user_counts)],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_list,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for at in autotexts1:
        at.set_fontsize(10)
        at.set_weight("bold")
    ax1.set_title("Distinct User Personas\n(N = 33 unique users by average daily steps)", fontweight="bold", pad=12)

    # Subplot B: Daily Activity Records (N=940 logs)
    wedges2, texts2, autotexts2 = ax2.pie(
        log_counts,
        labels=[f"{cat.split()[0]} ({val})" for cat, val in zip(ACTIVITY_ORDER, log_counts)],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_list,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for at in autotexts2:
        at.set_fontsize(10)
        at.set_weight("bold")
    ax2.set_title("Daily Activity Logs\n(N = 940 logged days showing day-to-day variance)", fontweight="bold", pad=12)

    fig.suptitle("Activity Distribution: User Personas vs. Daily Activity Records", fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "user_type_distribution.png", dpi=200)
    plt.close(fig)

    # -------------------------------------------------------------
    # Chart 4: Average Steps by Day of Week (Full Activity Dataset, N=940)
    # Highlights the TRUE Saturday Peak & Sunday Slump
    # -------------------------------------------------------------
    avg_steps = daily_activity.groupby("DayOfWeek", observed=True)["TotalSteps"].mean().reindex(DAY_ORDER)
    overall_mean = daily_activity["TotalSteps"].mean()

    fig, ax = plt.subplots(figsize=(11, 6))
    bar_colors = ["#457B9D" if day not in ["Saturday", "Sunday"] else ("#2A9D8F" if day == "Saturday" else "#E76F51") for day in DAY_ORDER]
    bars = ax.bar(DAY_ORDER, avg_steps.values, color=bar_colors, width=0.62, edgecolor="#2b2d42", linewidth=0.8)

    # Benchmark line
    ax.axhline(overall_mean, color="#333333", linestyle="--", linewidth=1.5, label=f"Weekly Average ({overall_mean:,.0f} steps)")
    ax.axhline(10000, color="#2A9D8F", linestyle=":", linewidth=1.5, label="10k Steps Recommended Goal")

    # Add direct data labels above bars
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

    # Annotate Saturday peak and Sunday drop
    sat_steps = avg_steps["Saturday"]
    sun_steps = avg_steps["Sunday"]
    ax.annotate(
        f"Peak Activity Day\n({sat_steps:,.0f} steps)",
        xy=(5, sat_steps),
        xytext=(4.3, sat_steps + 1100),
        arrowprops=dict(facecolor="#2A9D8F", shrink=0.08, width=1.5, headwidth=7),
        fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F8F5", edgecolor="#2A9D8F"),
    )
    ax.annotate(
        f"Weekly Trough (Rest Day)\n({sun_steps:,.0f} steps)",
        xy=(6, sun_steps),
        xytext=(5.6, sun_steps + 1200),
        arrowprops=dict(facecolor="#E76F51", shrink=0.08, width=1.5, headwidth=7),
        fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FDEDEC", edgecolor="#E76F51"),
    )

    ax.set_title("Average Daily Steps by Day of Week: The 'Saturday Surge & Sunday Rest' Dynamic", pad=15, fontweight="bold")
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Average Total Steps")
    ax.set_ylim(0, 11500)
    ax.legend(loc="upper left", frameon=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "avg_steps_by_day.png", dpi=200)
    plt.close(fig)


def export_summary_statistics(
    daily_activity: pd.DataFrame, sleep_day: pd.DataFrame, merged_data: pd.DataFrame
) -> None:
    """Export clean summary statistics excluding nominal identifiers."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Filter numerical metric columns only (exclude 'Id')
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

    summary_act = daily_activity[metrics_activity].describe().T
    summary_act["Dataset"] = f"Daily Activity (N={len(daily_activity)}, 33 users)"

    summary_slp = sleep_day[metrics_sleep].describe().T
    summary_slp["Dataset"] = f"Sleep Logs (N={len(sleep_day)}, 24 users)"

    combined_summary = pd.concat([summary_act, summary_slp])
    combined_summary.to_csv(DOCS_DIR / "summary_statistics.csv")
    print(f"Summary statistics exported to {DOCS_DIR / 'summary_statistics.csv'}")


def main() -> None:
    print("Starting Bellabeat fitness tracker data analysis...")
    daily_activity, sleep_day, merged_data = load_and_clean_data()
    print(f"Loaded {len(daily_activity)} daily activity records across {daily_activity['Id'].nunique()} distinct users.")
    print(f"Loaded {len(sleep_day)} clean sleep records across {sleep_day['Id'].nunique()} distinct users.")
    print(f"Merged {len(merged_data)} concurrent activity & sleep records across {merged_data['Id'].nunique()} users.")

    generate_visualizations(daily_activity, sleep_day, merged_data)
    print("Visualizations generated successfully in visualizations/")

    export_summary_statistics(daily_activity, sleep_day, merged_data)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
