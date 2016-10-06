#Start kubenetes in a node
###Install docker-compose
[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

###Run command
```
docker-compose up
```

###Download kubelet(v1.3.6)
```
wget https://storage.googleapis.com/kubernetes-release/release/v1.3.6/bin/linux/amd64/kubelet
```

###Copy kubelet into $HOME_PATH
```
sudo cp kubelet /usr/local/sbin
```

###Run kubelet
```
sudo kubelet --api-servers=http://{MASTER_IP}:8080  --address=0.0.0.0 --enable-debugging-handlers=true --config=/etc/kubernetes/manifests --allow-privileged=False --v=2 --cluster-domain=cluster.local
```

#Download kubectl(v1.3.6)
```
curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.3.6/bin/linux/amd64/kubectl
```

###Provide permission for kubectl
```
sudo chmod +x kubectl
```

###Testing system
```
./kubectl get nodes
```
