# Cyclistic Bike-Share: Converting Casual Riders to Members

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-reproducible-16a34a)

## Portfolio summary

**Business question:** How do casual riders and annual members use Cyclistic bikes differently, and what can marketing do to convert casual riders to members?

This end-to-end analyst project uses the real public **Divvy** trip-data archive (the public data used for the fictional Cyclistic case study). It downloads a rolling 12-month window, cleans and validates the records in chunks, produces executive-ready visuals, and writes auditable CSV summaries.

> The repository contains code and small, reproducible outputs only. Raw trip files are intentionally excluded: they are large, refreshed by the publisher, and can be downloaded with one command.

## Executive findings to validate after running

1. Casual riders generally take longer, leisure-oriented rides and concentrate on weekends and warm-weather months.
2. Members contribute steadier weekday volume, consistent with commuting and routine trips.
3. The best conversion audience is repeat casual riders who ride on weekends or during seasonal peaks; a generic, year-round message is less targeted.

These are testable hypotheses, not claims about individual riders. Exact values are generated from the selected data window and appear in `reports/analysis_summary.md` after the pipeline runs.

## Recommendations

1. **Trigger a weekend conversion journey.** After a casual rider completes repeat weekend rides, show a mobile-first annual-membership offer that compares their recent pass spend with annual value.
2. **Launch a seasonal commuter trial.** During spring and fall, target casual riders with repeated weekday morning/evening trips using a 30-day membership trial and a clear commute-value message.
3. **Measure incrementally.** A/B test message, offer, and timing; use membership conversion, 30/90-day retention, and incremental margin as success metrics. Do not use trip data to infer personal identity or home address.

## Project structure

```text
cyclistic-divvy-portfolio/
├── data/
│   ├── source_urls.csv          # Live public-data manifest
│   ├── raw/                     # Downloaded ZIPs (gitignored)
│   └── processed/               # Aggregates (gitignored)
├── notebooks/
│   └── cyclistic_analysis.ipynb # Optional walkthrough notebook
├── reports/
│   ├── analysis_summary.md      # Generated result narrative
│   └── figures/                 # Generated charts
├── scripts/
│   └── run_analysis.py          # Download, clean, analyze, visualize
├── .gitignore
├── requirements.txt
└── README.md
```

## Reproduce the analysis

### 1. Create an environment and install packages

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### 2. Choose a 12-month window

`data/source_urls.csv` ships with July 2024-June 2025 - a stable, completed 12-month period. Replace the entries with newer monthly archive URLs from the source below whenever needed. Each URL follows this pattern:

```text
https://divvy-tripdata.s3.amazonaws.com/YYYYMM-divvy-tripdata.zip
```

### 3. Run

```bash
python scripts/run_analysis.py
```

Useful options:

```bash
# Validate the workflow on the first two months only
python scripts/run_analysis.py --months 2

# Reuse downloaded ZIPs
python scripts/run_analysis.py --skip-download

# Keep only rides from 1 minute to 24 hours (default)
python scripts/run_analysis.py --min-minutes 1 --max-hours 24
```

The script emits:

- `data/processed/monthly_member_summary.csv`
- `data/processed/day_member_summary.csv`
- `data/processed/rideable_member_summary.csv`
- `data/processed/data_quality_report.csv`
- `reports/analysis_summary.md`
- Three PNG charts in `reports/figures/`

## Data and ethics

The data is the [Divvy Trips public archive](https://divvy-tripdata.s3.amazonaws.com/index.html), published by Lyft/Divvy. The original Google Data Analytics case study identifies it as data made available by Motivate International Inc. Review the archive terms and [Divvy data terms](https://divvybikes.com/data) before reuse.

The dataset does not provide personally identifying rider fields. This project deliberately does **not** attempt to identify riders, infer where they live, or connect trips to purchases. Trip data indicates behavior, not causality: weather, pricing, availability, service changes, and missing station values may confound results.

## Cleaning rules

The analysis script documents row-level exclusions in `data_quality_report.csv`:

- harmonizes common legacy/current column names;
- keeps only `member` and `casual` rider types;
- parses timestamps and requires `ended_at > started_at`;
- removes rides shorter than 1 minute or longer than 24 hours by default;
- derives ride duration, weekday, month, hour, and weekday/weekend flags;
- aggregates in chunks so the 12-month data set does not need to fit into memory.

## Tools and skills demonstrated

Python, pandas, matplotlib, data cleaning, quality checks, reproducible pipelines, descriptive analysis, stakeholder communication, and ethical handling of public mobility data.

## LinkedIn-ready project description

> Built a reproducible Python analysis of public Divvy bike-share trips for the Cyclistic marketing case study. I created a chunked data pipeline to download, clean, validate, and aggregate a rolling 12-month dataset; visualized rider behavior by membership type, weekday, season, and bike type; and translated results into targeted membership-conversion experiments. The project includes documented data-quality rules, source lineage, and privacy-aware recommendations.

## Author

Replace this section with your name, LinkedIn URL, and portfolio URL before publishing.
