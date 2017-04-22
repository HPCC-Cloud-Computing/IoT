# Author: Cuong Nguyen
#
# Build: docker build -t cuongnb14/onfta_api:0.1 .
# Run: docker run -d -p 8080:8080 --name onfta_api cuongnb14/onfta_api:0.1 .
#

FROM ubuntu:16.04
MAINTAINER Huan Phan "nauh94@gmail.com"

RUN apt-get update -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip build-essential python3-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libmysqlclient-dev \
        libxml2-dev libxslt1-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libssl-dev libffi-dev

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

