# Cyclistic/Divvy analysis summary

**Trip-start window:** 2024-06 to 2025-06  
**Archive files processed:** 2024-07 to 2025-06  
**Cleaned trips analyzed:** 5,465,569  
**Rows excluded by documented rules:** 131,461

## What the data shows

| Rider type | Trips | Average ride (minutes) | Weekend share |
|---|---:|---:|---:|
| Casual | 1,982,411 | 20.6 | 37.0% |
| Member | 3,483,158 | 12.0 | 23.8% |

## Interpretation

Casual rides average **20.6 minutes**, versus **12.0 minutes** for members. Compare the monthly-volume and weekday-duration charts before deciding campaign timing; these descriptive results show behavior patterns, not why any individual purchased a pass.

## Recommended next experiments

1. Offer repeat weekend casual riders an in-app membership-value comparison after their second or third ride.
2. Test a spring/fall weekday-commute trial against a standard annual-membership offer.
3. Hold out a randomized control group and assess incremental conversion, retention, and contribution margin.

## Reproducibility notes

Source URLs are recorded in `data/source_urls.csv`. Quality counts, including invalid timestamps and duration-rule exclusions, are in `data/processed/data_quality_report.csv`. The pipeline uses no personally identifying fields.