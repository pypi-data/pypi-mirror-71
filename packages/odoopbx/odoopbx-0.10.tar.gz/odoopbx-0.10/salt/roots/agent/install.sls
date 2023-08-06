agent-install-pkgs:
  pkg.installed:
    - names:
      - python3-pip
      - python-pip
      - ipset
      - iptables
    - reload_modules: True

agent-install-self:
  pip.installed:
    - bin_env: /usr/bin/pip3
    - name: asterisk-odoo-agent
    - upgrade: True
    - require:
      - pkg: agent-install-pkgs
