# Prometheus
### Build & Install 
##### Requirements
- [docker](https://www.docker.com/)
- [Go](https://golang.org/doc/install)

##### [Architecture](https://prometheus.io/docs/introduction/overview/#architecture)

![arch](https://prometheus.io/assets/architecture.svg)

##### Deploy (On Docker) 
- `$ docker run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml \
       prom/prometheus`
- `$ docker run -p 9090:9090 -v /prometheus-data \
       prom/prometheus -config.file=/prometheus-data/prometheus.yml`

##### Run a sample
- Load a sample
```
# Fetch the client library code and compile example.
git clone https://github.com/prometheus/client_golang.git
cd client_golang/examples/random
go get -d
go build

# Start 3 example targets in separate terminals:
./random -listen-address=:8080
./random -listen-address=:8081
./random -listen-address=:8082
```

- Make a config file located in `/tmp/prometheus.yml`
```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # Evaluate rules every 15 seconds.

  # Attach these extra labels to all timeseries collected by this Prometheus instance.
  external_labels:
    monitor: 'codelab-monitor'

rule_files:
  - 'prometheus.rules'

scrape_configs:
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name:       'example-random'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:8080', 'localhost:8081']
        labels:
          group: 'production'

      - targets: ['localhost:8082']
        labels:
          group: 'canary'
```
- Run
```
$ docker run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml \   prom/prometheus
```
## Build a sample prometheus client (python)
1. `pip install prometheus_client`
2. make a sample application
```
from prometheus_client import start_http_server, Summary
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
```
3.  Visit http://localhost:8000/ to view the metrics.
![]()
4.  Visit http://localhost:9090/ to visualize the metrics.
![]()

## Reference
- https://prometheus.io/docs/introduction/install/
- https://prometheus.io/docs/introduction/getting_started/
- https://prometheus.io/docs/introduction/getting_started/#configuring-prometheus-to-monitor-the-sample-targets
- https://prometheus.io/docs/introduction/getting_started/#starting-up-some-sample-targets

