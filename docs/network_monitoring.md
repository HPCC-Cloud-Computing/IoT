# Monitor Weave Network with Prometheus
## Router Metrics
The endpoint address is `localhost:6782`
The following metrics are exposed:
- `weave_connections` – Number of peer-to-peer connections.
- `weave_connection_terminations_total` – Number of peer-to-peer connections terminated.
- `weave_ips` – Number of IP addresses.
- `weave_max_ips` – Size of IP address space used by allocator.
- `weave_dns_entries` – Number of DNS entries.
- `weave_flows` – Number of FastDP flows.

## Prometheus configuration for Weave Net
The following YAML fragment can be used to scrape the router metrics endpoint
```
scrape_configs:
- job_name: 'weave'
  scrape_interval: 15s
  static_configs:
  - targets: ['localhost:6782']
```

## Configuration for Kubernetes itegrating with Weave
The following Kubernetes config will install and configure Prometheus 1.3 on your cluster and configure it to discover and scrape the Weave endpoints
```
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus
data:
  prometheus.yml: |-
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'weave'
      kubernetes_sd_configs:
      - api_server:
        role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace,__meta_kubernetes_pod_label_name]
        action: keep
        regex: ^kube-system;weave-net$
      - source_labels: [__meta_kubernetes_pod_container_name,__address__]
        action: replace
        target_label: __address__
        regex: ^weave;(.+?)(?::\d+)?$
        replacement: $1:6782
      - source_labels: [__meta_kubernetes_pod_container_name,__address__]
        action: replace
        target_label: __address__
        regex: ^weave-npc;(.+?)(?::\d+)?$
        replacement: $1:6781
      - source_labels: [__meta_kubernetes_pod_container_name]
        action: replace
        target_label: job
---
apiVersion: v1
kind: Service
metadata:
  labels:
    name: prometheus
  name: prometheus
spec:
  selector:
    app: prometheus
  type: NodePort
  ports:
  - name: prometheus
    protocol: TCP
    port: 9090
    nodePort: 30900
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      name: prometheus
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:v1.3.0
        args:
          - '-config.file=/etc/prometheus/prometheus.yml'
        ports:
        - name: web
          containerPort: 9090
        volumeMounts:
        - name: config-volume
          mountPath: /etc/prometheus
      volumes:
      - name: config-volume
        configMap:
          name: prometheus
```
