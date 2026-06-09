with source as (
    select *
    from {{ source('fintech_raw', 'milestones') }}
),

renamed as (
    select
        cast(milestone_id as string) as milestone_id,
        cast(project_id as string) as project_id,
        cast(milestone_name as string) as milestone_name,
        coalesce(safe.parse_date('%d/%m/%Y', cast(planned_completion_date as string)), safe_cast(planned_completion_date as date)) as planned_completion_date,
        coalesce(safe.parse_date('%d/%m/%Y', cast(actual_completion_date as string)), safe_cast(actual_completion_date as date)) as actual_completion_date,
        cast(status as string) as milestone_status
    from source
)

select *
from renamed
