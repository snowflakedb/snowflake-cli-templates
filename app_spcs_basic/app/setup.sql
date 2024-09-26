create application role if not exists app_public;
execute immediate from './services.sql';
