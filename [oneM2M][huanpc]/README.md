# OneM2M
### Build & Install 
##### Requirements
- [docker](https://www.docker.com/)

##### Components:
- oneM2M - port 8080
- web_service (python) : port 9090
- grafana : port 3000
- influxdb: port 8084
- cavisor

##### Run 
1. `docker-compose up`
2. Vào đường dẫn `http://127.0.0.1:8080/webpage` để truy cập giao diện Web interface của oneM2M (authenticate với user/password: admin/admin)
##### Config 

### OneM2M Features
- Các tài nguyên được lưu trữ, quản lý trong `Application Entity`
    + "DESCRIPTOR" container lưu thông tin mô tả, các hàm điều khiển tài nguyên
    + "DATA" container lưu trữ dữ liệu về trạng thái của tài nguyên
- Cấu trúc lưu trữ:
    + Lưu trữ dưới dạng phân cấp
    + IN-CSE ![cấu trúc](https://wiki.eclipse.org/images/thumb/c/c4/OM2M-web-incse.jpg/500px-OM2M-web-incse.jpg.png)
    + ![](https://wiki.eclipse.org/images/thumb/4/46/OM2M-web-link-mncse.jpg/600px-OM2M-web-link-mncse.jpg.png)
    + MN-CSE ![](https://wiki.eclipse.org/images/thumb/1/1f/OM2M-web-mn-cse.jpg/500px-OM2M-web-mn-cse.jpg.png)
    + ![cấu trúc](http://wiki.eclipse.org/images/e/e3/One-web-applications.png)
    + Container resources  ![](http://wiki.eclipse.org/images/0/00/One-web-containers.png)
    + ContentInstance Resource ![](http://wiki.eclipse.org/images/7/77/One-web-contetnInstances.png)
##### Kiến trúc OneM2M:
![](https://wiki.eclipse.org/images/2/21/IPE_Sample_Architecture.png)
###### CSE
- Server quản lý, lưu trữ
###### IPE
- The aim of an Interworking Proxy Entity is to create an interface from a device technology / specific network to the oneM2M standard.
- Điều khiển trực tiếp các sensor
- Controller package:
    + Life cycle manager:
This component is in charge of starting and stopping internal components, handle the creation of resource in the CSE at the start of the plugin and so on. Also, it has to stop any working thread in the case that the stop method of the Activator has been called.
    + Sample Controller:
The aim of the controller component is to make the interaction between the devices following the orders coming from the oneM2M interface. As your plugin will receive requests, the controller will perform the corresponding operation on the devices (retrieve the state, switch on a lamp, etc.).
- Monitor component:
    + The monitor component has to retrieve information depending on the specific technology and push that information into the CSE. For instance, it can have a thread that will look for a sensor value periodically.
- Model package:
    + As we have simulated lamps, we have to represent them using Java objects to store their "real values". This represents the devices we are going to monitor and control.
- GUI component:
    + This component only shows the state of the lamps and allows us to interact with it.


##### Web interface
##### Rest API
1. Theo dõi trạng thái của resource
2. Tạo một application resource
3. Lưu trữ trạng thái của resource 
3. Điều khiển trạng thái của resource
4. Bộ resource monitoring

> [Docs here](https://wiki.eclipse.org/OM2M/one/REST_API)

### DEMO
#### Workflow
![arch]()
#### Description
- Xây dựng một restful service trung gian để quản lý onem2m resource (thông qua các REST API)
    + Lấy trạng thái của application resource
    + Điều khiển application resource (thay đổi trạng thái)
    + Tracking dữ liệu trạng thái của các sensor và đẩy lên public queue (CloudAMPQ)
- Xây dựng bộ giả lập IPE: sinh dữ liệu trạng thái từ các sensor và gửi lên server CSE quản lý.

#### Requirements:
- Docker
- Advanced Rest Client : giả lập RESTful request
#### Run
- `pip install -r requirements.txt`
- `python3 main.py`
- Gửi các Restful request lên địa chỉ` http://127.0.0.1:9090`
    + GET `/resource/{app_id}/state` : lấy trạng thái của app resource app_id
    + GET `/resource/{app_id}/descriptor` :  lấy thông tin điều khiển của app resource app_id
    + GET `/resource/{app_id}/switchON`: điều khiển app resource (chỉ dành cho bộ giả lập Lamp)
    + GET `/resource/{app_id}/switchOFF`: điều khiển app resource (chỉ dành cho bộ giả lập Lamp)
- Tự động monitor trạng thái của một sensor chỉ định và đẩy lên một message queue 
- Server MQ: 
[CloudAMQP](https://white-mynah-bird.rmq.cloudamqp.com/#/queues/yhjylhjo/hello)

## Reference
- http://www.eclipse.org/om2m/
- https://wiki.eclipse.org/OM2M/one#Getting_started
- http://wiki.eclipse.org/OM2M/one/Clone
- http://wiki.eclipse.org/OM2M/one/Web_Interface
- https://www.cloudamqp.com/docs/index.html
- https://rabbitpy.readthedocs.io/en/latest/index.html

