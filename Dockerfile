# Alpine used to make the image as small as possible.
FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add py3-pip

# Trying to install py3-requests and py3-urllib3 directly doesn't work.
# The packages get installed, but they can't be imported by the app.
# So let's install them through pip instead.
RUN pip install requests urllib3

# Copy the fw_update*.py script (and whatever else is inside this repo)
# into the container.
COPY . .

CMD [ "python3", "./fw_update-1.2.py" ]