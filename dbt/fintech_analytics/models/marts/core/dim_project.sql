select
    project_id,
    product_name,
    department_id,
    project_manager_id,
    city,
    project_country_latitude,
    project_country_longitude,
    project_status,
    risk_level,
    planned_start_date,
    planned_end_date,
    actual_start_date,
    actual_end_date,
    project_country
from {{ ref('stg_projects') }}