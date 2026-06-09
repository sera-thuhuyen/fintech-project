select
    employee_id,
    full_name,
    department_id,
    role,
    experience_level,
    country,
    city,
    employee_country_latitude,
    employee_country_longitude,
    hourly_rate_eur_hour
from {{ ref('stg_employees') }}