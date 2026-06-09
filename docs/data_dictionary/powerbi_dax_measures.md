# Power BI DAX Measures

Create a measure table first:

```DAX
Measures = DATATABLE("Measure Group", STRING, {{"Fintech Analytics"}})
```

Then create the following measures under the `Measures` table.

## Project Portfolio

```DAX
Total Projects =
DISTINCTCOUNT(fact_project_performance[project_id])
```

```DAX
Completed Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[project_status] = "Completed"
)
```

```DAX
In Progress Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[project_status] = "In Progress"
)
```

```DAX
Avg Completion % =
DIVIDE(
    AVERAGE(fact_project_performance[completion_percentage]),
    100
)
```

```DAX
Over Budget Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[is_over_budget] = TRUE()
)
```

```DAX
Over Budget Project % =
DIVIDE([Over Budget Projects], [Total Projects])
```

## Budget

```DAX
Total Planned Budget EUR =
SUM(fact_project_performance[planned_budget_eur])
```

```DAX
Total Actual Budget EUR =
SUM(fact_project_performance[actual_budget_eur])
```

```DAX
Budget Variance EUR =
[Total Actual Budget EUR] - [Total Planned Budget EUR]
```

```DAX
Budget Variance % =
DIVIDE([Budget Variance EUR], [Total Planned Budget EUR])
```

## Schedule

```DAX
Avg Schedule Delay Days =
AVERAGE(fact_project_performance[schedule_delay_days])
```

```DAX
Completed On Time Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[is_completed_on_time] = TRUE()
)
```

```DAX
Completed On Time % =
DIVIDE([Completed On Time Projects], [Completed Projects])
```

## Task Performance

```DAX
Total Tasks =
DISTINCTCOUNT(fact_task_performance[task_id])
```

```DAX
Completed Tasks =
SUM(fact_project_performance[completed_task_count])
```

```DAX
On Hold Tasks =
SUM(fact_project_performance[on_hold_task_count])
```

```DAX
Review Required Tasks =
SUM(fact_project_performance[review_required_task_count])
```

```DAX
Planned Task Hours =
SUM(fact_task_performance[planned_hours])
```

```DAX
Actual Task Hours =
SUM(fact_task_performance[actual_hours])
```

```DAX
Task Hour Variance =
[Actual Task Hours] - [Planned Task Hours]
```

```DAX
Task Hour Efficiency Ratio =
DIVIDE([Actual Task Hours], [Planned Task Hours])
```

## Labor Cost

```DAX
Total Planned Labor Cost EUR =
SUM(fact_task_performance[planned_labor_cost_eur])
```

```DAX
Total Actual Labor Cost EUR =
SUM(fact_task_performance[actual_labor_cost_eur])
```

```DAX
Labor Cost Variance EUR =
[Total Actual Labor Cost EUR] - [Total Planned Labor Cost EUR]
```

```DAX
Labor Cost Variance % =
DIVIDE([Labor Cost Variance EUR], [Total Planned Labor Cost EUR])
```

```DAX
Avg Hourly Rate EUR =
AVERAGE(dim_employee[hourly_rate_eur_hour])
```

## Milestones

```DAX
Total Milestones =
SUM(fact_project_performance[milestone_count])
```

```DAX
Completed Milestones =
SUM(fact_project_performance[completed_milestone_count])
```

```DAX
Delayed Milestones =
SUM(fact_project_performance[delayed_milestone_count])
```

```DAX
Avg Milestone Delay Days =
AVERAGE(fact_project_performance[avg_milestone_delay_days])
```

```DAX
Max Milestone Delay Days =
MAX(fact_project_performance[max_milestone_delay_days])
```