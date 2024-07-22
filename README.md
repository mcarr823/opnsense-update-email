# opnsense-update-email
Python script to check an OPNsense firewall for available updates and send an email if any are available

You can run this script by specifying the following environment variables:

| Variable         | Required         | Description | Default Value |
| :----------- | :--------------: | :------------------------- | :---- |
| VERIFY | NO | Require HTTPS verification  | True |
| KEY    | YES   | API key | |
| SECRET    | YES   | API secret | |
| HOST    | YES   | Email server. Hostname or IP address | |
| EMAIL    | YES   | Email alert recipient's email address | |
| NAME    | YES   | Name of the email recipient | |
| SENDER | NO | Email address from which to send the email | root@$HOST |

For example:

```
VERIFY=false \
KEY=xxx \
SECRET=xxx \
HOST=192.168.1.1 \
EMAIL=myemailaddress@test.com \
NAME=MyName \
python3 fw_update-1.2.py
```