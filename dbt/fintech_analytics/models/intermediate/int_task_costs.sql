with tasks as (
    select *
    from {{ ref('stg_tasks') }}
),

employees as (
    select *
    from {{ ref('stg_employees') }}
),

task_costs as (
    select
        tasks.task_id,
        tasks.project_id,
        tasks.assigned_to_employee_id,
        employees.department_id as employee_department_id,
        tasks.task_name,
        tasks.priority,
        tasks.task_status,
        tasks.planned_hours,
        tasks.actual_hours,
        employees.hourly_rate_eur_hour,
        safe_cast(tasks.planned_hours as numeric) * employees.hourly_rate_eur_hour as planned_labor_cost_eur,
        safe_cast(tasks.actual_hours as numeric) * employees.hourly_rate_eur_hour as actual_labor_cost_eur,
        tasks.actual_hours - tasks.planned_hours as hour_variance,
        (safe_cast(tasks.actual_hours as numeric) - safe_cast(tasks.planned_hours as numeric)) * employees.hourly_rate_eur_hour as labor_cost_variance_eur
    from tasks
    left join employees
        on tasks.assigned_to_employee_id = employees.employee_id
)

select *
from task_costs