# Methodology and Data Quality Specifications

## Analysis Scope

This analysis evaluates how casual riders and annual subscribers utilize the municipal bicycle-sharing network differently. The investigation evaluates four primary quantitative dimensions: trip volume, ride duration, weekly cadence, and fleet mix.

## Source Lineage

Download endpoints and archive months are cataloged in `data/source_urls.csv`. The inputs are public monthly archives published by Divvy / Lyft. The script preserves the source manifest to ensure deterministic data lineage.

## Validation and Cleansing Pipeline

For every ingested row, the pipeline validates:
1. Parseability of start and end timestamps.
2. Chronological sequence (`ended_at > started_at`).
3. Rider classification (`member` or `casual`).
4. Duration thresholds ($1\text{ min} \le t \le 24\text{ hrs}$).

Quality counts are logged at the archive-month grain in `data/processed/data_quality_report.csv`. Data is transformed in 200,000-row streaming chunks to ensure constant memory utilization.

## Analytical Limitations

- Small volumes of trips beginning in the final hours of a calendar month appear in the following month's archive; records are classified by true `started_at` timestamps.
- Public trip logs do not contain demographic identifiers, residential locations, pricing tiers, or trip purpose.
- Observed patterns indicate behavioral correlations and should be tested via controlled experiments before broad commercial deployment.

## Decision Framework

Descriptive findings inform acquisition and conversion hypotheses. Proposed interventions should be deployed via randomized controlled trials with a designated holdout group, measuring 30-day conversion, 90-day retention, and net revenue contribution.
