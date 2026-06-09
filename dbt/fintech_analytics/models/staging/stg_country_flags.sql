with source as (
    select *
    from {{ source('fintech_raw', 'country_flags') }}
),

renamed as (
    select
        cast(country as string) as country,
        cast(alpha_code as string) as alpha_code,
        cast(flat_flag as string) as flat_flag_url,
        cast(shiny_flag as string) as shiny_flag_url,
        cast(circle_flag as string) as circle_flag_url
    from source
)

select *
from renamed
