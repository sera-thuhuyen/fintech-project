from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GCP_PROJECT_ID = "ecommerce-project-498012"
GCS_BUCKET_NAME = "sera-fintech-bucket"
GCS_RAW_CSV_PREFIX = "raw/csv"
BIGQUERY_RAW_DATASET = "fintech_raw"
BIGQUERY_LOCATION = "US"

TABLE_FILES = {
    "country_flags": "country_flags.csv",
    "departments": "departments.csv",
    "employees": "employees.csv",
    "milestones": "milestones.csv",
    "projects": "projects.csv",
    "tasks": "tasks.csv",
}

TABLE_SCHEMAS = {
    "country_flags": [
        ("country", "STRING"),
        ("alpha_code", "STRING"),
        ("flat_flag", "STRING"),
        ("shiny_flag", "STRING"),
        ("circle_flag", "STRING"),
    ],
    "departments": [
        ("department_id", "STRING"),
        ("department_name", "STRING"),
        ("head_of_department", "STRING"),
    ],
    "employees": [
        ("employee_id", "STRING"),
        ("full_name", "STRING"),
        ("department_id", "STRING"),
        ("role", "STRING"),
        ("experience_level", "STRING"),
        ("country", "STRING"),
        ("city", "STRING"),
        ("employee_country_latitude", "FLOAT"),
        ("employee_country_longitude", "FLOAT"),
        ("hourly_rate_eur_hour", "NUMERIC"),
    ],
    "milestones": [
        ("milestone_id", "STRING"),
        ("project_id", "STRING"),
        ("milestone_name", "STRING"),
        ("planned_completion_date", "STRING"),
        ("actual_completion_date", "STRING"),
        ("status", "STRING"),
    ],
    "projects": [
        ("project_id", "STRING"),
        ("product_name", "STRING"),
        ("department_id", "STRING"),
        ("project_manager_id", "STRING"),
        ("city", "STRING"),
        ("project_country_latitude", "FLOAT"),
        ("project_country_longitude", "FLOAT"),
        ("planned_start_date", "STRING"),
        ("planned_end_date", "STRING"),
        ("actual_start_date", "STRING"),
        ("actual_end_date", "STRING"),
        ("status", "STRING"),
        ("planned_budget_eur", "NUMERIC"),
        ("actual_budget_eur", "NUMERIC"),
        ("risk_level", "STRING"),
        ("completion_percentage", "INTEGER"),
        ("project_country", "STRING"),
    ],
    "tasks": [
        ("task_id", "STRING"),
        ("project_id", "STRING"),
        ("assigned_to_employee_id", "STRING"),
        ("task_name", "STRING"),
        ("planned_hours", "INTEGER"),
        ("actual_hours", "INTEGER"),
        ("task_status", "STRING"),
        ("priority", "STRING"),
    ],
}


def resolve_project_path(path_value: str | None) -> Path | None:
    """Resolve a user-provided path relative to the project root when needed."""
    if not path_value:
        return None

    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def build_gcs_uri(file_name: str) -> str:
    """Build the source GCS URI for one raw CSV file."""
    return f"gs://{GCS_BUCKET_NAME}/{GCS_RAW_CSV_PREFIX}/{file_name}"


def create_bigquery_client(credentials_file: Path | None):
    """Create a BigQuery client from a service account JSON or default credentials."""
    try:
        from google.cloud import bigquery
        from google.oauth2 import service_account
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Google Cloud Python packages. Run: "
            "pip install -r requirements.txt"
        ) from exc

    if credentials_file is None:
        return bigquery.Client(project=GCP_PROJECT_ID), bigquery

    if not credentials_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_file}")

    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    return bigquery.Client(project=GCP_PROJECT_ID, credentials=credentials), bigquery


def build_table_schema(bigquery, table_name: str):
    """Build an explicit BigQuery schema for one raw table."""
    return [
        bigquery.SchemaField(column_name, column_type)
        for column_name, column_type in TABLE_SCHEMAS[table_name]
    ]


def ensure_dataset(client, bigquery) -> None:
    """Create the raw dataset if it does not already exist."""
    dataset_id = f"{GCP_PROJECT_ID}.{BIGQUERY_RAW_DATASET}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = BIGQUERY_LOCATION
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset ready: {dataset_id}")


def load_table_from_gcs(client, bigquery, table_name: str, file_name: str) -> None:
    """Load one GCS CSV file into one BigQuery raw table."""
    table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_RAW_DATASET}.{table_name}"
    source_uri = build_gcs_uri(file_name)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=build_table_schema(bigquery, table_name),
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_uri(source_uri, table_id, job_config=job_config)
    load_job.result()

    destination_table = client.get_table(table_id)
    print(f"Loaded {destination_table.num_rows} rows into {table_id} from {source_uri}")


def load_all_tables(credentials_file: Path | None, dry_run: bool) -> None:
    """Load all fintech raw CSV files from GCS into BigQuery."""
    if dry_run:
        for table_name, file_name in TABLE_FILES.items():
            table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_RAW_DATASET}.{table_name}"
            schema_columns = ", ".join(column_name for column_name, _ in TABLE_SCHEMAS[table_name])
            print(f"DRY RUN: load {build_gcs_uri(file_name)} -> {table_id} ({schema_columns})")
        return

    client, bigquery = create_bigquery_client(credentials_file)
    ensure_dataset(client, bigquery)

    for table_name, file_name in TABLE_FILES.items():
        load_table_from_gcs(client, bigquery, table_name, file_name)

    print(f"BigQuery raw load complete: {GCP_PROJECT_ID}.{BIGQUERY_RAW_DATASET}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load fintech CSV files from GCS into BigQuery raw tables."
    )
    parser.add_argument(
        "--credentials-file",
        help="Path to a Google Cloud service account JSON key. Relative paths are resolved from project root.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print BigQuery load targets without loading tables.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    credentials_file = resolve_project_path(args.credentials_file)
    load_all_tables(credentials_file=credentials_file, dry_run=args.dry_run)


if __name__ == "__main__":
    main()