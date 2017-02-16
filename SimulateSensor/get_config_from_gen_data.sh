#!/bin/bash
mkdir -p /openhab/configurations/items/
wget http://${SENSOR_GEN_HOST}:9090/sensor/description -O /openhab/configurations/items/demo_2.items