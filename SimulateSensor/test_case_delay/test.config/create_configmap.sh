stt=1
## sleep in bash for loop ##
# create sensor item
for i in {1..5}
do
  kubectl create configmap sensor-items-$i --from-file=sensor.items/items.$i.cfg --namespace kube-system
  #sleep 1h
done
# create sensor config
for i in {1..5}
do
 kubectl create configmap sensor-config-$i --from-file=sensor.config/config.$i.cfg --namespace kube-system
done
# create onem2m config
for i in {1..5}
do
  kubectl create configmap onem2m-config-$i --from-file=onem2m.config/config.$i.cfg --namespace kube-system
  #sleep 1h
done

# create onem2m item
for i in {1..5}
do
  kubectl create configmap onem2m-items-$i --from-file=onem2m.items/items.$i.cfg --namespace kube-system
done

