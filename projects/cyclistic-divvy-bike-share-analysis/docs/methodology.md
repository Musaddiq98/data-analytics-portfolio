# Methodology and data quality notes

## Analysis scope

The fictional Cyclistic case study asks how casual riders and annual members use bikes differently. This project operationalizes that question with four descriptive measures: trip volume, average trip duration, weekday/weekend mix, and bike-type mix.

## Source lineage

Every download URL and its archive month is recorded in `data/source_urls.csv`. The sources are public monthly ZIP archives from Divvy. The script never overwrites the manifest, so a reviewer can see exactly which files produced a run.

## Cleaning and validation

For every input row, the pipeline checks that both timestamps parse, rider type is `casual` or `member`, and duration falls between the configured limits (1 minute and 24 hours by default). The quality report gives the counts at the archive-month level. Data is processed in 200,000-row chunks and is summarized before the next chunk is read.

## Limits

- A trip archive can include a small number of rides that began in the preceding calendar month; all charts use the actual `started_at` month.
- Public trip data does not reveal a rider's identity, membership purchase history, demographics, marketing exposure, or reason for traveling.
- Associations in these summaries do not establish that a message or offer caused conversion.
- Station availability, weather, operational changes, and the selected duration bounds may affect observed patterns.

## Decision framework

Use the descriptive analysis to select plausible audience/timing hypotheses, then validate them with a randomized controlled experiment. Pre-register a primary conversion metric, retain a holdout group, and monitor longer-term retention and contribution margin as guardrails.
