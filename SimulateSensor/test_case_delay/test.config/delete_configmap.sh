stt=1
## sleep in bash for loop ##
# create sensor item
for i in {1..5}
do
  kubectl delete configmap sensor-items-$i --namespace kube-system
  #sleep 1h
done
# create sensor config
for i in {1..5}
do
 kubectl delete configmap sensor-config-$i  --namespace kube-system
done
# create onem2m config
for i in {1..5}
do
  kubectl delete configmap onem2m-config-$i  --namespace kube-system
  #sleep 1h
done


# create onem2m item
for i in {1..5}
do
  kubectl delete configmap onem2m-items-$i --namespace kube-system
done

