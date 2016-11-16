# Hướng dẫn tạo bản Docker image chạy kura

Có hai cách để tạo bản Docker image chạy kura

- Cách 1: Sử dụng dockerfile. Làm theo hướng dẫn:
  - Tải file "Dockerfile" về
  - Tạo một thư mục mới ví dụ "mkdir DockerFileDK"
  - Copy "Dockerfile", "entrypoint.sh", onboot-cron vào thư mục "DockerFileDK" và trỏ vào thư mục "DockerFileDK"
  - Gõ lệnh build docker image "sudo docker build -t debian-kura ."
  - Để chạy docker image vừa tạo gõ lệnh sau: "sudo docker run -i -t -p 80:80 -p 5002:5002 -p 1450:1450 --name debian-kura debian-kura"
- Cách 2: Sử dụng Docker hub. Bản REPOSITORY: "nguyenvulebinh/debian-kura". 
  Gõ lệnh sau để chạy container: "sudo docker run -i -t -p 80:80 -p 5002:5002 -p 1450:1450 --name debian-kura nguyenvulebinh/debian-kura"

Để chạy bundle nhận data từ một broker và chuyển data tới một server cung cấp rest api thì phải thêm các biến môi trường cho container. Ví dụ chạy lệnh như sau: "docker run -i -t -p 80:80 -p 5002:5002 -p 1450:1450 -e IP_SENSOR='172.17.0.3' -e PORT_SENSOR='1883' -e SENSOR_TOPIC='test,get-data' -e CLOUD_API='http://172.17.0.2/data' --name nguyenvulebinh/debian-kura kura"

Dấu ',' trong SENSOR_TOPIC là để ngăn cách các topic mà kura sẽ lắng nghe.
