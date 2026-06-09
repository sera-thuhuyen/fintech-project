with project_dates as (
    select planned_start_date as date_day from {{ ref('stg_projects') }} where planned_start_date is not null
    union all
    select planned_end_date as date_day from {{ ref('stg_projects') }} where planned_end_date is not null
    union all
    select actual_start_date as date_day from {{ ref('stg_projects') }} where actual_start_date is not null
    union all
    select actual_end_date as date_day from {{ ref('stg_projects') }} where actual_end_date is not null
),

milestone_dates as (
    select planned_completion_date as date_day from {{ ref('stg_milestones') }} where planned_completion_date is not null
    union all
    select actual_completion_date as date_day from {{ ref('stg_milestones') }} where actual_completion_date is not null
),

all_source_dates as (
    select date_day from project_dates
    union all
    select date_day from milestone_dates
),

date_bounds as (
    select
        date_trunc(min(date_day), month) as min_date,
        last_day(max(date_day), month) as max_date
    from all_source_dates
),

date_spine as (
    select date_day
    from date_bounds,
    unnest(generate_date_array(min_date, max_date, interval 1 day)) as date_day
),

final as (
    select
        date_day,
        extract(year from date_day) as year,
        extract(quarter from date_day) as quarter,
        extract(month from date_day) as month_number,
        format_date('%B', date_day) as month_name,
        format_date('%Y-%m', date_day) as year_month,
        date_trunc(date_day, week(monday)) as week_start_date,
        extract(dayofweek from date_day) as day_of_week_number,
        format_date('%A', date_day) as day_of_week_name,
        extract(day from date_day) as day_of_month,
        case when extract(dayofweek from date_day) in (1, 7) then true else false end as is_weekend
    from date_spine
)

select *
from final