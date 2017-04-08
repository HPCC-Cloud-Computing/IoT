stt=1
## sleep in bash for loop ##
# create sensor item
for i in {1..6}
do
  kubectl delete configmap sensor-items-$i --namespace kube-system
  #sleep 1h
done
# create sensor config
for i in {1..6}
do
 kubectl delete configmap sensor-config-$i  --namespace kube-system
done
# create onem2m config
for i in {1..3}
do
  kubectl delete configmap onem2m-config-$i  --namespace kube-system
  #sleep 1h
done

# create openhab config
for i in {1..3}
do
 kubectl delete configmap openhab-cfg-$i --namespace kube-system
done
# create onem2m item
for i in {1..3}
do
  kubectl delete configmap onem2m-items-$i --namespace kube-system
done

# create openhab item
for i in {1..3}
do
  kubectl delete configmap openhab-items-$i --namespace kube-system
done
