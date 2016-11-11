#Start mqtt
##Start mqtt
`kubectl create -f mqtt_rc.yaml`
##Start mqtt_service
`kubectl create -f mqtt_service.yaml`

#Start openhab
`kubectl create -f openhab.yaml`

#Start oM2M
##Start oM2M core
`kubectl create -f om2m.yaml`
##Start oM2M service
`kubectl create -f om2m_service.yaml`
##Start oM2M webservice (middle-ware)
`kubectl create -f om2m_webservice.yaml`
