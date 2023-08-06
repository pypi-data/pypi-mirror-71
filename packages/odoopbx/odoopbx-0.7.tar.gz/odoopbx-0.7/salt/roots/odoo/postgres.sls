{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-postgres-user:
  postgres_user.present:
    - name: {{ odoo.user }}
    - createdb: True
    - encrypted: True
    - password: {{ odoo.dbpassword }}
    - db_user: postgres
