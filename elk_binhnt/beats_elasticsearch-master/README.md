# Tìm hiểu về Beats

## Giới thiệu tổng quan

  The Beats are open source data shippers that you install as agents on your servers to send different types of operational data to [Elasticsearch](https://github.com/nguyenvulebinh/elasticsearch). Beats can send data directly to Elasticsearch or send it to Elasticsearch via [Logstas](http://learn.elastic.co/logstash-intro)
  
  ![alt tag](https://github.com/nguyenvulebinh/beats_elasticsearch/blob/master/beats-platform.png)
  
  Elastic cung cấp 3 bản tùy biến của Beats bao gồm
  - Packetbeat: is a network packet analyzer that ships information about the transactions exchanged between your application servers
  - Topbeat: is a server monitoring agent that periodically ships system-wide and per-process statistics from your servers
  - Filebeat: ships log files from your servers.

Elastic cung cấp thư viện "libbeat" giúp tùy biến các chức năng của Beats theo miền ứng dụng nên ngoài 3 bản tùy biến trên, cộng đồng cũng đưa ra rất nhiều bản tùy biến khác nhau. Xem thêm ở link [1]
  
  
## Giới thiệu về Filebeat

  Filebeat là một chương trình mã nguồn mở, xây dựng dựa trên libbeat framework, đóng vai trò như một agent theo dõi những thư mục hoặc file log được chỉ định và gửi cho server mỗi khi có sự thay đổi trên file. Filebeat có thể gửi trự tiếp cho Elasticsearch để  index hoặc gửi cho Logstash để phân tích cú pháp sau đó mới gửi tới Elasticsearch để index

  ![alt tag](https://github.com/nguyenvulebinh/beats_elasticsearch/blob/master/filebeat.png)
  
  Trong kiến trúc của Filebeat, khi bắt đầu khởi động, mỗi thư mục sẽ được theo dõi bởi một prospectors, prospectors sẽ khởi tạo mỗi harvester tương ứng với một file để theo dõi sự thay đổi trên file này. Prospectors sẽ tổng hợp lại các sự kiện và nỗi dung thay đổi sau đó chuyển cho spooler để gửi ra ngoài.
  
## Cài đặt và sử dụng

  + **Cài đặt**
  
    Filebeat được sử dụng kết hợp với ELK stack (bao gồm các module Elasticsearch, Logstash, Kibana) nên trước khi cài đặt Filebeat cần thực hiện cài đặt các module này. Tham khảo tài liệu [2]  

    Sau khi cài đặt xong các module này ta thực hiện cài đặt Filebeat theo hướng dẫn [3]
    
    Cấu hình kết nối Filebeat tới Elasticsearch (file /etc/filebeat/filebeat.yml)
    
    ```
    # Configure what outputs to use when sending the data collected by the beat.
    # Multiple outputs may be used.
    output:
    ### Elasticsearch as output
    elasticsearch:
      # Array of hosts to connect to.
      hosts: ["192.168.1.42:9200"]
    ```
    Cấu hình kết nối Filebeat tới Logstash (Lưu ý phải comment phần cấu hình kết nối tới Elasticsearch trước)
    
    ```
    output:
    logstash:
    hosts: ["127.0.0.1:5044"]

    # Optional load balance the events between the Logstash hosts
    #loadbalance: true
    ```
    Cấu hình thư mục để  Filebeat theo dõi
    
    ```
    filebeat:
    # List of prospectors to fetch data.
    prospectors:
    # Each - is a prospector. Below are the prospector specific configurations
    # Paths that should be crawled and fetched. Glob based paths.
    # For each file found under this path, a harvester is started.
    paths:
      - "/var/log/*.log"
      #- c:\programdata\elasticsearch\logs\*

    # Type of the files. Based on this the way the file is read is decided.
    # The different types cannot be mixed in one prospector
    #
    # Possible options are:
    # * log: Reads every line of the log file (default)
    # * stdin: Reads the standard in
    input_type: log
    ```
    
    Cấu hình Template định dạng type và các trường của type để gửi lên Elasticsearch

    ```
    output:
    elasticsearch:
    hosts: ["localhost:9200"]

    # A template is used to set the mapping in Elasticsearch
    # By default template loading is disabled and no template is loaded.
    # These settings can be adjusted to load your own template or overwrite existing ones
    template:

      # Template name. By default the template name is filebeat.
      #name: "filebeat"

      # Path to template file
      path: "filebeat.template.json"

      # Overwrite existing template
      #overwrite: false
    ```
    
  + **Sử dụng** 
    
    Đơn giản chỉ việc start Filebeat lên và Filebeat sẽ tự động gửi log tới Elasticsearch 

    ```
    sudo /etc/init.d/filebeat start
    ```
    
    Khi đã khởi động Filebeat, ta có thể xem dữ liệu đã được gửi lên thành công chưa. Ta gửi request lên Elasticsearch. Lưu ý khi Filebeat gửi dữ liệu lên, index sẽ có định dạng là filebeat-*, * ở đây là định dạng ngày sẽ thay đổi theo từng ngày.
    
    ```
    curl -i -XGET 'http://localhost:9200/filebeat-*/log/_search?pretty'
    ```
  
    Ví dụ kết quả trả về sẽ như này
    
    ```
    {
      "took" : 5,
      "timed_out" : false,
      "_shards" : {
        "total" : 5,
        "successful" : 5,
        "failed" : 0
      },
      "hits" : {
        "total" : 2,
        "max_score" : 1.0,
        "hits" : [ {
          "_index" : "filebeat-2016.08.05",
          "_type" : "log",
          "_id" : "AVZbJacBpyT_MiMazAOT",
          "_score" : 1.0,
          "_source" : {
            "@timestamp" : "2016-08-05T14:40:05.463Z",
            "beat" : {
              "hostname" : "elk",
              "name" : "elk"
            },
            "count" : 1,
            "fields" : null,
            "input_type" : "log",
            "message" : "haha",
            "offset" : 53,
            "source" : "/var/log/nguyenbinh.log",
            "type" : "log"
          }
        }, {
          "_index" : "filebeat-2016.08.05",
          "_type" : "log",
          "_id" : "AVZbKsampyT_MiMazAOZ",
          "_score" : 1.0,
          "_source" : {
            "@timestamp" : "2016-08-05T14:45:40.510Z",
            "beat" : {
              "hostname" : "elk",
              "name" : "elk"
            },
            "count" : 1,
            "fields" : null,
            "input_type" : "log",
            "message" : "bobo",
            "offset" : 58,
            "source" : "/var/log/nguyenbinh.log",
            "type" : "log"
          }
        } ]
      }
    }

    ```
  
## Tài liệu tham khảo

[1] https://www.elastic.co/guide/en/beats/libbeat/current/community-beats.html

[2] https://www.elastic.co/guide/en/beats/libbeat/1.2/getting-started.html

[3] https://www.elastic.co/guide/en/beats/filebeat/1.2/filebeat-installation.html

