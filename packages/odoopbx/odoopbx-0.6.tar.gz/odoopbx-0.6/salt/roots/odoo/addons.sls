{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-addons-clone:
  git.latest:
    - name: git@gitlab.com:odoopbx/addons.git
    - branch: {{ odoo.rev }}
    - depth: 1
    - rev: {{ odoo.rev }}
    - target: {{ odoo.addons }}
    - identity: salt://files/id_rsa

odoo-addons-venv:
  virtualenv.manage:
    - venv_bin: pyvenv
    - name: {{ odoo.venv }}
    - requirements: {{ odoo.addons }}/requirements.txt
