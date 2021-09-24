FROM ghcr.io/nslythe/docker-base:latest

ARG UNIFI_VERSION=6.4.54

RUN apt-get update && apt-get install -y openjdk-8-jre-headless jsvc mongodb-server curl logrotate libcap2

ADD https://dl.ui.com/unifi/${UNIFI_VERSION}/unifi_sysvinit_all.deb /unifi.dep

RUN dpkg -i /unifi.dep

EXPOSE 3478/udp
EXPOSE 10001/udp
EXPOSE 8080
EXPOSE 8443
EXPOSE 1900/udp
EXPOSE 8843
EXPOSE 8880
EXPOSE 6789
EXPOSE 5514/udp

VOLUME /config

COPY root /
