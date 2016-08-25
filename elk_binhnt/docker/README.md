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
  + Build docker image Kibana bằng lệnh
    
      ```
      sudo docker build -t kibana .
      ```
    Ngoài cách build thủ công còn có thể sử dụng image có sẵn trên docker hub: "kibana" (một bản OFFICIAL REPOSITORY)
    
  + Chay docker image Kibana
    Chạy image Kibana bằng cách trỏ tới Docker container chạy Elasticsearch (ví dụ elegant_brahmagupta):
      
      ```
      sudo docker run --link elegant_brahmagupta:elasticsearch -d -p 5601:5601 kibana
      ```
    
    Ngoài ra có thể chạy Kibana image bằng cách trỏ tới địa chỉ ip của server chạy Elasticsearch:
      
      ```
      sudo docker run --name some-kibana -e ELASTICSEARCH_URL=http://some-elasticsearch:9200 -p 5601:5601 -d kibana
      ```

## Hướng dẫn chạy Logstash container
