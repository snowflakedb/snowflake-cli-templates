USE ROLE <! setup_role | upper !>;

CREATE OR REPLACE WAREHOUSE <! ( prefix ~ '_' ~ warehouse )| upper | replace('-', '_') !>;

CREATE OR REPLACE DATABASE <! ( prefix ~ '_' ~ database )| upper | replace('-', '_') !>;
CREATE OR REPLACE SCHEMA <! 'PUBLIC' if schema == 'PUBLIC' else ( prefix ~ '_' ~ schema )| upper | replace('-', '_') !>;
CREATE OR REPLACE STAGE <! ( prefix ~ '_' ~ stage )| upper | replace('-', '_') !>;

CREATE ROLE IF NOT EXISTS <! ( prefix ~ '_' ~ role )| upper | replace('-', '_') !>;
