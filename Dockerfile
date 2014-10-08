# cloudfleet mailbox
#
# VERSION 0.1

FROM ubuntu:14.04

ADD . /opt/cloudfleet/setup
RUN /opt/cloudfleet/setup/scripts/install.sh

CMD /opt/cloudfleet/setup/scripts/start.sh
