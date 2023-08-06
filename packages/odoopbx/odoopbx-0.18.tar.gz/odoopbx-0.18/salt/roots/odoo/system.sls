{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-account:
  user.present:
    - name: {{ odoo.user }}
    - shell: /bin/bash
    - home: {{ odoo.datadir }}
    - system: True

odoo-folders:
  file.directory:
    - names:
      - {{ odoo.logdir }}
      - {{ odoo.datadir }}
      - {{ odoo.confdir }}:
        - user: root
    - user: {{ odoo.user}}
    - makedirs: True
    - require:
      - user: odoo-account

odoo-configs:
  file.managed:
    - names:
      - {{ odoo.confdir }}/odoo.conf:
        - source: salt://odoo/templates/odoo.conf
        - user: {{ odoo.user }}
        - mode: 600
      - /etc/systemd/system/odoo.service:
        - source: salt://odoo/templates/odoo.service
    - user: root
    - mode: 644
    - template: jinja
    - context: {{ odoo }}
    - backup: minion
    - require:
      - file: odoo-folders

odoo-service:
  service:
    - {{ { True: 'running', False: 'dead'}[odoo.enable] }}
    - name: odoo
    - enable: {{ odoo.enable }}
    - require:
      - file: odoo-configs
    - watch:
      - file: {{ odoo.confdir }}/odoo.conf
