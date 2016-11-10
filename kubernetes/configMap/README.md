###Create openhab-cfg
`kubectl create configmap openhab-cfg --from-file openhab.cfg`
###Create openhab-hpcc-items
`kubectl create configmap openhab-hpcc-items --from-file hpcc.items`
###Create openhab-hpcc-sitemap
`kubectl create configmap openhab-hpcc-sitemap --from-file hpcc.sitemap`
###Create om2m-middleware
kubectl create configmap om2m-middleware --from-file=om2m-middleware-env
###Create om2m-ipe-config
kubectl create configmap om2m-ipe-config --from-file=ipe_config


