# Power BI Implementation Checklist
Dashboard design workbook:

```text
dashboards/powerbi/powerbi_dashboard_design_spec.xlsx
```

Use this workbook as a page-by-page wireframe before building visuals in Power BI.

Use this checklist to build the Power BI report from the BigQuery marts layer.

## 1. Connect To BigQuery

- Open Power BI Desktop.
- Select `Get Data` > `Google BigQuery`.
- Sign in with the Google account or service account flow available in your environment.
- Select project:

```text
ecommerce-project-498012
```

- Select dataset:

```text
fintech_dbt_marts
```

- Import these tables:

```text
dim_department
dim_employee
dim_project
fact_project_performance
fact_task_performance
mart_executive_summary
dim_date
```

Recommended mode: `Import` for this portfolio dataset.

## 2. Configure Relationships

Set relationship filter direction to `Single` unless a specific visual requires otherwise.

| From | To | Cardinality |
| --- | --- | --- |
| `dim_project[project_id]` | `fact_project_performance[project_id]` | 1:* |
| `dim_project[project_id]` | `fact_task_performance[project_id]` | 1:* |
| `dim_employee[employee_id]` | `fact_task_performance[employee_id]` | 1:* |
| `dim_employee[employee_id]` | `fact_project_performance[project_manager_id]` | 1:* |
| `dim_department[department_id]` | `dim_project[department_id]` | 1:* |
| `dim_department[department_id]` | `dim_employee[department_id]` | 1:* |
| `dim_department[department_id]` | `fact_project_performance[department_id]` | 1:* |

If Power BI reports ambiguous paths, keep the direct relationship needed for the visual and mark less-used relationships inactive.


Optional date relationships for slicers:

| From | To | Cardinality | Active? |
| --- | --- | --- | --- |
| `dim_date[date_day]` | `dim_project[planned_end_date]` | 1:* | Active if filtering by planned end date |
| `dim_date[date_day]` | `dim_project[planned_start_date]` | 1:* | Inactive |
| `dim_date[date_day]` | `dim_project[actual_end_date]` | 1:* | Inactive |

For the Executive Overview page, use `dim_date[year_month]` or `dim_date[date_day]` as the planned end date slicer. If Power BI creates ambiguous paths, keep only the `planned_end_date` relationship active.
## 3. Create Measure Table

Create an empty table for measures:

```DAX
Measures = DATATABLE("Measure Group", STRING, {{"Fintech Analytics"}})
```

Then add measures from:

```text
docs/data_dictionary/powerbi_dax_measures.md
```

## 4. Format Fields

Currency fields:

- `planned_budget_eur`
- `actual_budget_eur`
- `budget_variance_eur`
- `planned_labor_cost_eur`
- `actual_labor_cost_eur`
- `labor_cost_variance_eur`
- `hourly_rate_eur_hour`

Percentage fields:

- `budget_variance_pct`
- `completion_percentage`
- `task_hour_efficiency_ratio`

Date fields:

- `planned_start_date`
- `planned_end_date`
- `actual_start_date`
- `actual_end_date`

## 5. Build Report Pages

### Page 1: Executive Overview

Recommended visuals:

- KPI cards: Total Projects, Completed Projects, Avg Completion %, Over Budget Projects, Avg Schedule Delay Days
- Clustered bar: Planned vs Actual Budget by Department
- Donut: Projects by Risk Level
- Stacked bar: Projects by Status
- Table: Top projects by Budget Variance EUR

Slicers:

- Department Name
- Risk Level
- Project Status
- Planned End Date

### Page 2: Project Performance

Recommended visuals:

- Matrix: Product Name, Status, Completion %, Budget Variance, Schedule Delay
- Scatter: Completion % vs Budget Variance %, size by Actual Budget, legend by Risk Level
- Bar: Avg Schedule Delay Days by Department
- Bar: Over Budget Projects by Department
- Table: Projects with highest delayed milestones

Slicers:

- Department Name
- Project Manager
- Risk Level
- Project Status

### Page 3: Resource & Cost

Recommended visuals:

- KPI cards: Planned Labor Cost, Actual Labor Cost, Labor Cost Variance, Task Hour Efficiency Ratio
- Bar: Actual Labor Cost by Department
- Bar: Avg Hourly Rate by Experience Level
- Matrix: Employee, Role, Experience Level, Planned Hours, Actual Hours, Labor Cost Variance
- Scatter: Hourly Rate vs Actual Hours

Slicers:

- Department Name
- Role
- Experience Level
- Priority

### Page 4: Task & Milestone Bottlenecks

Recommended visuals:

- Stacked bar: Task Count by Task Status and Priority
- Bar: On Hold Tasks by Department
- Bar: Review Required Tasks by Department
- Bar: Avg Milestone Delay Days by Department
- Table: Projects with highest Task Hour Variance and Delayed Milestones

Slicers:

- Department Name
- Task Status
- Priority
- Risk Level

## 6. Export Portfolio Assets

Save the report file to:

```text
dashboards/powerbi/fintech_project_delivery_analytics.pbix
```

Export screenshots to:

```text
dashboards/screenshots/
```

Suggested screenshots:

```text
executive_overview.png
project_performance.png
resource_cost.png
task_milestone_bottlenecks.png
```

## 7. Update README

After screenshots are exported, update README with:

- Dashboard preview images
- Link to PBIX file path
- Short insight summary from the dashboard