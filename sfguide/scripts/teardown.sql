DROP WAREHOUSE IF EXIST <! ( prefix ~ '_' ~ warehouse )| upper | replace('-', '_') !>;

DROP DATABASE IF EXIST <! ( prefix ~ '_' ~ database )| upper | replace('-', '_') !>;

DROP ROLE IF EXISTS <! ( prefix ~ '_' ~ role )| upper | replace('-', '_') !>;
