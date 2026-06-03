from __future__ import annotations

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


def extract_sheet_to_csv(workbook_path: Path, sheet_name: str, output_table_name: str) -> dict:
    """Read one Excel sheet and export it as one CSV file."""
    df = pd.read_excel(workbook_path, sheet_name=sheet_name, engine="openpyxl")
    output_path = PROCESSED_DIR / f"{output_table_name}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return {
        "source_workbook": workbook_path.name,
        "source_sheet": sheet_name,
        "output_table": output_table_name,
        "output_file": str(output_path.relative_to(PROJECT_ROOT)),
        "row_count": len(df),
        "column_count": len(df.columns),
    }


def build_manifest(rows: list[dict]) -> pd.DataFrame:
    """Create a small manifest describing every extracted table."""
    return pd.DataFrame(rows).sort_values(["source_workbook", "source_sheet"])


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    for workbook_name, sheet_mapping in SOURCE_WORKBOOKS.items():
        workbook_path = DATA_DIR / workbook_name
        for sheet_name, output_table_name in sheet_mapping.items():
            manifest_rows.append(
                extract_sheet_to_csv(
                    workbook_path=workbook_path,
                    sheet_name=sheet_name,
                    output_table_name=output_table_name,
                )
            )

    manifest = build_manifest(manifest_rows)
    manifest_path = PROCESSED_DIR / "ingestion_manifest.csv"
    manifest.to_csv(manifest_path, index=False, encoding="utf-8-sig")

    print(f"Extracted {len(manifest)} tables to: {PROCESSED_DIR}")
    print(f"Wrote ingestion manifest to: {manifest_path}")


if __name__ == "__main__":
    main()
