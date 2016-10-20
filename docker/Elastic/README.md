# Tổng quan về việc chạy các thành phần Elasticsearch, Logstash, Kibana trên từng container riêng biệt

## Hướng dẫn chạy Elasticsearch container
  + Build docker image Elasticsearch bằng lệnh
    
      ```
      #cd tới thư mục chứa dockerfile Elasticsearch
      docker build -t elasticsearch .
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
      #cd tới thư mục chứa dockerfile Kibana
      docker build -t kibana .
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
  + Build docker image Logstash bằng lệnh
    
      ```
      #cd tới thư mục chứa dockerfile Logstash
      docker build -t logstash .
      ```
    Ngoài cách build thủ công còn có thể sử dụng image có sẵn trên docker hub: "logstash" (một bản OFFICIAL REPOSITORY)

  + Chạy docker image Logstash
    Test thử xem docker image có hoạt động bình thường không bằng lệnh

    ```
    docker run -it --rm logstash -e 'input { stdin { } } output { stdout { } }'
    ```
    
    Để kết nối Logstash tới Elasticsearch ta thực hiện lệnh sau
    
    ```
    sudo docker run -it -v "$PWD":/mount logstash -f /mount/config
    ```
    Trong đó: 
      - $PWD lấy đường dẫn hiện tại của host, 
      - "/mount" mount đường dẫn hiện tại vào thư mục /mount của container
      - "-f /mount/config" lấy file config trong thư mục mount để làm file cấu hình cho logstash chạy. Trong file này sẽ định nghĩa vị trí của Elasticsearch
      
      Ví dụ file config sẽ có dạng
        ```
          input {
              file {
                  path => "/var/log/nguyenbinh.log"
              }
              beats {
                 port => "5044"
              }
          }
          filter {
              grok {
                  match => { "message" => "(idp %{DATA:idp} )([^\"]*)(idkv %{DATA:idkv} )([^\"]*)(idcum %{DATA:idcum} )([^\"]*)(nhietdo %{NUMBER:nhietdo:float})([^\"]*)(doam %{NUMBER:doam:float})([^\"]*)(nguoi |%{NUMBER:nguoi:int})"}
              }
          }
          output {
              elasticsearch {
                hosts => ["192.168.0.109:9200"]
              }
          }
        ```
