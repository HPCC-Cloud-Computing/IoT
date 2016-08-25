# Tổng quan về việc chạy các thành phần Elasticsearch, Logstash, Kibana trên từng container riêng biệt

## Hướng dẫn chạy Elasticsearch container
  + Build docker image Elasticsearch bằng lệnh
    
      ```
      sudo docker build -t elasticsearch .
      ```
    Ngoài cách build thủ công còn có thể sử dụng image có sẵn trên docker hub: "elasticsearch" (một bản OFFICIAL REPOSITORY)
    
  + Chạy docker image Elasticsearch
    Sau khi build xong Docker image có thể chạy đơn giản bằng lệnh
    
    ```
    docker run -d -P elasticsearch
    ```
    Có thể sử dụng file cấu hình tùy biến (ví dụ /usr/share/elasticsearch/config) bằng lệnh 
    
    ```
    docker run -d -v "$PWD/config":/usr/share/elasticsearch/config elasticsearch
    ```
    
## Hướng dẫn chạy Kibana container

## Hướng dẫn chạy Logstash container
