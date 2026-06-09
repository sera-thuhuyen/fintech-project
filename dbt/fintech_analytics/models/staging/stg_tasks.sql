with source as (
    select *
    from {{ source('fintech_raw', 'tasks') }}
),

renamed as (
    select
        cast(task_id as string) as task_id,
        cast(project_id as string) as project_id,
        cast(assigned_to_employee_id as string) as assigned_to_employee_id,
        cast(task_name as string) as task_name,
        safe_cast(planned_hours as int64) as planned_hours,
        safe_cast(actual_hours as int64) as actual_hours,
        cast(task_status as string) as task_status,
        cast(priority as string) as priority
    from source
)

select *
from renamed
