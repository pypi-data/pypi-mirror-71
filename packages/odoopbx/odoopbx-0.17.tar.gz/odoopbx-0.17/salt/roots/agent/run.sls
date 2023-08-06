{% import_yaml "agent/defaults.yaml" as defaults %}
{% set agent = salt['pillar.get']('agent', defaults.agent, merge=True) %}

systemd-reload:
  cmd.run:
   - name: systemctl --system daemon-reload
   - onchanges:  
     - file: agent-service
     - file: console-service

agent-service:
  file:
    - managed
    - name: /etc/systemd/system/asterisk-agent.service
    - source: salt://files/asterisk-odoo-agent/deploy/agent.service
    - template: jinja
    - context: {{ agent }}
  service:
    - {{ { True: 'running', False: 'dead'}[agent.enable] }}
    - name: asterisk-agent
    - enable: {{ agent.enable }}

console-service:
  file.managed:
    - name: /etc/systemd/system/asterisk-console.service
    - source: salt://files/asterisk-odoo-agent/deploy/console.service
    - template: jinja
    - mode: 0644
    - context: {{ agent }}
  service:
    - {{ { True: 'running', False: 'dead'}[agent.console.enable] }}
    - name: asterisk-console
    - enable: {{ agent.console.enable }}
