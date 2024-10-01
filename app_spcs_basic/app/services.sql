-- namespace under which our services and their functions will live
create schema if not exists services;

-- namespace for service administration
create or alter versioned schema setup;

-- creates a compute pool, service, and service function
create or replace procedure setup.create_service(privileges ARRAY)
returns varchar
language sql
execute as owner
as $$
    begin
        let pool_name := (select current_database()) || '_app_pool';

        create compute pool if not exists identifier(:pool_name)
            MIN_NODES = 1
            MAX_NODES = 1
            INSTANCE_FAMILY = CPU_X64_XS;

        create service if not exists services.spcs_na_service
            in compute pool identifier(:pool_name)
            from spec='service_spec.yml';

        grant usage on service services.spcs_na_service
            to application role app_public;

        create or replace function services.echo(payload varchar)
            returns varchar
            service = services.spcs_na_service
            endpoint = 'my-endpoint'
            max_batch_rows = 50
            AS '/echo';

        grant usage on function services.echo(varchar)
            to application role app_public;

        return 'Done';
    end;
$$;
grant usage on procedure setup.create_service(ARRAY)
    to application role app_public;

create or replace procedure setup.suspend_service()
returns varchar
language sql
execute as owner
as $$
    begin
        alter service services.spcs_na_service suspend;
        return 'Done';
    end;
$$;
grant usage on procedure setup.suspend_service()
    to application role app_public;

create or replace procedure setup.resume_service()
returns varchar
language sql
execute as owner
as $$
    begin
        alter service services.spcs_na_service resume;
        return 'Done';
    end;
$$;
grant usage on procedure setup.resume_service()
    to application role app_public;

create or replace procedure setup.drop_service_and_pool()
returns varchar
language sql
execute as owner
as $$
    begin
        let pool_name := (select current_database()) || '_app_pool';
        drop service if exists services.spcs_na_service;
        drop compute pool if exists identifier(:pool_name);
        return 'Done';
    end;
$$;
grant usage on procedure setup.drop_service_and_pool()
    to application role app_public;

create or replace procedure setup.service_status()
returns varchar
language sql
execute as owner
as $$
    declare
        service_status varchar;
    begin
        call system$get_service_status('services.spcs_na_service') into :service_status;
        return parse_json(:service_status)[0]['status']::varchar;
    end;
$$;
grant usage on procedure setup.service_status()
    to application role app_public;

grant usage on schema setup to application role app_public;
