# Tutorial on using CoreOS Flannel for Docker networking
## CoreOS
 + Lightweight OS based on Gentoo Linux
 + Has a distributed key-value store at the core
 + Read-only rootfs. Writeable /etc
   + All services are in containers
   
## Flannel Basic
 + One CIDR subnet per machine, like Kubernestes
 + No Docker port-based mapping
 + Containers reach each other through IP
 + Packets encapsulated using UDP, and soon VxLAN
 ![](https://raw.githubusercontent.com/huanpc/IoT-1/master/docs/images/flannel_01.png)
 
### Instructions to run Flannel
1. Build flannel on each host
```bash
$ git clone https://github.com/coreos/flannel.git
$ cd flannel
$ docker run -v `pwd`:/opt/flannel -it google/golang /bin/bash -c "cd /opt/flannel && ./build"
```
2. Set key in etcd for network config
```bash
$ curl -L http://127.0.0.1:4001/v2/keys/coreos.com/network/config -XPUT -d value='{
    "Network": "10.0.0.0/8",
    "SubnetLen": 20,
    "SubnetMin": "10.10.0.0",
    "SubnetMax": "10.99.0.0",
    "Backend": {
        "Type": "udp",
        "Port": 7890}}'
```
3. Start flannel
 - flanneld port created and route is set for the full flat IP range
```bash
$ sudo ./bin/flanneld &
```
4. Restart docker daemon with appropriate bridge IP
```bash
$ source /run/flannel/subnet.env
$ sudo ifconfig docker0 ${FLANNEL_SUBNET}
$ sudo docker -d --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU} &
```
### Testing Flannel Networking 
![Testing](https://raw.githubusercontent.com/huanpc/IoT-1/master/docs/images/flannel_02.jpg)
