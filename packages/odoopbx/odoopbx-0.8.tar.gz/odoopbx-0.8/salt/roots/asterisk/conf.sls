deploy-conf-files:
  file.recurse:
    - name: {{ pillar.asterisk.confdir }}
    - source: salt://files/addons/asterisk_base/deploy/etc/asterisk/
