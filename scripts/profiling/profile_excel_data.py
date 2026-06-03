from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "fin_data"
PROFILE_DIR = DATA_DIR / "profiling"

MAIN_WORKBOOK = DATA_DIR / "Fintech Projects Dataset.xlsx"
FLAGS_WORKBOOK = DATA_DIR / "World Flags Dataset Addition.xlsx"

MAIN_TABLES = ["Projects", "Tasks", "Milestones", "Employees", "Departments"]
FLAGS_TABLE = "Banderas"


PRIMARY_KEYS = {
    "Projects": "ProjectID",
    "Tasks": "TaskID",
    "Milestones": "MilestoneID",
    "Employees": "EmployeeID",
    "Departments": "Department_ID",
    "Banderas": "Alpha Code",
}

RELATIONSHIPS = [
    ("Projects", "DepartmentID", "Departments", "Department_ID"),
    ("Projects", "ProjectManagerID", "Employees", "EmployeeID"),
    ("Tasks", "ProjectID", "Projects", "ProjectID"),
    ("Tasks", "AssignedTo (EmployeeID)", "Employees", "EmployeeID"),
    ("Milestones", "ProjectID", "Projects", "ProjectID"),
    ("Employees", "DepartmentID", "Departments", "Department_ID"),
]


def read_workbooks() -> Dict[str, pd.DataFrame]:
    """Read each Excel sheet as one source table."""
    tables = pd.read_excel(MAIN_WORKBOOK, sheet_name=MAIN_TABLES, engine="openpyxl")
    flags = pd.read_excel(FLAGS_WORKBOOK, sheet_name=FLAGS_TABLE, engine="openpyxl")
    tables[FLAGS_TABLE] = flags
    return tables


def profile_columns(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for table_name, df in tables.items():
        for column_name in df.columns:
            series = df[column_name]
            rows.append(
                {
                    "table_name": table_name,
                    "column_name": column_name,
                    "data_type": str(series.dtype),
                    "row_count": len(df),
                    "null_count": int(series.isna().sum()),
                    "null_pct": round(float(series.isna().mean() * 100), 2),
                    "unique_count": int(series.nunique(dropna=True)),
                    "sample_values": sample_values(series),
                }
            )
    return pd.DataFrame(rows)


def sample_values(series: pd.Series, limit: int = 3) -> str:
    values = []
    for value in series.dropna().unique()[:limit]:
        values.append(str(value))
    return " | ".join(values)


def check_primary_keys(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for table_name, key_column in PRIMARY_KEYS.items():
        df = tables[table_name]
        null_count = int(df[key_column].isna().sum())
        duplicate_count = int(df[key_column].duplicated().sum())
        rows.append(
            {
                "table_name": table_name,
                "primary_key": key_column,
                "row_count": len(df),
                "null_key_count": null_count,
                "duplicate_key_count": duplicate_count,
                "status": "pass" if null_count == 0 and duplicate_count == 0 else "fail",
            }
        )
    return pd.DataFrame(rows)


def check_relationships(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for child_table, child_key, parent_table, parent_key in RELATIONSHIPS:
        child_values = set(tables[child_table][child_key].dropna().astype(str))
        parent_values = set(tables[parent_table][parent_key].dropna().astype(str))
        missing_values = sorted(child_values - parent_values)
        rows.append(
            {
                "child_table": child_table,
                "child_key": child_key,
                "parent_table": parent_table,
                "parent_key": parent_key,
                "missing_key_count": len(missing_values),
                "sample_missing_keys": " | ".join(missing_values[:5]),
                "status": "pass" if len(missing_values) == 0 else "fail",
            }
        )
    return pd.DataFrame(rows)



def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Render a small DataFrame as a Markdown table without extra dependencies."""
    if df.empty:
        return "No rows."

    columns = list(df.columns)
    rows = []
    rows.append("| " + " | ".join(columns) + " |")
    rows.append("| " + " | ".join(["---"] * len(columns)) + " |")

    for _, row in df.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if pd.isna(value):
                value = ""
            values.append(str(value).replace("|", "/"))
        rows.append("| " + " | ".join(values) + " |")

    return "\n".join(rows)

def build_markdown_report(
    tables: Dict[str, pd.DataFrame],
    column_profile: pd.DataFrame,
    primary_key_checks: pd.DataFrame,
    relationship_checks: pd.DataFrame,
) -> str:
    lines = [
        "# Fintech Project Data Profiling Report",
        "",
        "This report summarizes the source Excel tables before ingestion and dbt transformation.",
        "",
        "## Source Tables",
        "",
        "| Table | Rows | Columns |",
        "| --- | ---: | ---: |",
    ]

    for table_name, df in tables.items():
        lines.append(f"| {table_name} | {len(df)} | {len(df.columns)} |")

    lines.extend([
        "",
        "## Primary Key Checks",
        "",
        dataframe_to_markdown(primary_key_checks),
        "",
        "## Relationship Checks",
        "",
        dataframe_to_markdown(relationship_checks),
        "",
        "## Columns With Null Values",
        "",
    ])

    null_columns = column_profile[column_profile["null_count"] > 0].copy()
    if null_columns.empty:
        lines.append("No null values found.")
    else:
        lines.append(
            dataframe_to_markdown(null_columns[["table_name", "column_name", "data_type", "null_count", "null_pct", "sample_values"]])
        )

    return "\n".join(lines) + "\n"


def write_outputs(
    column_profile: pd.DataFrame,
    primary_key_checks: pd.DataFrame,
    relationship_checks: pd.DataFrame,
    markdown_report: str,
) -> None:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    column_profile.to_csv(PROFILE_DIR / "column_profile.csv", index=False)
    primary_key_checks.to_csv(PROFILE_DIR / "primary_key_checks.csv", index=False)
    relationship_checks.to_csv(PROFILE_DIR / "relationship_checks.csv", index=False)
    (PROFILE_DIR / "data_profile_summary.md").write_text(markdown_report, encoding="utf-8")


def main() -> None:
    tables = read_workbooks()
    column_profile = profile_columns(tables)
    primary_key_checks = check_primary_keys(tables)
    relationship_checks = check_relationships(tables)
    markdown_report = build_markdown_report(
        tables=tables,
        column_profile=column_profile,
        primary_key_checks=primary_key_checks,
        relationship_checks=relationship_checks,
    )
    write_outputs(column_profile, primary_key_checks, relationship_checks, markdown_report)
    print(f"Wrote profiling outputs to: {PROFILE_DIR}")


if __name__ == "__main__":
    main()

