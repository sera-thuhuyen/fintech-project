with source as (
    select *
    from {{ source('fintech_raw', 'projects') }}
),

renamed as (
    select
        cast(project_id as string) as project_id,
        cast(product_name as string) as product_name,
        cast(department_id as string) as department_id,
        cast(project_manager_id as string) as project_manager_id,
        cast(city as string) as city,
        safe_cast(project_country_latitude as float64) as project_country_latitude,
        safe_cast(project_country_longitude as float64) as project_country_longitude,
        coalesce(safe.parse_date('%d/%m/%Y', cast(planned_start_date as string)), safe_cast(planned_start_date as date)) as planned_start_date,
        coalesce(safe.parse_date('%d/%m/%Y', cast(planned_end_date as string)), safe_cast(planned_end_date as date)) as planned_end_date,
        coalesce(safe.parse_date('%d/%m/%Y', cast(actual_start_date as string)), safe_cast(actual_start_date as date)) as actual_start_date,
        coalesce(safe.parse_date('%d/%m/%Y', cast(actual_end_date as string)), safe_cast(actual_end_date as date)) as actual_end_date,
        cast(status as string) as project_status,
        safe_cast(planned_budget_eur as numeric) as planned_budget_eur,
        safe_cast(actual_budget_eur as numeric) as actual_budget_eur,
        cast(risk_level as string) as risk_level,
        safe_cast(completion_percentage as int64) as completion_percentage,
        cast(project_country as string) as project_country
    from source
)

select *
from renamed
