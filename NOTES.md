- This sounds a lot like a typical [EAV](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model) structure
- Postgres EAV:
  - http://dba.stackexchange.com/questions/3492/optimizing-query-using-view-on-eav-structure
  - http://stackoverflow.com/questions/2224234/database-eav-pros-cons-and-alternatives
- Note: several posters mention using Postgres `hstore`: http://www.postgresql.org/docs/9.4/static/hstore.html

- SQLAlchemy
  - Declaritive:
    - http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/table_config.html#using-a-hybrid-approach-with-table
  - JOINS:
    - UNION:
      - http://stackoverflow.com/questions/24781611/creating-a-basic-table-with-flask-sqlalchemy
      - http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.union
    - FILTER:
      - http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter
      - http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter_by

- ORM to JSON:
  - https://marshmallow.readthedocs.org/en/latest/index.html

- MIGRATION COMMANDS:
  - python complion/manage.py db init
  - python complion/manage.py db migrate

- POSTGRESQL SQL QUERIES:
  - CREATE DB ctdms;
  - CREATE USER vagrant WITH PASSWORD 'ce!#ec4&!!eif7HS$!ya';
  - GRANT ALL ON DATABASE ctdms TO vagrant;
