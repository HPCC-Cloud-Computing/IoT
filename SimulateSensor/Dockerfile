FROM hardbyte/python3
MAINTAINER quanglys@gmail.com
COPY . "/SimulateSensor"
WORKDIR "/SimulateSensor"
RUN pip install -r requirements.txt
CMD [ "python", "/SimulateSensor/main.py" ]

#docker run -it -p 9090:9090 -v ${PWD}/config/config.cfg:/config/config.cfg sensor-simulator:0.2