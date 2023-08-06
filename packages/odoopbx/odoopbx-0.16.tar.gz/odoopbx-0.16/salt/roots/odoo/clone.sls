{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-clone:
  git.latest:
    - name: https://github.com/odoo/odoo.git
    - branch: {{ odoo.rev }}
    - rev: {{ odoo.rev }}
    - target: {{ odoo.srcdir }}
    - depth: 1
    - fetch_tags: False
