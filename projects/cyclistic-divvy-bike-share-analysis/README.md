# Cyclistic Bike-Share Mobility Analytics: Diurnal Commute Patterns & Membership Conversion

## Executive Summary

This study analyzes bicycle-sharing mobility patterns across **5.47 million validated trips** from the Divvy Chicago public bicycle network over a 12-month period (July 2024 – June 2025). The core objective is to analyze how usage patterns diverge between annual subscribers and casual riders, providing quantitative foundations for customer acquisition and membership conversion strategies.

---

## Data Architecture & Validation Pipeline

### 1. Data Provenance & Ingestion
- **Source:** Divvy public trip data archive published by Lyft / City of Chicago under municipal open-data licensing.
- **Scale:** 12 monthly compressed archives containing raw trip logs.
- **Pipeline Architecture:** Implements a memory-bounded streaming pipeline (`scripts/run_analysis.py`) that processes large-scale CSV extracts in 200,000-row chunks.

### 2. Grain Definition & Validation Rules
- **Data Grain:** The fundamental grain is the individual trip record identified by unique ride timestamps and start/end station identifiers.
- **Quality Assurance & Filtering:**
  - **Temporal Integrity:** Trips require non-null, valid timestamps with `ended_at > started_at`.
  - **Duration Boundaries:** Trips $< 1$ minute (potential false docks, immediate returns) and $> 24$ hours (lost, stolen, or improperly locked equipment) are excluded.
  - **Classification Verification:** Restricts analysis strictly to verified `member` and `casual` cohorts.
- **Audit Results:** Across 5,597,030 ingested records, 131,461 rows (2.35%) were excluded under these quality criteria, yielding **5,465,569 validated records**.

---

## Key Behavioral Findings & Visualizations

### 1. Diurnal Travel Dynamics: Commuter Rush vs. Leisure Demand
Trip frequency across the 24-hour diurnal cycle demonstrates distinct behavioral intent between the two cohorts.

![Hourly Ride Distribution](./reports/figures/hourly_ride_distribution.png)

- **Member Commute Utility:** Annual members exhibit pronounced bimodal demand peaks at **08:00 (246,681 trips)** and **17:00 (352,000+ trips)** on weekdays, validating bike-share as a core urban transit mode.
- **Casual Leisure Curve:** Casual riders follow an unimodal demand curve rising through the afternoon and peaking at **17:00**, with negligible morning commute volume.

---

### 2. Trip Duration Profiles
Trip lengths diverge significantly across user tiers and days of the week.

![Mean Duration by Day of Week](./reports/figures/average_duration_by_day.png)

- **Duration Asymmetry:** Casual trips average **20.6 minutes**, compared to **12.0 minutes** for annual members (a 1.7x duration ratio).
- **Weekend Expansion:** Casual ride durations expand from ~19.5 minutes on weekdays to **24.2 minutes on Sundays**, whereas member trip durations remain consistent (11.5–13.2 minutes) throughout the week.

---

### 3. Seasonality & Operational Resilience
Monthly ridership highlights strong weather sensitivity alongside an operational commuter floor.

![Monthly Trip Volume](./reports/figures/monthly_ride_volume.png)

- **Summer Peak:** Both segments peak between June and August (~450k monthly member trips; ~330k casual trips).
- **Winter Demand:** Casual volume contracts by over **85%** during sub-freezing months (December–February), whereas member volume sustains a baseline of over 120,000 monthly commuting trips.

---

### 4. Fleet Utilization & Vehicle Preferences
Ridership across Classic, Electric, and Docked bicycle configurations indicates operational preferences.

![Fleet Mix](./reports/figures/bike_type_mix.png)

- **Electric Fleet Adoption:** Electric bikes account for the highest volume across both user groups, delivering efficient transit across extended city distances.
- **Docked Bike Usage:** Legacy docked bikes are utilized almost exclusively by casual riders on long-duration journeys.

---

## Validated Summary Metrics

| Rider Tier | Validated Trips | Fleet Share | Mean Duration | Weekend Trip Share | Peak Travel Window |
|:---|---:|---:|---:|---:|:---:|
| **Casual Rider** | 1,982,411 | 36.3% | 20.6 minutes | 37.0% | 15:00 – 18:00 |
| **Annual Member** | 3,483,158 | 63.7% | 12.0 minutes | 23.8% | 08:00 & 17:00 |

---

## Strategic Interventions & Growth Campaigns

1. **Weekday Commute Bridge Campaign:**
   - **Target Audience:** Casual riders recording 2+ weekday trips during morning (07:00–09:00) or evening (16:30–18:30) peak hours.
   - **Offer:** A 14-day trial pass granting member pricing for rides up to 45 minutes, habituating daily transit use.
2. **Dynamic In-App Cost Comparison Prompts:**
   - For casual rides exceeding 20 minutes, deliver an immediate post-trip summary comparing unlock fees and per-minute overage charges against annual subscription rates.
3. **End-of-Summer Credit Rollover:**
   - In late August, allow casual pass holders to credit 100% of their cumulative seasonal pass expenditure toward an annual membership.

---

## Methodological Limitations

- **Aggregated Telemetry:** Public trip records do not contain individual user account keys, preventing multi-year longitudinal tracking of specific riders.
- **Exogenous Variables:** Weather events, municipal transit service disruptions, and road construction are not controlled for within the raw trip logs.
- **Experimental Verification:** Proposed acquisition funnels should be evaluated using randomized controlled holdout groups measuring 30-day conversion and 90-day retention.

---

## Pipeline Execution

```bash
# Option 1: Fast Execution (Uses precomputed summaries in data/processed/)
python scripts/run_analysis.py --charts-only

# Option 2: Full End-to-End Ingestion (Streams and processes raw AWS archives)
python scripts/run_analysis.py
```
