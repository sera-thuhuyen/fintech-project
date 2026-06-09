with milestones as (
    select *
    from {{ ref('stg_milestones') }}
),

milestone_metrics as (
    select
        milestone_id,
        project_id,
        milestone_name,
        planned_completion_date,
        actual_completion_date,
        milestone_status,
        case
            when actual_completion_date is not null then date_diff(actual_completion_date, planned_completion_date, day)
            else null
        end as milestone_delay_days,
        case
            when actual_completion_date is not null and actual_completion_date <= planned_completion_date then true
            when milestone_status in ('Completed', 'Done') and actual_completion_date is null then null
            else false
        end as is_milestone_on_time
    from milestones
),

project_milestone_summary as (
    select
        project_id,
        count(*) as milestone_count,
        countif(milestone_status = 'Completed') as completed_milestone_count,
        countif(milestone_status = 'On Track') as on_track_milestone_count,
        countif(milestone_status = 'Delayed') as delayed_milestone_count,
        avg(milestone_delay_days) as avg_milestone_delay_days,
        max(milestone_delay_days) as max_milestone_delay_days,
        countif(is_milestone_on_time is true) as on_time_milestone_count,
        countif(is_milestone_on_time is false) as late_or_pending_milestone_count
    from milestone_metrics
    group by project_id
)

select *
from project_milestone_summary