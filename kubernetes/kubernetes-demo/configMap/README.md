###Create openhab-cfg
`kubectl create configmap openhab-cfg --from-file openhab.cfg`
- MQTT_IP in config is the same with EntryPoint of MQTT_service
###Create openhab-hpcc-items
`kubectl create configmap openhab-hpcc-items --from-file hpcc.items`
###Create openhab-hpcc-sitemap
`kubectl create configmap openhab-hpcc-sitemap --from-file hpcc.sitemap`
