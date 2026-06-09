# Power BI Dashboard Plan

## Data Source

Connect Power BI to BigQuery using the marts dataset:

```text
ecommerce-project-498012.fintech_dbt_marts
```

Recommended tables:

| Table | Purpose |
| --- | --- |
| `dim_project` | Project attributes: product, owner, status, risk, timeline, location. |
| `dim_department` | Department lookup and head of department. |
| `dim_employee` | Employee attributes: role, experience, location, hourly rate. |
| `fact_project_performance` | Project-level KPIs for budget, schedule, task, labor cost, and milestone performance. |
| `fact_task_performance` | Task-level KPIs for planned vs actual hours and labor cost. |
| `mart_executive_summary` | One-row summary for headline KPI cards. |

## Relationship Model

Use a star-schema style model with single-direction filtering from dimensions to facts.

| From | To | Cardinality | Filter Direction |
| --- | --- | --- | --- |
| `dim_project[project_id]` | `fact_project_performance[project_id]` | 1:* | Single |
| `dim_project[project_id]` | `fact_task_performance[project_id]` | 1:* | Single |
| `dim_employee[employee_id]` | `fact_task_performance[employee_id]` | 1:* | Single |
| `dim_employee[employee_id]` | `fact_project_performance[project_manager_id]` | 1:* | Single |
| `dim_department[department_id]` | `dim_project[department_id]` | 1:* | Single |
| `dim_department[department_id]` | `dim_employee[department_id]` | 1:* | Single |
| `dim_department[department_id]` | `fact_project_performance[department_id]` | 1:* | Single |

Avoid many-to-many relationships. If Power BI warns about ambiguous paths, keep direct dimension-to-fact relationships and disable redundant relationships where needed.

## Page 1: Executive Overview

Purpose: Give leadership a quick view of portfolio health.

Recommended visuals:

| Visual | Fields / Measures |
| --- | --- |
| KPI cards | Total Projects, Completed Projects, Avg Completion %, Over Budget Projects, Avg Schedule Delay Days |
| Clustered bar chart | Planned Budget vs Actual Budget by Department |
| Donut chart | Project count by Risk Level |
| Stacked bar chart | Project count by Project Status |
| Table | Top projects by Budget Variance EUR |

Recommended slicers:

- Department Name
- Risk Level
- Project Status
- Planned Start Date / Planned End Date

## Page 2: Project Performance

Purpose: Compare project delivery performance across budget, schedule, and completion.

Recommended visuals:

| Visual | Fields / Measures |
| --- | --- |
| Matrix | Product Name, Project Status, Completion %, Budget Variance EUR, Schedule Delay Days |
| Scatter chart | Completion % vs Budget Variance %, size by Actual Budget EUR, legend by Risk Level |
| Bar chart | Avg Schedule Delay Days by Department |
| Bar chart | Project count by Over Budget flag |
| Table | Projects with highest late_or_pending_milestone_count |

Recommended slicers:

- Department Name
- Risk Level
- Project Status
- Project Manager

## Page 3: Resource & Cost

Purpose: Analyze how employee allocation, hourly rate, and experience level influence task and labor cost performance.

Recommended visuals:

| Visual | Fields / Measures |
| --- | --- |
| KPI cards | Total Planned Labor Cost, Total Actual Labor Cost, Labor Cost Variance, Task Hour Efficiency Ratio |
| Bar chart | Actual Labor Cost by Department |
| Bar chart | Avg Hourly Rate by Experience Level |
| Matrix | Employee, Role, Experience Level, Planned Hours, Actual Hours, Labor Cost Variance |
| Scatter chart | Hourly Rate vs Actual Hours, legend by Experience Level |

Recommended slicers:

- Department Name
- Role
- Experience Level
- Task Priority

## Page 4: Task & Milestone Bottlenecks

Purpose: Identify operational bottlenecks and rework signals.

Recommended visuals:

| Visual | Fields / Measures |
| --- | --- |
| Stacked bar chart | Task Count by Task Status and Priority |
| Bar chart | On Hold Tasks by Department |
| Bar chart | Review Required Tasks by Department |
| Bar chart | Avg Milestone Delay Days by Department |
| Table | Projects with highest Task Hour Variance and Delayed Milestones |

Recommended slicers:

- Department Name
- Task Status
- Priority
- Risk Level

## Power BI Modeling Notes

- Use Import mode for this small portfolio dataset unless testing DirectQuery behavior is required.
- Hide technical ID fields from report view after relationships are configured.
- Format currency fields as EUR.
- Format percentage fields as percentage with one or two decimals.
- Use single-direction relationships unless a specific visual requires otherwise.
- Keep dashboard pages focused on business questions rather than showing every field.