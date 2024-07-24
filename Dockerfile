# Alpine used to make the image as small as possible.
FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add py3-pip

# Trying to install py3-requests and py3-urllib3 directly doesn't work.
# The packages get installed, but running them doesn't.
# So let's install them through pip instead.
RUN pip install requests urllib3

COPY . .

CMD [ "python3", "./fw_update-1.2.py" ]