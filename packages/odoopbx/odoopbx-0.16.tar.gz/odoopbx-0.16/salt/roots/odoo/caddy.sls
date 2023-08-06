caddy-odoopbx-config:
  file.managed:
    - name: /etc/caddy/Caddyfile.d/odoopbx.conf
    - source: salt://odoo/templates/caddy.conf
    - template: jinja
    - makedirs: True
    - watch_in:
      - service: caddy-service


