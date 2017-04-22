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
##### Install CoreOS [ETCD](https://github.com/coreos/etcd/releases/)
###### Download and Run Etcd

```bash
$ ETCD_VER=v3.0.14
$ DOWNLOAD_URL=https://github.com/coreos/etcd/releases/download
$ curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o ~/etcd-${ETCD_VER}-linux-amd64.tar.gz
$ mkdir -p ~/test-etcd && tar xzvf ~/etcd-${ETCD_VER}-linux-amd64.tar.gz
$ ~/test-etcd/etcd --version
Git SHA: 8a37349
Go Version: go1.6.3
Go OS/Arch: linux/amd64
# start a local etcd server
$ ~/test-etcd/etcd

# write,read to etcd
$ ETCDCTL_API=3 /tmp/test-etcd/etcdctl --endpoints=localhost:2379 put foo "bar"
$ ETCDCTL_API=3 /tmp/test-etcd/etcdctl --endpoints=localhost:2379 get foo

# start etcd on multi host
# Assume that you have two Linux VM (or physical machine) with hostname node1/node2 and IP 192.168.236.130/131 seperately.
$ ~/test-etcd/etcd -name {node} -initial-advertise-peer-urls http://{NODE_IP}:2380 \
  -listen-peer-urls http://0.0.0.0:2380 \
  -listen-client-urls http://0.0.0.0:2379,http://127.0.0.1:4001 \
  -advertise-client-urls http://0.0.0.0:2379 \
  -initial-cluster-token etcd-cluster \
  -initial-cluster node1=http://192.168.236.130:2380,node2=http://192.168.236.131:2380 \
  -initial-cluster-state new
```
###### Config Etcd
Flannel reads its configuration from etcd. By default, it will read the configuration from `/coreos.com/network/config` (can be overridden via –etcd-prefix). You need to use etcdctl utility to set values in etcd.
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

##### Config Flannel
###### Download Flannel executed file
```
$ curl -L https://github.com/coreos/flannel/releases/download/v0.6.2/flanneld-amd64 -o ~/flanneld
```
###### Start flannel
Run flanneld on both nodes:
```bash
$ sudo ~/flanneld &
```
Use ifconfig to confirm the network of flanned was setup successfully, the outputs should be something like this:
```bash
flannel0  Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
          inet addr:10.15.240.0  P-t-P:10.15.240.0  Mask:255.0.0.0
          UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1472  Metric:1
          RX packets:606921 errors:0 dropped:0 overruns:0 frame:0
          TX packets:308311 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500
          RX bytes:893358516 (893.3 MB)  TX bytes:16225380 (16.2 MB)
```
After Flannel is running, you need to config network for docker0 and restart docker daemon with Flannel network configuration, execute commands as follows:
```bash
$ service docker stop
$ source /run/flannel/subnet.env
$ sudo ifconfig docker0 ${FLANNEL_SUBNET}
$ sudo docker daemon --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU} &
$ docker ps
```
### Testing Flannel Networking 
![Testing](https://raw.githubusercontent.com/huanpc/IoT-1/master/docs/images/flannel_02.jpg)

### UDP and VxLAN backends
There are two different backends supported by Flannel. The previous configuration uses UDP backend, which is a pretty slow solution because all the packets are encrypted in userspace. VxLAN backend uses Linux Kernel VxLAN support as well as some hardware features to achieve a much more faster network.

It’s easy to use VxLAN backend. When configuring Etcd, just define the backend block with vxlan.
```bash
$ curl -L http://127.0.0.1:4001/v2/keys/coreos.com/network/config -XPUT -d value='{
    "Network": "10.0.0.0/8",
    "SubnetLen": 20,
    "SubnetMin": "10.10.0.0",
    "SubnetMax": "10.99.0.0",
    "Backend": {
        "Type": "vxlan",
        "Port": 7890}}'
```
The native network performance between two hosts:
```bash
flannel@node2:~# iperf -c 192.168.236.130
------------------------------------------------------------
Client connecting to 192.168.236.130, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  3] local 192.168.236.131 port 54584 connected with 192.168.236.130 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  2.57 GBytes  2.21 Gbits/sec
```
With UDP backend, the iperf result of two containers on different hosts are as follows:
```bash
root@93c451432761:~# iperf -c 10.10.160.2
------------------------------------------------------------
Client connecting to 10.10.160.2, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  3] local 10.15.240.2 port 57496 connected with 10.10.160.2 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec   418 MBytes   351 Mbits/sec
```
With VxLAN backend, the iperf result of two containers on different hosts are as follows:
```bash
root@93c451432761:~# iperf -c 10.15.240.3
------------------------------------------------------------
Client connecting to 10.15.240.3, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  3] local 10.15.240.2 port 38099 connected with 10.15.240.3 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  1.80 GBytes  1.56 Gbits/sec
```

