select
    task_id,
    project_id,
    assigned_to_employee_id as employee_id,
    employee_department_id,
    task_name,
    priority,
    task_status,
    planned_hours,
    actual_hours,
    hourly_rate_eur_hour,
    planned_labor_cost_eur,
    actual_labor_cost_eur,
    hour_variance,
    labor_cost_variance_eur,
    actual_hours > planned_hours as is_over_planned_hours
from {{ ref('int_task_costs') }}