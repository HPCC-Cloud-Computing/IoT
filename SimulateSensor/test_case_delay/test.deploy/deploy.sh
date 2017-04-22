stt=1
## sleep in bash for loop ##
# create onem2m
for i in {1..5}
do
  kubectl create -f onem2m.deploy/onem2m_configmap_$i.yaml --namespace kube-system
  #sleep 1h
done

# create sensor
# kubectl create -f sensor.deploy/ --namespace kube-system


