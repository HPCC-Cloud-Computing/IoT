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

# Install CoreOS [ETCD](https://github.com/coreos/etcd/releases/)
```bash
$ ETCD_VER=v3.0.14
$ DOWNLOAD_URL=https://github.com/coreos/etcd/releases/download
$ curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o 
$ /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
$ mkdir -p /tmp/test-etcd && tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C $ /tmp/test-etcd --strip-components=1

$ /tmp/test-etcd/etcd --version
Git SHA: 8a37349
Go Version: go1.6.3
Go OS/Arch: linux/amd64
# start a local etcd server
$ /tmp/test-etcd/etcd

# write,read to etcd
$ ETCDCTL_API=3 /tmp/test-etcd/etcdctl --endpoints=localhost:2379 put foo "bar"
$ ETCDCTL_API=3 /tmp/test-etcd/etcdctl --endpoints=localhost:2379 get foo
```

### Run in Docker
```bash
$ docker run --name etcd quay.io/coreos/etcd:v3.0.14
```


