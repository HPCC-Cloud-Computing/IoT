FROM debian

## to build it
## sudo docker build -t debian-kura .
## to run it
## sudo docker run -i -t debian-kura -p 80:80 

##Them nguon jdk-8 Do mac dinh chua co

RUN echo "deb http://ftp.de.debian.org/debian jessie-backports main" >> /etc/apt/sources.list

## Cai dat cac goi phan mem can thiet
RUN apt-get update && \
    apt-get install -y apt-utils unzip ethtool dos2unix telnet bind9 hostapd isc-dhcp-server iw monit wget openjdk-8-jdk  wireless-tools && \
    rm -rf /var/lib/apt/lists/*

## Cai dat kura
RUN wget http://ftp.daumkakao.com/eclipse/kura/releases/2.0.0/kura_2.0.0_raspberry-pi-2_installer.deb
RUN dpkg -i kura_2.0.0_raspberry-pi-2_installer.deb

## Hack for ubuntu
RUN [ -f /lib/$(arch)-linux-gnu/libudev.so.0 ] || ln -sf /lib/$(arch)-linux-gnu/libudev.so.1 /lib/$(arch)-linux-gnu/libudev.so.0

## Bind cong 80 cua may chinh vao cong 5002 may chay kura
EXPOSE 80
EXPOSE 5002

