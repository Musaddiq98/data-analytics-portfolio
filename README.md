# Data Analytics & Business Intelligence Portfolio

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-16a34a?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

An executive-ready portfolio of end-to-end data analytics and product intelligence case studies. Each project addresses a clearly defined business objective, implements robust data cleaning and validation rules, leverages scalable Python pipelines, and translates analytical discoveries into high-impact growth strategies.

---

## Featured Case Studies

| Project | Business Objective | Dataset & Scale | Tech Stack | Key Deliverables & Highlights |
|:---|:---|:---|:---|:---|
| **[Cyclistic Bike-Share Growth Analysis](projects/cyclistic-divvy-bike-share-analysis/)** | Convert casual riders into high-LTV annual members | **5.47M cleaned trips** (Divvy Chicago, 12-month rolling window) | Python, pandas, matplotlib, requests | • Chunked streaming pipeline (memory-safe)<br>• Bimodal commute vs. leisure diurnal curve<br>• Targeted commute-trial conversion experiments<br>• [Interactive Walkthrough Notebook](projects/cyclistic-divvy-bike-share-analysis/notebooks/cyclistic_analysis.ipynb) |
| **[Bellabeat Smart Wellness Analytics](projects/bellabeat-fitness-tracker-analysis/)** | Drive smart-device adoption & subscription retention | **Fitbit Activity & Sleep logs** (33 distinct users, 940 daily records) | Python, pandas, seaborn, matplotlib | • Grain separation: distinct user personas vs. daily variance<br>• "Saturday Surge & Sunday Recovery" lifecycle insight<br>• Sleep latency coaching & sedentary nudge strategies<br>• [Full Methodology & Visuals](projects/bellabeat-fitness-tracker-analysis/README.md) |

---

## Core Analytics Competencies Demonstrated

### 1. Data Engineering & Scalable Pipelines
- **Memory Optimization:** Designed a chunked streaming pipeline (200k rows/chunk) in Cyclistic to ingest and transform 5.47 million rows on commodity hardware without out-of-memory crashes.
- **Reproducible Automation:** Created CLI entry points (`--charts-only`, `--months N`) and source manifests for zero-friction reproducibility.

### 2. Rigorous Data Cleaning & Quality Assurance
- **Documented Exclusion Rules:** Cataloged timestamp anomalies, duration boundaries ($1\text{ min} \le t \le 24\text{ hrs}$), and unparseable records into auditable quality reports.
- **Methodological Integrity:** Identified and corrected classic analytical traps—such as confusing record rows with distinct users, sampling bias in join logic, and calculating statistics on categorical IDs.

### 3. Exploratory Data Analysis & Behavioral Segmentation
- **Diurnal & Seasonal Patterns:** Uncovered 8:00 AM / 5:00 PM weekday commuter spikes for Cyclistic members versus casual afternoon/weekend recreation.
- **Activity & Sleep Dynamics:** Established a $r = 0.59$ step-to-calorie expenditure rate and quantified an average 39-minute sleep latency gap for Bellabeat.

### 4. Business Strategy & Experimentation Design
- Formulated testable go-to-market strategies: personalized commute trial passes, dynamic price-comparison triggers, and weekend wind-down wellness messaging.
- Structured randomized control-group testing frameworks with primary conversion and guardrail retention metrics.

---

## Repository Architecture

```text
data-analytics-portfolio/
├── projects/
│   ├── bellabeat-fitness-tracker-analysis/
│   │   ├── data/                   # Input datasets (dailyActivity, sleepDay)
│   │   ├── docs/                   # Formatted summary statistics
│   │   ├── scripts/                # Production analysis script (analysis.py)
│   │   ├── visualizations/         # High-resolution charts
│   │   ├── requirements.txt
│   │   └── README.md               # Case study narrative & strategic findings
│   │
│   └── cyclistic-divvy-bike-share-analysis/
│       ├── data/
│       │   ├── source_urls.csv     # Live AWS S3 archive manifest
│       │   └── processed/          # Precomputed aggregates (for instant audit)
│       ├── notebooks/
│       │   └── cyclistic_analysis.ipynb  # Self-contained recruiter walkthrough
│       ├── reports/
│       │   ├── analysis_summary.md # Automated executive summary
│       │   └── figures/            # Visualizations (embedded in README)
│       ├── scripts/
│       │   └── run_analysis.py     # Chunked streaming data pipeline
│       ├── requirements.txt
│       └── README.md               # Case study narrative & conversion experiments
│
├── requirements.txt                # Unified portfolio dependencies
├── .gitignore                      # Clean git hygiene rules
└── README.md                       # Portfolio overview & index
```

---

## Quickstart: Reproduce in 3 Steps

All case studies are self-contained and reproducible with Python 3.11+:

```bash
# 1. Clone repository & create virtual environment
git clone https://github.com/Musaddiq98/data-analytics-portfolio.git
cd data-analytics-portfolio
python -m venv .venv

# 2. Activate virtual environment
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies & run any analysis
pip install -r requirements.txt

# Run Bellabeat Analysis
python projects/bellabeat-fitness-tracker-analysis/scripts/analysis.py

# Run Cyclistic Analysis (instant chart regeneration)
python projects/cyclistic-divvy-bike-share-analysis/scripts/run_analysis.py --charts-only
```

---

## Author & Contact

**Musaddiq**  
*Data Analyst | Business Intelligence & Analytics Engineer*  

- **GitHub:** [@Musaddiq98](https://github.com/Musaddiq98)  
- **Specialization:** Python, SQL, Tableau/PowerBI, Product Analytics, Experimentation  

---

## Data Licensing & Ethics Notice
The analyses utilize public datasets from the [Divvy Trips Public Data](https://divvybikes.com/data) (Lyft / City of Chicago) and [FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit) (Mobius / Kaggle). All data is strictly anonymized; no personal identity is tracked or inferred. Recommendations represent analytical hypotheses designed for portfolio demonstration.
