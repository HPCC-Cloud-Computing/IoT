stt=1
## sleep in bash for loop ##
for i in {1..10}
do
  kubectl create configmap sensor-config --from-file=config/config_$i.cfg --namespace kube-system
  sleep 1h
done
