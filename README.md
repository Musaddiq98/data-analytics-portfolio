# Data Analytics Engineering: Urban Mobility & Consumer Health Telemetry

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-16a34a?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

An analytics engineering repository containing end-to-end data pipelines, behavioral segmentation models, and executive analytics reports across urban mobility and consumer health domains.

---

## Analytics Projects

| Project | Domain / Objective | Dataset & Volume | Technical Stack | Core Deliverables |
|:---|:---|:---|:---|:---|
| **[Cyclistic Bike-Share Mobility Analytics](projects/cyclistic-divvy-bike-share-analysis/)** | Analyze subscriber vs. casual travel patterns to optimize membership conversion funnels | **5.47M validated trips** (Divvy Chicago, rolling 12-month window) | Python, pandas, matplotlib, requests | • Chunked memory-safe streaming ETL<br>• Diurnal commute vs. leisure distribution<br>• Data quality exclusion reporting<br>• [Interactive Analysis Notebook](projects/cyclistic-divvy-bike-share-analysis/notebooks/cyclistic_analysis.ipynb) |
| **[Bellabeat Consumer Health Analytics](projects/bellabeat-fitness-tracker-analysis/)** | Evaluate user activity intensities, caloric burn, and sleep latency to inform product strategy | **Fitbit Activity & Sleep telemetry** (33 unique users, 940 daily records) | Python, pandas, seaborn, matplotlib | • Persona disaggregation (users vs. daily logs)<br>• Saturday surge & Sunday recovery cycle<br>• Sleep latency & efficiency analysis<br>• [Technical Report & Findings](projects/bellabeat-fitness-tracker-analysis/README.md) |

---

## Engineering Standards

### 1. Scalable Ingestion & Memory Management
- **Streaming Pipeline:** The Cyclistic ingestion engine processes multi-gigabyte monthly trip data archives in 200,000-row chunks, maintaining constant memory overhead on commodity hardware.
- **Fast Execution Mode:** Precomputed aggregations allow instant figure generation and reporting (`--charts-only`) without re-downloading large remote archives.

### 2. Data Validation & Grain Disaggregation
- **Quality Assurance:** Automated validation of temporal consistency (`ended_at > started_at`), duration thresholding ($1\text{ min} \le t \le 24\text{ hrs}$), and segment classification.
- **Methodological Controls:** Prevents common analytical fallacies by distinguishing distinct user entities from record-level observation counts and avoiding survivor bias from premature inner joins.

### 3. Quantitative Insights & Statistical Modeling
- **Diurnal Commute Spikes:** Pinpointed 08:00 and 17:00 weekday demand peaks for annual members versus smooth afternoon curves for casual users.
- **Caloric Expenditure Linearity:** Derived a linear relationship ($r = 0.59$) correlating incremental step counts with active caloric burn.

---

## Repository Architecture

```text
data-analytics-portfolio/
├── projects/
│   ├── bellabeat-fitness-tracker-analysis/
│   │   ├── data/                   # Activity and sleep input tables
│   │   ├── docs/                   # Summary metric exports
│   │   ├── scripts/                # Analysis pipeline (analysis.py)
│   │   ├── visualizations/         # Publication-grade figures
│   │   ├── .gitignore              # Project-level ignore rules
│   │   ├── requirements.txt        # Subproject dependencies
│   │   └── README.md               # Technical whitepaper & findings
│   │
│   └── cyclistic-divvy-bike-share-analysis/
│       ├── data/
│       │   ├── source_urls.csv     # AWS S3 archive manifest
│       │   └── processed/          # Validated summary tables
│       ├── notebooks/
│       │   └── cyclistic_analysis.ipynb  # Executed analytical walkthrough
│       ├── reports/
│       │   ├── analysis_summary.md # Executive metric summary
│       │   └── figures/            # Visualizations (embedded in report)
│       ├── scripts/
│       │   └── run_analysis.py     # Streaming data pipeline
│       ├── .gitignore              # Project-level ignore rules
│       ├── requirements.txt        # Subproject dependencies
│       └── README.md               # Technical whitepaper & conversion strategy
│
├── requirements.txt                # Workspace dependencies
├── .gitignore                      # Repository git exclusions
└── README.md                       # Repository overview & index
```

---

## Environment Setup & Execution

### 1. Prerequisites & Virtual Environment

```bash
# Clone repository
git clone https://github.com/Musaddiq98/data-analytics-portfolio.git
cd data-analytics-portfolio

# Create and activate virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execution Commands

```bash
# Execute Bellabeat analysis pipeline
python projects/bellabeat-fitness-tracker-analysis/scripts/analysis.py

# Execute Cyclistic visualization pipeline (fast mode)
python projects/cyclistic-divvy-bike-share-analysis/scripts/run_analysis.py --charts-only
```

---

## Data Provenance & Ethics
All analyses rely on anonymized public datasets published by the [City of Chicago / Divvy](https://divvybikes.com/data) and [Fitbit / Kaggle](https://www.kaggle.com/datasets/arashnic/fitbit). No personally identifiable information (PII) is accessed or stored. Findings represent analytical modeling for commercial and product strategy.
