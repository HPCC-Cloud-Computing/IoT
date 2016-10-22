###Run
Like the jobs it monitors, Prometheus runs as a pod in your Kubernetes cluster
- *run command:* `kubectl create -f https://raw.githubusercontent.com/coreos/blog-examples/master/monitoring-kubernetes-with-prometheus/prometheus.yml`
- *expose prometheus connection:* 
`kubectl get pods -l app=prometheus -o name | \
	sed 's/^.*\///' | \
	xargs -I{} kubectl port-forward {} 9090:9090`
