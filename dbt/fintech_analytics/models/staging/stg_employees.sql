with source as (
    select *
    from {{ source('fintech_raw', 'employees') }}
),

renamed as (
    select
        cast(employee_id as string) as employee_id,
        cast(full_name as string) as full_name,
        cast(department_id as string) as department_id,
        cast(role as string) as role,
        cast(experience_level as string) as experience_level,
        cast(country as string) as country,
        cast(city as string) as city,
        safe_cast(employee_country_latitude as float64) as employee_country_latitude,
        safe_cast(employee_country_longitude as float64) as employee_country_longitude,
        safe_cast(hourly_rate_eur_hour as numeric) as hourly_rate_eur_hour
    from source
)

select *
from renamed
