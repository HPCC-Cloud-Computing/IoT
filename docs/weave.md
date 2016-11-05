# Tutorial on using Weave Net for Docker networking
## Introducing Weave Net
 - From weaveworks:
 > Weave Net creates a virtual network that connects Docker containers across multiple hosts and enables their automatic discovery. With Weave Net, portable microservices-based applications consisting of multiple containers can run anywhere: on one host, multiple hosts or even across cloud providers and data centers. Applications use the network just as if the containers were all plugged into the same network switch, without having to configure port mappings, ambassadors or links.
Services provided by application containers on the weave network can be exposed to the outside world, regardless of where they are running. Similarly, existing internal systems can be opened to accept connections from application containers irrespective of their location..

![introducing](/images/weave_01.jpg)

### Instructions to run Weave Net
*Require Docker (version 1.6.0 or later)*
 1. Install
```bash
$ sudo curl -L git.io/weave -o /usr/local/bin/weave
$ sudo chmod a+x /usr/local/bin/weave
```
 2. Launching Weave Net
 - On `$HOST1` run:
```bash
host1$ sudo -s
host1$ weave launch
host1$ eval $(weave env)
host1$ docker run --name a1 -ti weaveworks/ubuntu
```
3. Creating Peer Connections Between Hosts
```bash
host2$ weave launch $HOST1
host2$ eval $(weave env)
host2$ docker run --name a2 -ti weaveworks/ubuntu
```
4. Testing Container Communications
 - From the container started on `$HOST1`
```bash
root@a1:/# ping -c 1 -q a2
PING a2.weave.local (10.40.0.2) 56(84) bytes of data.
--- a2.weave.local ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.341/0.341/0.341/0.000 ms
```
- Similarly, in the container started on `$HOST2`
```bash
root@a2:/# ping -c 1 -q a1
PING a1.weave.local (10.32.0.2) 56(84) bytes of data.
--- a1.weave.local ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.366/0.366/0.366/0.000 ms
```
