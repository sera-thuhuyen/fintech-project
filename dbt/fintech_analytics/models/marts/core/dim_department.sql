select
    department_id,
    department_name,
    head_of_department
from {{ ref('stg_departments') }}