rabbitmq-server:
  pkg.installed


rabbitmq-service:
  service.running:
    - name: rabbitmq-server
    - enable: yes
    - require:
      - pkg: rabbitmq-server

