with projects as (
    select *
    from {{ ref('stg_projects') }}
),

task_summary as (
    select *
    from {{ ref('int_project_task_summary') }}
),

milestone_summary as (
    select *
    from {{ ref('int_project_milestone_summary') }}
),

project_performance as (
    select
        projects.project_id,
        projects.product_name,
        projects.department_id,
        projects.project_manager_id,
        projects.city,
        projects.project_status,
        projects.risk_level,
        projects.completion_percentage,
        projects.planned_start_date,
        projects.planned_end_date,
        projects.actual_start_date,
        projects.actual_end_date,
        projects.planned_budget_eur,
        projects.actual_budget_eur,
        projects.actual_budget_eur - projects.planned_budget_eur as budget_variance_eur,
        safe_divide(projects.actual_budget_eur - projects.planned_budget_eur, nullif(projects.planned_budget_eur, 0)) as budget_variance_pct,
        case
            when projects.actual_end_date is not null then date_diff(projects.actual_end_date, projects.planned_end_date, day)
            else null
        end as schedule_delay_days,
        projects.actual_budget_eur > projects.planned_budget_eur as is_over_budget,
        case
            when projects.actual_end_date is null then null
            else projects.actual_end_date <= projects.planned_end_date
        end as is_completed_on_time,
        coalesce(task_summary.task_count, 0) as task_count,
        coalesce(task_summary.completed_task_count, 0) as completed_task_count,
        coalesce(task_summary.in_progress_task_count, 0) as in_progress_task_count,
        coalesce(task_summary.on_hold_task_count, 0) as on_hold_task_count,
        coalesce(task_summary.review_required_task_count, 0) as review_required_task_count,
        task_summary.planned_task_hours,
        task_summary.actual_task_hours,
        task_summary.task_hour_variance,
        task_summary.planned_labor_cost_eur,
        task_summary.actual_labor_cost_eur,
        task_summary.labor_cost_variance_eur,
        task_summary.task_hour_efficiency_ratio,
        coalesce(milestone_summary.milestone_count, 0) as milestone_count,
        coalesce(milestone_summary.completed_milestone_count, 0) as completed_milestone_count,
        coalesce(milestone_summary.on_track_milestone_count, 0) as on_track_milestone_count,
        coalesce(milestone_summary.delayed_milestone_count, 0) as delayed_milestone_count,
        milestone_summary.avg_milestone_delay_days,
        milestone_summary.max_milestone_delay_days,
        coalesce(milestone_summary.on_time_milestone_count, 0) as on_time_milestone_count,
        coalesce(milestone_summary.late_or_pending_milestone_count, 0) as late_or_pending_milestone_count
    from projects
    left join task_summary
        on projects.project_id = task_summary.project_id
    left join milestone_summary
        on projects.project_id = milestone_summary.project_id
)

select *
from project_performance