# Cyclistic / Divvy Analysis Summary: Executive Findings

- **Trip-Start Window Analyzed:** 2024-06 to 2025-06
- **Archive Files Processed:** 2024-07 to 2025-06
- **Cleaned Trips Analyzed:** 5,465,569
- **Rows Excluded by Documented Rules:** 131,461 (2.35% exclusion rate)

## Summary Metrics by Membership Type

| Rider Type | Total Cleaned Trips | Trip Share | Average Ride Duration | Weekend Share | Peak Travel Hour |
|:---|---:|---:|---:|---:|:---:|
| **Casual** | 1,982,411 | 36.3% | 20.6 mins | 37.0% | 17:00 |
| **Member** | 3,483,158 | 63.7% | 12.0 mins | 23.8% | 17:00 |

## Key Behavioral Insights

1. **Trip Duration Gap:** Casual trips average **20.6 minutes**—nearly **1.7x longer** than annual members (**12.0 minutes**), indicating casual usage is predominantly leisure and recreational.
2. **The Commuter Signature:** Annual members exhibit distinct bimodal volume peaks at **8:00 AM** and **5:00 PM** on weekdays, confirming reliable daily utility and commuter transit.
3. **Weekend & Seasonal Leisure Concentration:** Casual riders generate **37.0%** of their trips on weekends (vs. **23.8%** for members) and peak sharply during summer months (June–August).

## Recommended Conversion Experiments

1. **Weekend-to-Commute Trial:** Target casual riders who log 2+ weekend rides in summer with a limited-time 'Commute Free for 14 Days' trial in September to introduce weekday routine habits.
2. **Dynamic Price-Comparison Prompts:** Trigger in-app notifications after casual rides exceeding 25 minutes showing: *'You spent $X on this single trip. An annual membership costs just $Y/month for unlimited 45-minute rides.'*
3. **Rigorous A/B Testing:** Evaluate conversion, 90-day retention, and incremental margin against a randomized 10% holdout group before broad rollout.

## Visualizations Generated

- `reports/figures/monthly_ride_volume.png`: 12-month seasonality trends by rider type.
- `reports/figures/average_duration_by_day.png`: Weekday vs. weekend trip length comparisons.
- `reports/figures/hourly_ride_distribution.png`: 24-hour diurnal patterns showing commuter peaks.
- `reports/figures/bike_type_mix.png`: Classic vs. electric fleet adoption across groups.

## Reproducibility & Governance

- Manifest: `data/source_urls.csv` documents the exact archive URLs used.
- Quality Audit: Row-level exclusions are cataloged in `data/processed/data_quality_report.csv`.
- Ethics: All rider records are anonymized; no PII is stored or analyzed.