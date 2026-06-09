with source as (
    select *
    from {{ source('fintech_raw', 'departments') }}
),

renamed as (
    select
        cast(department_id as string) as department_id,
        cast(department_name as string) as department_name,
        cast(head_of_department as string) as head_of_department
    from source
)

select *
from renamed
