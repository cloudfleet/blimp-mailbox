# cloudfleet mailbox
#
# VERSION 0.1

FROM ubuntu:14.04

RUN (apt-get update -y && apt-get install python-flask -y)

CMD ["python", "/opt/cloudfleet/app/mailbox/Mailbox.py"]

EXPOSE 3000
VOLUME /opt/cloudfleet/common/mails

ADD . /opt/cloudfleet/app
