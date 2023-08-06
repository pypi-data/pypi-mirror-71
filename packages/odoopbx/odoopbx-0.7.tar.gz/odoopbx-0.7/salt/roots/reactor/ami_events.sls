{% if data.get('Event') in ['InvalidPassword', 'InvalidAccountID', 'ChallengeResponseFailed'] %}
ban_ip:
  #caller.asterisk.ban_event:
  caller.ipset.add:
    - args:
      #- event: data
      - setname: blacklist
      - entry: {{ data['RemoteAddress'].split('/')[2] }}
      - comment: Added by agent
{% endif %}

send_ami_event:
  caller.odoo.send_ami_event:
    - args:
      - event: {{ data }}
