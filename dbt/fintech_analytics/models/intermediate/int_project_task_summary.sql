with task_costs as (
    select *
    from {{ ref('int_task_costs') }}
),

project_task_summary as (
    select
        project_id,
        count(*) as task_count,
        countif(task_status = 'Completed') as completed_task_count,
        countif(task_status = 'In Progress') as in_progress_task_count,
        countif(task_status = 'On Hold') as on_hold_task_count,
        countif(task_status = 'Review Required') as review_required_task_count,
        sum(planned_hours) as planned_task_hours,
        sum(actual_hours) as actual_task_hours,
        sum(hour_variance) as task_hour_variance,
        sum(planned_labor_cost_eur) as planned_labor_cost_eur,
        sum(actual_labor_cost_eur) as actual_labor_cost_eur,
        sum(labor_cost_variance_eur) as labor_cost_variance_eur,
        safe_divide(sum(actual_hours), nullif(sum(planned_hours), 0)) as task_hour_efficiency_ratio
    from task_costs
    group by project_id
)

select *
from project_task_summary