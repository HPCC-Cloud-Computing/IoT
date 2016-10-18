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

## Reference
- https://prometheus.io/docs/introduction/install/
- https://prometheus.io/docs/introduction/getting_started/
- https://prometheus.io/docs/introduction/getting_started/#configuring-prometheus-to-monitor-the-sample-targets
- https://prometheus.io/docs/introduction/getting_started/#starting-up-some-sample-targets

