# Tìm hiểu về Logstash

##Tổng quan

  Logstash là một "Open source data collection engine". Nó có chức năng thu thập dữ liệu từ các nguồn khác nhau một cách tự động, real-time và chuẩn hóa đống dữ liệu này nhằm mục đích lưu trữ, thống kê, phân tích....
  
  ![alt tag](https://github.com/nguyenvulebinh/logstash/blob/master/logstash.png)
  
  
##Cài đặt và demo
  
  + **Cài đặt**

    Làm theo hướng dẫn tài liệu [1]. 
  
    Lưu ý nếu như đên bước chạy lệnh "sudo apt-get update && sudo apt-get install logstash" bị lỗi thì ta thực hiện lệnh "sudo apt-get upgrade" trước khi chạy lại lệnh trên.
  
  + **Demo**
  
    Ta thực hiện demo sử dụng kết hợp các module Filebeat + Logstash + Elasticsearch + Kibana theo mô hình: Filebeat theo dõi sự thay đổi các file log về nhiệt độ, độ ẩm từ các nguồn khác nhau(các cụm sensor), gửi nội dung log về cho Logstash. Logstash sẽ tiến hành phân tích log và tách các thông tin về id cụm sensor, nhiệt độ và độ ẩm tại cụm sensor đó. Sau khi tách thông tin xong sẽ gửi cho Elasticsearch để index dữ liệu và dùng Kibana để visualize thông tin từ các cụm sensor này.

    Vệc cài đặt môi trường demo xem lại tài liệu [2], [3]. Sau đây ta sẽ đi cấu hình lần lượt các thành phần để chúng giao tiếp được với nhau.
    
    - Cấu hình Filebeat: vào file "/etc/filebeat/filebeat.yml". Ta tiến hành comment lại các phần cấu hình output ra Elasticsearch và cấu hình output trỏ tới Logstash
    
      ```
      #Cấu hình thư mục để theo dõi sự thay đổi      
      filebeat:
        prospectors:
          paths:
            - /home/nguyenbinh/beat/testlog/nguyenbinh*.log 

      #Cấu hình đầu ra là Logstash
      output:
      
        #elasticsearch:
        #  hosts: ["localhost:9200"]
        #  template:
        #    path: "filebeat.template.json"
     
        logstash:
          hosts: ["localhost:5043"]
      ```
      
    - Cấu hình Logstash: Tạo file cấu hình bất kỳ (lúc khỏi chạy Logstash sẽ trỏ tới file này) với nội dung như sau
    
      ```
      #Cấu hình đầu vào từ 2 nguồn.
      input {
          #nguồn thứ nhất là theo dõi từ file logstash-tutorial.log 
          file {
              path => "/home/nguyenbinh/elk/logstash/logstash-tutorial.log"
          }
          #nguồn thứ hai là nhận dữ liệu từ beat tại cổng 5043
          beats {
             port => "5043"
          }
      }
      
      #Cấu hình lọc log có khuôn mẫu có thông tin id của cụm sensor, nhiệt độ và độ ẩm
      filter {
          grok {
              match => { "message" => "(id %{DATA:id}:)([^\"]*)(temp %{DATA:temp}oC)([^\"]*)(humidity %{DATA:humidity}%)"}
          }
      }
      
      #Cấu hình đầu ra là gửi tới Elasticsearch để index
      output {
          elasticsearch {
          }
      }
      ```
      Lưu ý: Cách sử dụng grok patterns xem thêm tài liệu [4]
    - Cấu hình Elasticsearch và Kibana xem lại tài liệu [2], [3]
      
    Sau khi đã cấu hình xong, ta tiến hành khởi chạy lần lượt các thành phần:
      
      ```
      #Khởi chạy Elasticsearch
      sudo /etc/init.d/elasticsearch start

      #Khởi chạy Kibana      
      ./elk/kibana-4.5.1-linux-x64/bin/kibana
      
      #Khởi chạy Logstash. Trong đó "first-pipeline.conf" là file cấu hình đã khởi tạo ở bước trước
      /opt/logstash/bin/logstash -f "~/elk/logstash/first-pipeline.conf"
      
      #Khởi chạy Filebeat
      sudo /etc/init.d/filebeat start
      ```
      
    Khi các thành phần đã chạy, ta vào các file log và tiến hành ghi thêm các thông tin vào để test thử. Ví dụ ta điền vào file "logstash-tutorial.log" nội dung "asdasd id 19: a a c v d e temp 70oC a d g j ư humidity 90%", điền vào file "nguyenbinh.log" nội dung "asdasd id 1: a a c v d e temp 20oC a d g j humidity 40%". Ta vào Kibana Sence (Xem tài liệu 2) để kiểm tra thì kết quả sẽ được như hình. Như ta có thể thấy, Logstash đã tách được các thông tin về id, nhiệt độ và độ ẩm từ log ta điền vào.
      
    ![alt tag](https://github.com/nguyenvulebinh/logstash/blob/master/Screenshot%20from%202016-08-12%2018-19-39.png)
      
##Tài liệu tham khảo

[1] https://www.elastic.co/guide/en/logstash/current/installing-logstash.html

[2] https://github.com/nguyenvulebinh/elasticsearch

[3] https://github.com/nguyenvulebinh/beats_elasticsearch

[4] http://grokconstructor.appspot.com/do/match
