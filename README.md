# Fintech Project Delivery Analytics

## Project Overview

This project analyzes project delivery performance for a fintech company building payment products across Europe. The dataset tracks projects, tasks, milestones, employees, departments, budgets, schedules, and labor effort.

The goal is to build an end-to-end analytics workflow that helps answer:

- Which projects are at risk of delay or budget overrun?
- How do planned hours and costs compare with actual delivery?
- Which departments, roles, and experience levels drive labor cost?
- Where do task and milestone bottlenecks appear?
- Which metrics should leadership monitor in a Power BI dashboard?

This project is designed as a portfolio-ready data analytics engineering project using Python, Google Cloud Storage, BigQuery, dbt, and Power BI.

## Architecture

```text
Excel source files
    -> Python profiling and extraction
    -> Local CSV table files
    -> Google Cloud Storage raw/csv
    -> BigQuery raw tables
    -> dbt staging views
    -> dbt intermediate views
    -> dbt marts tables
    -> Power BI dashboard
```
Architecture documentation: [docs/architecture/data_architecture.md](docs/architecture/data_architecture.md)

## Tech Stack

| Tool | Role |
| --- | --- |
| Python | Excel extraction, profiling, GCS upload, BigQuery loading |
| pandas / openpyxl | Read Excel sheets and export CSV table files |
| Google Cloud Storage | Store raw CSV files before warehouse loading |
| BigQuery | Cloud data warehouse and SQL compute engine |
| dbt Core + dbt-bigquery | SQL transformation, data tests, model documentation |
| Power BI | Business dashboard and semantic reporting layer |
| Git / GitHub | Version control and portfolio presentation |

## Source Data

The source Excel files are stored in `fin_data/`:

| File | Description |
| --- | --- |
| `Fintech Projects Dataset.xlsx` | Main project management dataset with project, task, milestone, employee, and department sheets |
| `World Flags Dataset Addition.xlsx` | Country flag lookup data |

Each Excel sheet is treated as one source table.

## Project Structure

```text
fintech-project/
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ config/                  # GCP config notes and local config templates
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ dashboards/              # Power BI files and screenshots
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ dbt/fintech_analytics/   # dbt project
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ docs/                    # Architecture, KPI, and dashboard documentation
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ fin_data/                # Source data and generated local profiling/processed outputs
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ scripts/                 # Python ingestion and profiling scripts
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ artifacts/               # Generated non-source artifacts
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ notebooks/               # Optional exploratory notebooks
```

## Data Pipeline

### 1. Profile Source Data

```powershell
python scripts/profiling/profile_excel_data.py
```

Outputs:

```text
fin_data/profiling/column_profile.csv
fin_data/profiling/primary_key_checks.csv
fin_data/profiling/relationship_checks.csv
fin_data/profiling/data_profile_summary.md
```

Purpose: validate row counts, null values, primary keys, and table relationships before ingestion.

### 2. Extract Excel Sheets to CSV

```powershell
python scripts/ingestion/extract_excel_sheets.py
```

Outputs:

```text
fin_data/processed/projects.csv
fin_data/processed/tasks.csv
fin_data/processed/milestones.csv
fin_data/processed/employees.csv
fin_data/processed/departments.csv
fin_data/processed/country_flags.csv
fin_data/processed/ingestion_manifest.csv
fin_data/processed/column_mapping.csv
```

The extraction script standardizes column names into BigQuery-friendly `snake_case`.

### 3. Upload Processed CSV Files to GCS

```powershell
python scripts/ingestion/upload_processed_to_gcs.py --credentials-file config/service-account.json
```

Destination:

```text
gs://sera-fintech-bucket/raw/csv/
```

### 4. Load GCS CSV Files to BigQuery Raw Tables

```powershell
python scripts/ingestion/load_gcs_to_bigquery.py --credentials-file config/service-account.json
```

Destination dataset:

```text
ecommerce-project-498012.fintech_raw
```

Raw tables:

```text
country_flags
departments
employees
milestones
projects
tasks
```

The load script uses explicit BigQuery schemas instead of autodetect to keep field names and types stable.

## dbt Models

dbt project path:

```text
dbt/fintech_analytics
```

### Staging Layer

Materialized as views in:

```text
fintech_dbt_staging
```

Models:

```text
stg_projects
stg_tasks
stg_milestones
stg_employees
stg_departments
stg_country_flags
```

Purpose:

- Cast fields to stable data types
- Parse date strings
- Standardize naming
- Prepare raw tables for downstream business logic

### Intermediate Layer

Materialized as views in:

```text
fintech_dbt_intermediate
```

Models:

```text
int_task_costs
int_project_task_summary
int_project_milestone_summary
int_project_performance
```

Purpose:

- Calculate planned and actual labor cost
- Aggregate task status, hours, and cost by project
- Calculate milestone delay metrics
- Combine project, task, and milestone metrics into one performance model

### Marts Layer

Materialized as tables in:

```text
fintech_dbt_marts
```

Models:

```text
dim_department
dim_employee
dim_project
fact_project_performance
fact_task_performance
mart_executive_summary
dim_date
```

Purpose:

- Provide business-ready tables for Power BI
- Support star-schema relationships
- Improve dashboard performance and usability

## dbt Commands

Run from the dbt project folder:

```powershell
cd dbt\fintech_analytics
```

Validate connection:

```powershell
dbt debug --profiles-dir .
```

Run models:

```powershell
dbt run --select staging --profiles-dir .
dbt run --select intermediate --profiles-dir .
dbt run --select marts --profiles-dir .
```

Run tests:

```powershell
dbt test --select staging --profiles-dir .
dbt test --select intermediate --profiles-dir .
dbt test --select marts --profiles-dir .
```

Latest validation results:

| Layer | Command | Result |
| --- | --- | --- |
| Staging | `dbt run --select staging` | 6 passed |
| Staging | `dbt test --select staging` | 52 passed |
| Intermediate | `dbt run --select intermediate` | 4 passed |
| Intermediate | `dbt test --select intermediate` | 18 passed |
| Marts | `dbt run --select marts` | 6 passed |
| Marts | `dbt test --select marts` | 23 passed |

## Power BI Dashboard Plan

Power BI should connect to the BigQuery marts dataset:

```text
ecommerce-project-498012.fintech_dbt_marts
```

Recommended dashboard pages:

1. Executive Overview
2. Project Performance
3. Resource & Cost
4. Task & Milestone Bottlenecks

Documentation and design assets:

- `docs/powerbi_dashboard_plan.md`
- `docs/powerbi_implementation_checklist.md`
- `docs/data_dictionary/kpi_definitions.md`
- `docs/data_dictionary/powerbi_dax_measures.md`
- `dashboards/powerbi/powerbi_dashboard_design_spec.xlsx`

## Key KPIs

| KPI | Meaning |
| --- | --- |
| Budget Variance EUR | Actual budget minus planned budget |
| Budget Variance % | Budget variance relative to planned budget |
| Schedule Delay Days | Actual end date minus planned end date |
| Task Hour Variance | Actual task hours minus planned task hours |
| Task Hour Efficiency Ratio | Actual task hours divided by planned task hours |
| Labor Cost Variance EUR | Actual labor cost minus planned labor cost |
| Avg Milestone Delay Days | Average milestone slippage by project |
| Over Budget Projects | Count of projects where actual budget exceeds planned budget |

## Local Setup Notes

Use Python 3.12 for dbt compatibility.

```powershell
py -3.12 -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Do not commit real service account credentials. Store local credentials as:

```text
config/service-account.json
```

This file is ignored by `.gitignore`.

## Current Status

Completed:

- Project folder structure
- Source data profiling
- Excel-to-CSV extraction
- GCS upload script
- BigQuery raw load script with explicit schemas
- dbt staging, intermediate, and marts layers
- dbt tests for source, staging, intermediate, and marts models
- Power BI dashboard and KPI documentation

Next:

- Build Power BI report file
- Add dashboard screenshots to `dashboards/screenshots/`
- Add final architecture diagram
- Optionally add GitHub Actions scheduling later