from __future__ import annotations

import argparse
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "fin_data" / "processed"

GCP_PROJECT_ID = "ecommerce-project-498012"
GCS_BUCKET_NAME = "sera-fintech-bucket"
GCS_RAW_CSV_PREFIX = "raw/csv"

UPLOAD_FILES = [
    "country_flags.csv",
    "departments.csv",
    "employees.csv",
    "milestones.csv",
    "projects.csv",
    "tasks.csv",
]


def build_blob_name(file_name: str) -> str:
    """Build the destination object path inside the GCS bucket."""
    return f"{GCS_RAW_CSV_PREFIX}/{file_name}"


def resolve_project_path(path_value: str | None) -> Path | None:
    """Resolve a user-provided path relative to the project root when needed."""
    if not path_value:
        return None

    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def validate_local_files() -> list[Path]:
    """Return local CSV files to upload and fail fast if any expected file is missing."""
    missing_files = []
    local_files = []

    for file_name in UPLOAD_FILES:
        file_path = PROCESSED_DIR / file_name
        if file_path.exists():
            local_files.append(file_path)
        else:
            missing_files.append(file_path)

    if missing_files:
        missing_display = "\n".join(str(path) for path in missing_files)
        raise FileNotFoundError(f"Missing processed CSV files:\n{missing_display}")

    return local_files


def create_storage_client(credentials_file: Path | None):
    """Create a GCS client from a service account JSON or default credentials."""
    try:
        from google.cloud import storage
        from google.oauth2 import service_account
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Google Cloud Python packages. Run: "
            "pip install -r requirements.txt"
        ) from exc

    if credentials_file is None:
        return storage.Client(project=GCP_PROJECT_ID)

    if not credentials_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_file}")

    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    return storage.Client(project=GCP_PROJECT_ID, credentials=credentials)


def upload_files(credentials_file: Path | None, dry_run: bool) -> None:
    """Upload processed CSV files to the GCS raw CSV prefix."""
    local_files = validate_local_files()

    if dry_run:
        for local_file in local_files:
            destination_uri = f"gs://{GCS_BUCKET_NAME}/{build_blob_name(local_file.name)}"
            print(f"DRY RUN: upload {local_file} -> {destination_uri}")
        return

    client = create_storage_client(credentials_file)
    bucket = client.bucket(GCS_BUCKET_NAME)

    for local_file in local_files:
        blob_name = build_blob_name(local_file.name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file)
        print(f"Uploaded {local_file.name} -> gs://{GCS_BUCKET_NAME}/{blob_name}")

    print(f"Upload complete. Destination prefix: gs://{GCS_BUCKET_NAME}/{GCS_RAW_CSV_PREFIX}/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload processed fintech CSV files to Google Cloud Storage."
    )
    parser.add_argument(
        "--credentials-file",
        help="Path to a Google Cloud service account JSON key. Relative paths are resolved from project root.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print upload destinations without uploading files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    credentials_file = resolve_project_path(args.credentials_file)
    upload_files(credentials_file=credentials_file, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

