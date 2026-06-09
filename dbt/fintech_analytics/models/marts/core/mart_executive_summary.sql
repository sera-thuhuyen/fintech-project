with project_performance as (
    select *
    from {{ ref('fact_project_performance') }}
),

summary as (
    select
        count(*) as total_projects,
        countif(project_status = 'Completed') as completed_projects,
        countif(project_status = 'In Progress') as in_progress_projects,
        countif(is_over_budget) as over_budget_projects,
        countif(is_completed_on_time) as completed_on_time_projects,
        sum(planned_budget_eur) as total_planned_budget_eur,
        sum(actual_budget_eur) as total_actual_budget_eur,
        sum(budget_variance_eur) as total_budget_variance_eur,
        avg(budget_variance_pct) as avg_budget_variance_pct,
        avg(schedule_delay_days) as avg_schedule_delay_days,
        avg(completion_percentage) as avg_completion_percentage,
        sum(task_count) as total_tasks,
        sum(completed_task_count) as completed_tasks,
        sum(on_hold_task_count) as on_hold_tasks,
        sum(review_required_task_count) as review_required_tasks,
        sum(planned_labor_cost_eur) as total_planned_labor_cost_eur,
        sum(actual_labor_cost_eur) as total_actual_labor_cost_eur,
        sum(labor_cost_variance_eur) as total_labor_cost_variance_eur
    from project_performance
)

select *
from summary