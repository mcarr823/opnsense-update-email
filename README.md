# opnsense-update-email

[![Docker Image amd64](https://github.com/mcarr823/opnsense-update-email/actions/workflows/docker-amd64.yml/badge.svg)](https://github.com/mcarr823/opnsense-update-email/actions/workflows/docker-amd64.yml)
[![Docker Image arm64](https://github.com/mcarr823/opnsense-update-email/actions/workflows/docker-aarch64.yml/badge.svg)](https://github.com/mcarr823/opnsense-update-email/actions/workflows/docker-aarch64.yml)

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
| SMTP_HOST | NO | IP or hostname of the SMTP server | localhost |
| SMTP_PORT | NO | Port on which the SMTP server is listening | 25 |
| SMTP_USER | NO | Username for authenticating requests to the SMTP server | |
| SMTP_PASS | NO | Password for authenticating requests to the SMTP server | |
| ALERT_NO_UPDATES | NO | If set to 'true', send an email even if there are no updates | |

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

## Docker

This program can also be run with docker.

Docker images are available for both amd64 and arm64/aarch64, with a different tag for each:
- :amd64
- :arm64

For example:

```
VERIFY=false \
KEY=xxx \
SECRET=xxx \
HOST=192.168.1.1 \
EMAIL=myemailaddress@test.com \
NAME=MyName \
docker run -it --rm \
-e VERIFY \
-e KEY \
-e SECRET \
-e HOST \
-e EMAIL \
-e NAME \
ghcr.io/mcarr823/opnsense-update-check:amd64
```

* Note that SMTP_HOST will likely need to be set to something other localhost, depending on the networking of the docker command.

ie. If you run the docker command without host networking, you'll likely need to use the SMTP server's external IP address and perhaps open up that port on the machine's firewall, even if this program and the SMTP server are on the same machine.

Alternatively, if both are running in docker containers, you can add them both to the same docker network.
