##Create MQTT replication controller
kubectl create -f mqtt_rc.yaml
##Create MQTT service
kubectl create -f mqtt_service.yaml
##Create OpenHab replication controller
kubectl create -f openhab.yaml
