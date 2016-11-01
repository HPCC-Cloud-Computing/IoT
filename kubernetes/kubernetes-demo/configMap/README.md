###Create openhab-cfg
`kubectl create configmap openhab-cfg --from-file openhab.cfg`
###Create openhab-hpcc-items
`kubectl create configmap openhab-hpcc-items --from-file hpcc.items`
###Create openhab-hpcc-sitemap
`kubectl create configmap openhab-hpcc-sitemap --from-file hpcc.sitemap`
