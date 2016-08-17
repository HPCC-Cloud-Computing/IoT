# Hướng dẫn tạo bản Docker image chạy kura

Có hai cách để tạo bản Docker image chạy kura

- Cách 1: Sử dụng dockerfile. Làm theo hướng dẫn:
  - Tải file "Dockerfile" về
  - Tạo một thư mục mới ví dụ "mkdir DockerFileDK"
  - Copy "Dockerfile" và thư mục "DockerFileDK" và trỏ vào thư mục "DockerFileDK"
  - Gõ lệnh build docker image "sudo docker build -t debian-kura ." Lệnh này chạy khá lâu nên phải thật bình tĩnh (tầm 60p tùy mạng)
  - Để chạy docker image vừa tạo gõ lệnh sau: "sudo docker run -i -t debian-kura -p 80:80"
- Cách 2: Sử dụng Docker hub. Bản REPOSITORY: "nguyenvulebinh/debian-kura". 
  Gõ lệnh sau để chạy container: "sudo docker run -i -t -p 80:80 nguyenvulebinh/debian-kura"
