# Bellabeat Consumer Health Analytics: Behavioral Segmentation & Product Strategy

## Executive Summary

This study investigates smart-device consumer usage data to identify physical activity, caloric burn, and sleep latency patterns across consumer cohorts. The analytical goal is to translate behavioral trends into quantitative inputs for Bellabeat's product ecosystem—specifically optimizing feature engagement for the **Bellabeat Leaf** wellness tracker, **Time** smartwatch, and subscription membership services.

---

## Data Architecture & Quality Validation

### 1. Data Provenance & Lineage
The analysis evaluates daily activity and sleep records from the public Fitbit fitness tracker dataset collected across a two-month observation window:
- **Daily Activity Domain (`dailyActivity_merged.csv`):** 940 daily observations tracking step volume, distance metrics, active minute intensities, and caloric expenditure.
- **Sleep Quality Domain (`sleepDay_merged.csv`):** 413 initial sleep sessions recording total minutes asleep and time in bed.

### 2. Grain Definition & Exclusion Rules
- **User Identifier Audit:** While original dataset metadata references 30 participants, exploratory validation reveals **33 distinct user IDs** in the activity log and **24 distinct user IDs** in the sleep log.
- **Grain Disaggregation:** The data grain represents *user-days* (one logged day per user ID). To prevent observational bias, analyses distinguish between **unique user personas** ($N=33$, computed from per-user averages) and **day-to-day variance** ($N=940$ daily records).
- **Deduplication:** Identified and eliminated 3 duplicate records in the sleep dataset on composite key `[Id, SleepDay]`, yielding 410 unique sleep observations.
- **Join Logic:** Overall activity, step distributions, and day-of-week demand are computed on the full 940-record activity dataset to avoid survivorship bias introduced by inner-joining with the smaller sleep subset (where only 24 users tracked sleep).

---

## Exploratory Data Analysis & Key Segments

### 1. Activity Segmentation & Persona Distribution
Users are categorized according to standard physical activity thresholds (Tudor-Locke & Bassett, 2004):
- **Sedentary:** $< 5,000$ steps/day
- **Lightly Active:** $5,000 - 7,499$ steps/day
- **Fairly Active:** $7,500 - 9,999$ steps/day
- **Very Active:** $\ge 10,000$ steps/day

![Activity Distribution](./visualizations/user_type_distribution.png)

- **User Personas ($N=33$ unique users):**
  - Lightly Active: 27.3% (9 users)
  - Fairly Active: 27.3% (9 users)
  - Sedentary: 24.2% (8 users)
  - Very Active: 21.2% (7 users)
- **Key Takeaway:** Over **54% of unique users** fall into the moderate activity tiers (5,000–9,999 steps). While aggregate daily logs show frequent high-activity spikes, only 21% of users consistently sustain a Very Active profile over time.

---

### 2. Step-to-Calorie Linear Dynamics
Evaluating total daily steps against caloric expenditure yields a strong positive linear relationship ($r = 0.59$).

![Total Steps vs Calories Burned](./visualizations/steps_vs_calories.png)

- Every incremental 1,000 steps corresponds to approximately 60–80 kcal of active energy expenditure.
- The lowest activity quartile logs fewer than 3,790 steps daily, resulting in reduced caloric expenditure below baseline targets.

---

### 3. Sleep Latency & Sleep Efficiency
Analysis of 410 validated sleep logs identifies an average sleep duration of **419 minutes (~7.0 hours)**, adhering closely to clinical sleep recommendations.

![Time in Bed vs Minutes Asleep](./visualizations/bed_vs_sleep.png)

- **Sleep Latency & Wakefulness:** Users spend an average of **458 minutes (~7.6 hours)** in bed, indicating a mean wakefulness / latency window of **39 minutes per night** (average sleep efficiency of **91.6%**).
- Outliers spending $> 550$ minutes in bed without proportional sleep indicate opportunities for targeted sleep hygiene interventions.

---

### 4. Day-of-Week Activity Rhythm
Weekly step counts follow a pronounced cadence characterized by a weekend surge and subsequent rest day.

![Average Total Steps by Day of Week](./visualizations/avg_steps_by_day.png)

- **Saturday Peak:** Saturday represents the peak activity day, averaging **8,153 steps**.
- **Sunday Recovery:** Sunday exhibits the lowest step count of the entire week (**6,933 steps**), representing a 15% drop from Saturday peak.
- **Weekday Baseline:** Weekday volume remains steady between 7,400 and 8,125 steps, with Tuesday representing the highest weekday volume (8,125 steps).

---

## Validated Summary Metrics

| Metric | Dataset Source | Mean | Median | Std Dev | 25th % | 75th % | Min | Max |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| **Daily Total Steps** | Daily Activity ($N=940$) | 7,638 | 7,406 | 5,087 | 3,790 | 10,727 | 0 | 36,019 |
| **Total Distance (km)** | Daily Activity ($N=940$) | 5.49 | 5.24 | 3.92 | 2.62 | 7.71 | 0.00 | 28.03 |
| **Very Active Minutes** | Daily Activity ($N=940$) | 21.2 | 4.0 | 32.8 | 0.0 | 32.0 | 0.0 | 210.0 |
| **Fairly Active Minutes** | Daily Activity ($N=940$) | 13.6 | 6.0 | 20.0 | 0.0 | 19.0 | 0.0 | 143.0 |
| **Lightly Active Minutes**| Daily Activity ($N=940$) | 192.8 | 199.0 | 109.2 | 127.0 | 264.0 | 0.0 | 518.0 |
| **Sedentary Minutes** | Daily Activity ($N=940$) | 991.2 | 1,057.5 | 301.3 | 729.8 | 1,229.5 | 0.0 | 1,440.0 |
| **Calories Burned (kcal)**| Daily Activity ($N=940$) | 2,304 | 2,134 | 718 | 1,829 | 2,793 | 0 | 4,900 |
| **Minutes Asleep** | Sleep Records ($N=410$) | 419.2 | 432.5 | 118.6 | 361.0 | 490.0 | 58.0 | 796.0 |
| **Time in Bed (minutes)**| Sleep Records ($N=410$) | 458.5 | 463.0 | 127.5 | 403.8 | 526.0 | 61.0 | 961.0 |
| **Time Awake in Bed (min)**| Sleep Records ($N=410$) | 39.3 | 25.5 | 46.7 | 17.0 | 40.0 | 0.0 | 371.0 |
| **Sleep Efficiency (%)** | Sleep Records ($N=410$) | 91.6% | 94.3% | 8.7% | 91.2% | 96.1% | 49.8% | 100.0% |

---

## Actionable Business Recommendations

1. **Product Positioning for the Moderate Core (54% of Users):**
   - Position the **Bellabeat Leaf** as a daily lifestyle companion rather than an extreme athletic monitor. Tailor marketing copy to emphasize incremental gains (e.g., converting 6,500 daily steps into sustainable energy).
2. **Dynamic Weekly Notification Cadence:**
   - **Saturday Morning:** Trigger active outdoor prompts when user propensity to walk is highest.
   - **Sunday Evening:** Shift in-app messaging to recovery, guided meditation, and bedtime preparation to support sleep quality ahead of the workweek.
3. **Targeted Sleep Latency Support:**
   - Capitalize on the observed 39-minute average bedtime latency by introducing an automated **Wind-Down Mode** in the Bellabeat App, incorporating relaxing soundscapes and screen-time notifications.
4. **Sedentary Inactivity Nudges:**
   - Address the 991 average sedentary minutes per day by enabling customizable vibration reminders on the **Bellabeat Time** watch during working hours (09:00–17:00).

---

## Methodological Limitations

- **Sample Scale:** Dataset reflects tracking logs from 33 unique users (24 tracking sleep). Findings serve as directional behavioral hypotheses.
- **Demographic Context:** Raw logs do not include demographic or physiological variables (age, height, weight baseline, occupation), which may confound calorie and step relationships.
- **Causality:** Observed associations indicate correlational behavior and should be validated via controlled A/B feature experiments within the Bellabeat application.
