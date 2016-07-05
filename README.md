# OneM2M
### Build & Install 
##### Requirements
- [docker](https://www.docker.com/)
##### Run 
1. `docker pull huanphan/onem2m`
2. `docker run -it -p "8080:8080" onem2m:0.1`
3. Vào đường dẫn `http://127.0.0.1:8080/webpage` để truy cập giao diện Web interface của oneM2M (authenticate với user/password: admin/admin)
##### Config 

### OneM2M Features
- Các tài nguyên được lưu trữ, quản lý trong `Application Entity`
    + "DESCRIPTOR" container lưu thông tin mô tả, các hàm điều khiển tài nguyên
    + "DATA" container lưu trữ dữ liệu về trạng thái của tài nguyên
- OneM2M gồm 2 thành phần:
    + Server (IN-CSE) : quản lý các gateway
    + Gateway (MN-CSE) : thu nhận dữ liệu từ sensor
    + Lưu trữ dưới dạng phân cấp
    + IN-CSE ![cấu trúc](https://wiki.eclipse.org/images/thumb/c/c4/OM2M-web-incse.jpg/500px-OM2M-web-incse.jpg.png)
    + ![](https://wiki.eclipse.org/images/thumb/4/46/OM2M-web-link-mncse.jpg/600px-OM2M-web-link-mncse.jpg.png)
    + MN-CSE ![](https://wiki.eclipse.org/images/thumb/1/1f/OM2M-web-mn-cse.jpg/500px-OM2M-web-mn-cse.jpg.png)
    + ![cấu trúc](http://wiki.eclipse.org/images/e/e3/One-web-applications.png)
    + Container resources  ![](http://wiki.eclipse.org/images/0/00/One-web-containers.png)
    + ContentInstance Resource ![](http://wiki.eclipse.org/images/7/77/One-web-contetnInstances.png)
- Bộ giả lập LAMP 

![](http://wiki.eclipse.org/images/thumb/3/3b/Gui-lamps-init.png/300px-Gui-lamps-init.png)
##### Web interface
##### Rest API
1. Theo dõi trạng thái của resource
2. Tạo một application resource
3. Lưu trữ trạng thái của resource 
3. Điều khiển trạng thái của resource
4. Bộ resource monitoring

> [Docs here](https://wiki.eclipse.org/OM2M/one/REST_API)

### DEMO
#### Description
- Xây dựng một restful service trung gian để quản lý onem2m resource (thông qua các REST API)
    + Lấy trạng thái của application resource
    + Tạo một application resource
    + Điều khiển application resource (thay đổi trạng thái)
#### Requirements:
- Docker
- Advanced Rest Client : giả lập RESTful request
#### Run
- `python main.py`
- Gửi các Restful request lên địa chỉ` http://127.0.0.1:9090`
    + GET `/resource/{app_id}/state` : lấy thông tin của app resource app_id
    + GET `/resource/create` :  tạo 1 application resource
    + GET `/resource/{app_id}/switchON`: điều khiển app resource (chỉ dành cho bộ giả lập Lamp)
    + GET `/resource/{app_id}/switchOFF`: điều khiển app resource (chỉ dành cho bộ giả lập Lamp)

## Reference
- http://www.eclipse.org/om2m/
- https://wiki.eclipse.org/OM2M/one#Getting_started
- http://wiki.eclipse.org/OM2M/one/Clone
- http://wiki.eclipse.org/OM2M/one/Web_Interface


