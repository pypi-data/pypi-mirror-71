{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-install-pkgs:
  pkg.installed:
    - pkgs:
      - git
      - python3-pip
      - build-essential
      - python3-dev
      - python3-venv
      - python3-wheel
      - python3-gevent
      - python3-greenlet
      - python3-eventlet
      - libxslt1-dev
      - libzip-dev
      - libldap2-dev
      - libsasl2-dev
      - python3-setuptools
      - node-less

odoo-venv:
  virtualenv.manage:
    - venv_bin: pyvenv
    - name: {{ odoo.venv }}
    - requirements: {{ odoo.srcdir }}/requirements.txt
    - require:
      - pkg: odoo-install-pkgs
      - git: odoo-clone 

