from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "fin_data"
PROCESSED_DIR = DATA_DIR / "processed"

SOURCE_WORKBOOKS = {
    "Fintech Projects Dataset.xlsx": {
        "Projects": "projects",
        "Tasks": "tasks",
        "Milestones": "milestones",
        "Employees": "employees",
        "Departments": "departments",
    },
    "World Flags Dataset Addition.xlsx": {
        "Banderas": "country_flags",
    },
}


def standardize_column_name(column_name: object) -> str:
    """Convert Excel column names to BigQuery-friendly snake_case names."""
    name = str(column_name).strip()
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = name.lower()
    name = name.replace("&", " and ")
    name = name.replace("/", "_")
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")

    if not name:
        raise ValueError(f"Column name cannot be standardized: {column_name!r}")

    if name[0].isdigit():
        name = f"col_{name}"

    return name


def standardize_dataframe_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Rename DataFrame columns and return the original-to-standardized mapping."""
    column_mapping = {column: standardize_column_name(column) for column in df.columns}
    standardized_names = list(column_mapping.values())

    duplicated_names = sorted(
        {name for name in standardized_names if standardized_names.count(name) > 1}
    )
    if duplicated_names:
        raise ValueError(f"Duplicate standardized column names found: {duplicated_names}")

    return df.rename(columns=column_mapping), column_mapping


def extract_sheet_to_csv(workbook_path: Path, sheet_name: str, output_table_name: str) -> tuple[dict, list[dict]]:
    """Read one Excel sheet and export it as one BigQuery-friendly CSV file."""
    df = pd.read_excel(workbook_path, sheet_name=sheet_name, engine="openpyxl")
    df, column_mapping = standardize_dataframe_columns(df)

    output_path = PROCESSED_DIR / f"{output_table_name}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    manifest_row = {
        "source_workbook": workbook_path.name,
        "source_sheet": sheet_name,
        "output_table": output_table_name,
        "output_file": str(output_path.relative_to(PROJECT_ROOT)),
        "row_count": len(df),
        "column_count": len(df.columns),
    }

    mapping_rows = [
        {
            "source_workbook": workbook_path.name,
            "source_sheet": sheet_name,
            "output_table": output_table_name,
            "original_column_name": original_column,
            "standardized_column_name": standardized_column,
        }
        for original_column, standardized_column in column_mapping.items()
    ]

    return manifest_row, mapping_rows


def build_manifest(rows: list[dict]) -> pd.DataFrame:
    """Create a small manifest describing every extracted table."""
    return pd.DataFrame(rows).sort_values(["source_workbook", "source_sheet"])


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    column_mapping_rows = []
    for workbook_name, sheet_mapping in SOURCE_WORKBOOKS.items():
        workbook_path = DATA_DIR / workbook_name
        for sheet_name, output_table_name in sheet_mapping.items():
            manifest_row, mapping_rows = extract_sheet_to_csv(
                workbook_path=workbook_path,
                sheet_name=sheet_name,
                output_table_name=output_table_name,
            )
            manifest_rows.append(manifest_row)
            column_mapping_rows.extend(mapping_rows)

    manifest = build_manifest(manifest_rows)
    manifest_path = PROCESSED_DIR / "ingestion_manifest.csv"
    manifest.to_csv(manifest_path, index=False, encoding="utf-8")

    column_mapping = pd.DataFrame(column_mapping_rows).sort_values(
        ["source_workbook", "source_sheet", "original_column_name"]
    )
    column_mapping_path = PROCESSED_DIR / "column_mapping.csv"
    column_mapping.to_csv(column_mapping_path, index=False, encoding="utf-8")

    print(f"Extracted {len(manifest)} tables to: {PROCESSED_DIR}")
    print(f"Wrote ingestion manifest to: {manifest_path}")
    print(f"Wrote column mapping to: {column_mapping_path}")


if __name__ == "__main__":
    main()

