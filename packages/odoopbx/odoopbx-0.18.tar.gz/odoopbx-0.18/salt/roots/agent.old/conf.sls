{% import_yaml "agent/defaults.yaml" as defaults %}
{% set agent = salt['pillar.get']('agent', defaults.agent, merge=True) %}

{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

agent-conf-dir:
  file.directory:
    - name: {{ agent.confdir }}
    - makedirs: True
    - dir_mode: 0755
agent-conf-files:
  file.managed:
    - mode: 0644
    - names:
      - {{ agent.confdir }}/config.yml:
        - source: salt://files/asterisk-odoo-agent/deploy/config.yml
      - {{ agent.confdir }}/setup_security.sh:
        - source: salt://files/asterisk-odoo-agent/deploy/setup_security.sh
        - mode: 0755
      - {{ agent.confdir }}/setup_queuelog.py:
        - source: salt://files/asterisk-odoo-agent/deploy/setup_queuelog.py
        - mode: 0755
      - {{ agent.confdir }}/env:
        - source: salt://agent/env
        - backup: minion
        - mode: 0600
        - template: jinja
        - context:
           odoo: {{ odoo }}
           agent: {{ agent }}
