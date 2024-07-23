#!/env/python3

###################################################################
# This script makes an API connection to OPNsense                 #
# and checks if there are any pending updates                     #
# if there are, it sends an email with details                    #
#                                                                 #
# Authors: Bart J. Smit, 'ObecalpEffect' and Franco Fichtner      #
#                                                                 #
# Version 1.2     07/05/2016                                      #
#                                                                 #
###################################################################

# import libraries
import json
import requests
import smtplib
import sys
from email.utils import formatdate
from os import environ

try:  
   api_key = environ["KEY"]
   api_secret = environ["SECRET"]
   host = environ["HOST"]
   recipients = environ["EMAIL"]
   rcpt_name = environ["NAME"]
except KeyError: 
   print("One or more environment variables not defined")
   sys.exit(1)

sender = environ["SENDER"] if 'SENDER' in environ else 'root@' + host
emailHost = environ["SMTP_HOST"] if 'SMTP_HOST' in environ else 'localhost'
port = environ["SMTP_PORT"] if 'SMTP_PORT' in environ else 25
username = environ["SMTP_USER"] if 'SMTP_USER' in environ else ''
password = environ["SMTP_PASS"] if 'SMTP_PASS' in environ else ''

# Check if username or password are defined.
# If one is defined, then the other must be as well.
# But if neither is defined, then that's fine.
if len(username) > 0 or len(password) > 0:
    if len(username) == 0 or len(password) == 0:
        print("SMTP username or password not defined")
        sys.exit(1)

# Require HTTPS verification by default
verify = True

# If VERIFY environment variable is set, and its value is anything other
# than "true", disable HTTPS verification
if 'VERIFY' in environ:
    verify = environ['VERIFY'] == 'true'
    

# If ALERT_NO_UPDATES is set to "true", then send an email even if there
# aren't any updates available.
# This is intended for testing purposes, to make sure the setup actually
# works before relying on it for update notifications.
alertNoUpdates = 'ALERT_NO_UPDATES' in environ and environ['ALERT_NO_UPDATES'] == 'true'


url = 'https://' + host + '/api/core/firmware/status'
message  = 'From: OPNsense Firewall <' + sender + '>\r\n'
message += 'To: ' + rcpt_name + '<' + recipients + '>\r\n'
message += 'MIME-Version: 1.0\r\n'
message += 'Content-Type: text/html\r\n'
message += 'Subject: Updates for OPNsense\r\n'
message += 'Date: ' + formatdate(localtime=True) + '\r\n'
message += '\r\n'

# request data
try:
    r = requests.post(url,verify=verify,auth=(api_key, api_secret))
except requests.exceptions.SSLError as e:
    print("SSL verification failed")
    print("Either set VERIFY=false, or trust your router's certificate")
    sys.exit(1)

if r.status_code == 200:
    response = json.loads(r.text)
    if response['status'] == 'ok':
        message += '<h2>Firewall Updates Available</h2>'
        message += '<br>The firewall has %s' % response['updates'] + ' update(s) available, totalling %s' % response['download_size'] + '<br>\r\n'
        nps = response['new_packages']
        if len(nps) > 0:
            message += '\r\n<br><b>New:</b><br>\r\n'
            if type(nps) == dict:
                for n in nps:
                    message += nps[n]['name'] + ' version ' + nps[n]['version'] + '<br>\r\n'
            else:
                for n in nps:
                    message += n['name'] + ' version ' + n['version'] + '<br>\r\n'
        ups = response['upgrade_packages']
        if len(ups) > 0:
            message += '\r\n<br><b>Upgrade:</b><br>\r\n'
            if type(ups) == dict:
                for u in ups:
                    message += ups[u]['name'] + ' from ' + ups[u]['current_version'] + ' to ' + ups[u]['new_version'] + '<br>\r\n'
            else:
                for u in ups:
                    message += u['name'] + ' from ' + u['current_version'] + ' to ' + u['new_version'] + '<br>\r\n'
        rps = response['reinstall_packages']
        if len(rps) > 0:
            message += '\r\n<br><b>Reinstall:</b><br>\r\n'
            if type(rps) == dict:
                for r in rps:
                    message += rps[r]['name'] + ' version ' + rps[r]['version'] + '<br>\r\n'
            else:
                for r in rps:
                    message += r['name'] + ' version ' + r['version'] + '<br>\r\n'
        message += '<br>Click <a href=\"https://' + host + '/ui/core/firmware/\">here</a> to fetch them.<br>\r\n'
        if response['upgrade_needs_reboot'] == '1':
            message += '<h3>This requires a reboot</h3>'
        else:
            pass # TODO auto apply
        s = smtplib.SMTP(emailHost, port)
        if len(username) > 0 and len(password) > 0:
            s.login(username, password)
        s.sendmail(sender,recipients,message)

    elif alertNoUpdates:

        message = "<p>No updates available</p>"

        # Append the time.
        # This is important for testing, since sending identical emails
        # can be interpreted as spam or an accident, resulting in non-delivery.
        message += "<p>Last checked at: "+formatdate(localtime=True)+"</p>"

        s = smtplib.SMTP(emailHost, port)
        if len(username) > 0 and len(password) > 0:
            s.login(username, password)
        s.sendmail(sender,recipients,message)

else:
    print('Connection / Authentication issue, response received:')
    print(r.text)
