# Bellabeat Fitness Tracker Data Analysis: Consumer Behavior & Marketing Strategy

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Reproducible-16a34a)
![Focus](https://img.shields.io/badge/Domain-Health_Tech_%26_Marketing_Analytics-blueviolet)

## Project Overview

This project is a comprehensive data analysis case study for **Bellabeat**, a high-tech manufacturer of health-focused smart products for women. As an analyst advising the marketing analytics team, the primary objective is to analyze smart-device usage data from consumer tracking logs, uncover behavioral trends, and translate those insights into data-backed marketing campaigns and product growth strategies for Bellabeat's ecosystem (the **Bellabeat App**, **Leaf**, and **Time** smart wellness trackers).

---

## Business Task & Core Questions

Analyze smart-device tracking data to identify behavioral trends across physical activity, sleep hygiene, and daily habits, and formulate strategic recommendations to optimize Bellabeat's marketing strategy and user engagement.

### Core Strategic Questions:
1. **What are the predominant trends in daily activity, sedentary time, and sleep patterns?**
2. **How do these patterns differ across unique user personas versus day-to-day variance?**
3. **How can Bellabeat leverage these behavioral insights to drive device adoption and app subscription retention?**

---

## Data Sources & Integrity Audit

The analysis utilizes the public **FitBit Fitness Tracker Data** (Mobius, Kaggle / Zenodo). 

### Data Lineage & Quality Notes:
- **Eligible Users:** Although the original Kaggle metadata mentions 30 eligible Fitbit users, an audit of the raw records reveals **33 distinct user IDs** in `dailyActivity_merged.csv` and **24 distinct user IDs** in `sleepDay_merged.csv`. Documenting this nuance is critical for analytical accuracy.
- **Timeframe:** March 12, 2016 – May 12, 2016 (minute-, hourly-, and daily-level output).
- **Files Utilized:**
  - `data/dailyActivity_merged.csv`: 940 daily records tracking steps, distances, intensities, active minutes, and calories.
  - `data/sleepDay_merged.csv`: 413 original sleep records (410 records after deduplication) tracking sleep sessions, total sleep duration, and time in bed.
- **Data Governance & Privacy:** The dataset is fully anonymized and distributed under CC0: Public Domain. No personally identifiable information (PII) is accessed or stored.

---

## Methodology & Pipeline Architecture

The analysis pipeline is built in Python (`scripts/analysis.py`) following senior data development practices:
1. **Grain Separation:** Disaggregates **distinct user personas** ($N=33$ unique users classified by mean daily steps) from **daily activity log variance** ($N=940$ individual daily logs). This avoids the common mistake of treating 30 logged days by one user as 30 separate users.
2. **Sampling Bias Mitigation:** Computes general activity distributions, step counts, and day-of-week trends on the full daily activity dataset ($N=940$) rather than discarding 530 rows through premature inner joins with sleep data (only 24 users logged sleep).
3. **Robust Date Parsing & Deduplication:** Applies explicit datetime parsing schemas (`%m/%d/%Y` and `%m/%d/%Y %I:%M:%S %p`) to prevent runtime parsing warnings and ensure deterministic sorting.
4. **Feature Engineering:** Computes `TotalActiveMinutes`, `SleepEfficiency` ($\frac{\text{Minutes Asleep}}{\text{Time in Bed}} \times 100$), `TimeAwakeInBed`, and step categories adhering to the Tudor-Locke & Bassett (2004) standard.

---

## Reproduce the Analysis

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute the analysis pipeline
python scripts/analysis.py
```

The script processes raw inputs from `data/`, regenerates high-resolution figures in `visualizations/`, and updates `docs/summary_statistics.csv`.

---

## Key Findings & Visualizations

### 1. Step-to-Calorie Dynamics: Linear Expenditure Relationship
A strong positive linear correlation ($r = 0.59$) exists between daily steps and caloric expenditure. 

![Total Steps vs Calories Burned](./visualizations/steps_vs_calories.png)

- **Finding:** Every additional 1,000 steps corresponds to an estimated ~60–80 kcal increase in daily burn.
- **Sedentary Risk:** The lowest quartile logs under 3,790 steps/day, burning significantly fewer calories (often below baseline metabolic expenditure), creating a prime intervention target.

---

### 2. Sleep Latency & Sleep Efficiency Analysis
Tracking records show an average sleep duration of **419 minutes (~7.0 hours)**, closely matching CDC health guidelines. However, users spend an average of **458 minutes (~7.6 hours)** in bed.

![Total Time in Bed vs Total Minutes Asleep](./visualizations/bed_vs_sleep.png)

- **Finding:** Users spend an average of **39 minutes awake in bed** before falling asleep or after waking up (average sleep efficiency of **91.6%**).
- **Outlier Patterns:** Significant dispersion occurs among users spending >550 minutes in bed without receiving proportional sleep, signaling sleep latency issues and suboptimal sleep hygiene.

---

### 3. User Personas vs. Day-to-Day Activity Variance
To prevent misleading claims, this analysis explicitly separates **Distinct User Personas** (by average daily step count across the study) from **Daily Activity Records** (individual day logs).

![Distribution of User Activity Levels](./visualizations/user_type_distribution.png)

- **User Personas ($N=33$ unique individuals):**
  - **Lightly Active (5k–7.4k steps):** 27.3% (9 users)
  - **Fairly Active (7.5k–9.9k steps):** 27.3% (9 users)
  - **Sedentary (<5k steps):** 24.2% (8 users)
  - **Very Active ($\ge$10k steps):** 21.2% (7 users)
- **Key Insight:** While individual daily logs show frequent high-activity days (32.2%), **only 21.2% of users consistently maintain a Very Active lifestyle**. The vast majority (54.5%) are in the moderate middle tiers ("Lightly" or "Fairly Active"), representing Bellabeat's prime addressable customer segment.

---

### 4. Day-of-Week Trends: The "Saturday Surge & Sunday Rest" Dynamic
Activity follows a distinct weekly rhythm that disproves the common misconception of uniform weekend activity.

![Average Total Steps by Day of the Week](./visualizations/avg_steps_by_day.png)

- **The Saturday Surge:** Saturday is the weekly peak, averaging **8,153 steps** (with users having more free time for outdoor recreation and long walks).
- **The Sunday Rest Slump:** Sunday drops to the **lowest step count of the entire week (6,933 steps)**—a 15% decline from Saturday.
- **Weekday Consistency:** Weekdays remain steady between 7,400 and 8,125 steps, with Tuesday exhibiting the highest weekday volume (8,125 steps).

---

## Executive Summary Statistics

The table below presents validated summary statistics from the clean datasets, omitting non-computational IDs and formatted for executive review:

| Metric | Dataset / Sample | Mean | Median (50%) | Std Dev | 25th % | 75th % | Min | Max |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| **Total Daily Steps** | Daily Activity ($N=940$) | 7,638 | 7,406 | 5,087 | 3,790 | 10,727 | 0 | 36,019 |
| **Total Distance (km)** | Daily Activity ($N=940$) | 5.49 | 5.24 | 3.92 | 2.62 | 7.71 | 0.00 | 28.03 |
| **Very Active Minutes** | Daily Activity ($N=940$) | 21.2 | 4.0 | 32.8 | 0.0 | 32.0 | 0.0 | 210.0 |
| **Fairly Active Minutes** | Daily Activity ($N=940$) | 13.6 | 6.0 | 20.0 | 0.0 | 19.0 | 0.0 | 143.0 |
| **Lightly Active Minutes**| Daily Activity ($N=940$) | 192.8 | 199.0 | 109.2 | 127.0 | 264.0 | 0.0 | 518.0 |
| **Sedentary Minutes** | Daily Activity ($N=940$) | 991.2 | 1,057.5 | 301.3 | 729.8 | 1,229.5 | 0.0 | 1,440.0 |
| **Total Active Minutes** | Daily Activity ($N=940$) | 227.5 | 247.0 | 121.8 | 146.8 | 317.3 | 0.0 | 552.0 |
| **Calories Burned (kcal)**| Daily Activity ($N=940$) | 2,304 | 2,134 | 718 | 1,829 | 2,793 | 0 | 4,900 |
| **Total Minutes Asleep** | Sleep Logs ($N=410$) | 419.2 | 432.5 | 118.6 | 361.0 | 490.0 | 58.0 | 796.0 |
| **Total Time in Bed (min)**| Sleep Logs ($N=410$) | 458.5 | 463.0 | 127.5 | 403.8 | 526.0 | 61.0 | 961.0 |
| **Time Awake in Bed (min)**| Sleep Logs ($N=410$) | 39.3 | 25.5 | 46.7 | 17.0 | 40.0 | 0.0 | 371.0 |
| **Sleep Efficiency (%)** | Sleep Logs ($N=410$) | 91.6% | 94.3% | 8.7% | 91.2% | 96.1% | 49.8% | 100.0% |

---

## Actionable Recommendations for Bellabeat

### 1. Capitalize on the "Saturday Surge & Sunday Recovery" Lifecycle
- **Saturday Morning Motivation:** Deploy in-app prompts and community challenges on Saturday morning when user motivation to venture outdoors and accumulate steps is highest.
- **Sunday Evening Wind-Down:** Avoid high-intensity workout notifications on Sunday. Instead, position the **Bellabeat Leaf** and **Bellabeat App** as a Sunday evening recovery companion—promoting guided meditation, sleep readiness scores, and bedtime preparation for the upcoming workweek.

### 2. Product Positioning for the "Moderate Middle" (54.5% of Users)
- Rather than targeting extreme athletes or perpetual sedentary users, position Bellabeat's marketing toward the **54.5% majority** who are Lightly or Fairly Active.
- Frame the **Leaf** jewelry tracker as effortless wellness integration: *"You're already halfway there—small daily habits turn 6,500 steps into lasting vitality."*

### 3. Smart Sleep Hygiene Coaching (Leaf & Time Ecosystem)
- With users averaging nearly 40 minutes awake in bed, introduce a dedicated **Sleep Latency & Wind-Down Feature** in the Bellabeat App.
- Provide personalized bedtime notifications based on historical sleep onset, gentle vibration reminders on the **Time** smartwatch to leave electronic devices outside the bedroom, and soothing soundscapes to reduce sleep onset latency.

### 4. Sedentary Alert Feature & Calorie Transparency
- Users accumulate an average of **991 sedentary minutes (16.5 hours) per day**. 
- Implement customizable haptic inactivity nudges after 60 consecutive minutes of sedentary time during business hours, framing light movement as an easy way to burn an extra 150–200 calories daily.

---

## Author & Contact

**Musaddiq** — *Data Analyst*  
*Specializing in Product Analytics, Business Intelligence, and Python Pipelines.*
