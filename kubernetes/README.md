# Start kubenetes in a node
### Install docker-compose
[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Run command
```
docker-compose up
```

### Download kubelet(v1.3.6)
```
wget https://storage.googleapis.com/kubernetes-release/release/v1.3.6/bin/linux/amd64/kubelet
```

### Copy kubelet into $HOME_PATH
```
sudo cp kubelet /usr/local/sbin
```

### Run kubelet
```
sudo kubelet --api-servers=http://{MASTER_IP}:8080  --address=0.0.0.0 --enable-debugging-handlers=true --config=/etc/kubernetes/manifests --allow-privileged=False --v=2 --cluster-domain=cluster.local
```

# Download kubectl(v1.3.6)
```
curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.3.6/bin/linux/amd64/kubectl
```

### Provide permission for kubectl
```
sudo chmod +x kubectl
```

### Testing system
```
./kubectl get nodes
```

# Kubernetes notes

## Deploy on multinode
```
$ git clone https://github.com/kubernetes/kube-deploy.git
```

## Start kube-node

### Master
```
$ cd kube-deploy/docker-multinode
$ sudo ./master.sh
$ sudo curl -Lo /usr/local/bin/kubectl http://storage.googleapis.com/kubernetes-release/release/v1.3.6/bin/linux/amd64/kubectl && sudo chmod +x /usr/local/bin/kubectl
```

### Worker 
```
$ cd kube-deploy/docker-multinode
$ export MASTER_IP=${MASTER_IP}
$ sudo ./worker.sh
```

## Assign label for node
```
$ kubectl label nodes <node-name> <label-key>=<label-value>

```
## Config cluster name
```
$ kubectl config set-cluster fog-cluster --server=http://[MASTER_IP]:8080
$ kubectl config set-context fog-system --cluster=fog-cluster
$ kubectl config use-context fog-system
```

## Deploy components on fog 
```
$ git clone https://github.com/huanpc/heapster.git
$ kubectl create -f deploy/kube-config/influxdb/
$ kubectl create -f kube-config/mosquitto_mqtt/fog
```

## Deploy components on cloud
```
$ git clone https://github.com/huanpc/heapster.git
$ kubectl create -f deploy/kube-config/influxdb/
$ kubectl create -f kube-config/mosquitto_mqtt/cloud
```





