# KPI Definitions

This document defines the main KPIs used in the Fintech Project Delivery Analytics dashboard.

## Project Portfolio KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Total Projects | Count of distinct `project_id`. | `fact_project_performance` | Size of the active project portfolio. |
| Completed Projects | Count of projects where `project_status = 'Completed'`. | `fact_project_performance` | Delivery throughput. |
| Avg Completion % | Average of `completion_percentage`. | `fact_project_performance` | Overall portfolio progress. |
| Over Budget Projects | Count of projects where `is_over_budget = true`. | `fact_project_performance` | Number of projects exceeding planned budget. |
| On-Time Completed Projects | Count of projects where `is_completed_on_time = true`. | `fact_project_performance` | Number of completed projects delivered on or before planned end date. |

## Budget KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Planned Budget EUR | Sum of `planned_budget_eur`. | `fact_project_performance` | Expected project budget. |
| Actual Budget EUR | Sum of `actual_budget_eur`. | `fact_project_performance` | Actual spend recorded for projects. |
| Budget Variance EUR | `actual_budget_eur - planned_budget_eur`. | `fact_project_performance` | Positive value means project is over budget. |
| Budget Variance % | `(actual_budget_eur - planned_budget_eur) / planned_budget_eur`. | `fact_project_performance` | Relative budget overrun or underrun. |

## Schedule KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Schedule Delay Days | `actual_end_date - planned_end_date` for completed projects. | `fact_project_performance` | Positive value means the project finished late. |
| Avg Schedule Delay Days | Average of `schedule_delay_days`. | `fact_project_performance` | Average delivery delay for completed projects. |
| Completed On Time Flag | `actual_end_date <= planned_end_date`. | `fact_project_performance` | Indicates whether a completed project met its deadline. |

## Task KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Task Count | Count of `task_id`. | `fact_task_performance` | Total tasks in scope. |
| Completed Task Count | Count of tasks where `task_status = 'Completed'`. | `fact_project_performance` | Completed work volume. |
| On Hold Task Count | Count of tasks where `task_status = 'On Hold'`. | `fact_project_performance` | Potential workflow blockage. |
| Review Required Task Count | Count of tasks where `task_status = 'Review Required'`. | `fact_project_performance` | Potential rework or quality-control signal. |
| Planned Task Hours | Sum of `planned_hours`. | `fact_task_performance` | Expected workload. |
| Actual Task Hours | Sum of `actual_hours`. | `fact_task_performance` | Actual workload. |
| Task Hour Variance | `actual_hours - planned_hours`. | `fact_task_performance` | Positive value means tasks took longer than planned. |
| Task Hour Efficiency Ratio | `actual_hours / planned_hours`. | `fact_project_performance` | Ratio above 1 means actual hours exceeded planned hours. |

## Labor Cost KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Planned Labor Cost EUR | `planned_hours * hourly_rate_eur_hour`. | `fact_task_performance` | Expected labor cost by task. |
| Actual Labor Cost EUR | `actual_hours * hourly_rate_eur_hour`. | `fact_task_performance` | Actual labor cost by task. |
| Labor Cost Variance EUR | `actual_labor_cost_eur - planned_labor_cost_eur`. | `fact_task_performance` | Positive value means labor cost exceeded plan. |
| Avg Hourly Rate EUR | Average of `hourly_rate_eur_hour`. | `dim_employee` or `fact_task_performance` | Employee cost rate benchmark. |

## Milestone KPIs

| KPI | Definition | Source Table | Business Meaning |
| --- | --- | --- | --- |
| Milestone Count | Count of milestones per project. | `fact_project_performance` | Number of tracked delivery checkpoints. |
| Completed Milestone Count | Count of completed milestones. | `fact_project_performance` | Milestone delivery progress. |
| Delayed Milestone Count | Count of delayed milestones. | `fact_project_performance` | Delivery risk indicator. |
| Avg Milestone Delay Days | Average difference between actual and planned milestone completion date. | `fact_project_performance` | Average milestone slippage. |
| Max Milestone Delay Days | Maximum milestone delay per project. | `fact_project_performance` | Worst milestone delay for a project. |

## Suggested DAX Measures

```DAX
Total Projects = DISTINCTCOUNT(fact_project_performance[project_id])

Completed Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[project_status] = "Completed"
)

Over Budget Projects =
CALCULATE(
    DISTINCTCOUNT(fact_project_performance[project_id]),
    fact_project_performance[is_over_budget] = TRUE()
)

Total Planned Budget EUR = SUM(fact_project_performance[planned_budget_eur])

Total Actual Budget EUR = SUM(fact_project_performance[actual_budget_eur])

Budget Variance EUR =
[Total Actual Budget EUR] - [Total Planned Budget EUR]

Budget Variance % =
DIVIDE([Budget Variance EUR], [Total Planned Budget EUR])

Avg Completion % = AVERAGE(fact_project_performance[completion_percentage])

Avg Schedule Delay Days = AVERAGE(fact_project_performance[schedule_delay_days])

Total Planned Labor Cost EUR = SUM(fact_task_performance[planned_labor_cost_eur])

Total Actual Labor Cost EUR = SUM(fact_task_performance[actual_labor_cost_eur])

Labor Cost Variance EUR =
[Total Actual Labor Cost EUR] - [Total Planned Labor Cost EUR]

Task Hour Efficiency Ratio =
DIVIDE(
    SUM(fact_task_performance[actual_hours]),
    SUM(fact_task_performance[planned_hours])
)
```