# Hướng dẫn cách publish/subcribe Raspberry Pi tới Broker

## Yêu cầu trước khi tiến hành kết nối 
+ **Raspberry Pi được cài đặt theo hướng dẫn[1]**
+ **THiết đặt broker đơn giản theo hướng dẫn [2] bước 1.4**
+ **Cài đặt extention [3] trên Google Chrome để làm App client điều khiển Raspberry Pi**
+ **Đọc tài liệu [4] hướng dẫn cách thêm file cấu hình vào kura**
+ **Đọc tài liệu [5] tổng quan về kết nối mqtt**
+ **Tham khảo tài liệu [6] hướng dẫn kết nối kura tới IBM Watson IoT**
+ **Mô hình kết nối sẽ như sau**

![alt tag](https://github.com/nguyenvulebinh/kura_mqtt/blob/master/13816802_1049728231783921_754624311_n.jpg)

## Các bước tiến hành kết nối
**Ta tận dụng lại project demo của kura để làm ví dụ cho việc kết nối này. Đọc tài liệu [7] trước khi thực hiện các bước dưới đây**

+ Bước 1: Đăng nhập vào giao diện kura trên web, cấu hình MqttDataTransport như hình.

![alt tag](https://github.com/nguyenvulebinh/kura_mqtt/blob/master/Screenshot%20from%202016-07-23%2010-27-41.png)

+ Bước 2: Đăng nhập vào trang "https://www.cloudmqtt.com/" và tiến hành tạo các topic như hình. Ở đây ta sẽ sử dụng 2 topic là test_mqtt và test_control

![alt tag](https://github.com/nguyenvulebinh/kura_mqtt/blob/master/Screenshot%20from%202016-07-23%2010-34-34.png)

+ Bước 3: Vào file cấu hình của project org.eclipse.kura.demo.heater (OSGI-INF/metatype/org.eclipse.kura.demo.heater.Heater.xml) để chỉnh sửa cấu hình cho kura có thể kết nối tới topic đã tạo ở bước 2. Ở đây sẽ khai báo 2 topic và các mức qos tương ứn với từng topic
``` xml
...
  <AD id="publish.semanticTopic" name="publish.semanticTopic" type="String"
		cardinality="0" required="true" default="test_mqtt"
		description="Default semantic topic to publish the messages to." />

	<AD id="publish.qos" name="publish.qos" type="Integer" cardinality="0"
		required="true" default="0" description="Default QoS to publish the messages with.">
		<Option label="Fire and forget" value="0" />
		<Option label="Al least once" value="1" />
		<Option label="At most once" value="2" />
	</AD>

	<AD id="subcribe.semanticTopic" name="subcribe.semanticTopic" type="String"
		cardinality="0" required="true" default="test_control"
		description="Default semantic topic to subcribe the messages to." />

	<AD id="subcribe.qos" name="subcribe.qos" type="Integer"
		cardinality="0" required="true" default="0"
		description="Default QoS to publish the messages with.">
		<Option label="Fire and forget" value="0" />
		<Option label="Al least once" value="1" />
		<Option label="At most once" value="2" />
	</AD>
...
```
Lưu ý: Theo như lúc mình làm thử thì topic của kura sẽ mặc định có định dang account-name/clientid/heater/tên_topic, vì thế trên broker cũng phải đặt tên topic đúng như dạng này. Ở dưới kura phần "account-name/clientid/heater/" sẽ được tự động thêm vào vì thế nên trong file cấu hình chỉnh cần để "tên_topic" là đủ.

+ Bước 4: Vào source file Heater.java thêm những phần sau (Hướng dẫn bên dưới chỉ thêm những phần code demo chưa có)
```java
  ...
  //Thêm khai báo topic để subcribe
  private static final String   SUBCRIBE_TOPIC_PROP_NAME  = "subcribe.semanticTopic";
	private static final String   SUBCRIBE_QOS_PROP_NAME    = "subcribe.qos";
  ...
  
  // Đăng ký subcribe một topic
	String  topic  = (String) m_properties.get(SUBCRIBE_TOPIC_PROP_NAME);
	Integer qos    = (Integer) m_properties.get(SUBCRIBE_QOS_PROP_NAME);
	
	try {
		m_cloudClient.subscribe(topic, qos);
		s_logger.info("Subcribe topic {}", topic);
	} 
	catch (Exception e) {
		s_logger.error("Cannot publish topic: "+topic, e);
	}
  
  ...
  
  //Hành động khi có tin nhắn mới đến từ topic subcribe.
  @Override
	public void onMessageArrived(String deviceId, String appTopic,
			KuraPayload msg, int qos, boolean retain) {
		StringBuffer buffer = new StringBuffer();
		byte[] body = msg.getBody();
		for(byte b : body){
			buffer.append((char)b + "");
		}
		s_logger.info("Nguyen Binh something happen {}: {}",msg.getBody().length, buffer.toString());
		
	}
	
	...
```
+ Bước 5: Build và deploy project lên kura.

![alt tag](https://github.com/nguyenvulebinh/kura_mqtt/blob/master/Screenshot%20from%202016-07-23%2011-02-21.png)

## Tài liệu tham khảo
[1] https://github.com/nguyenvulebinh/kura_experience/blob/master/Ket_noi_i2c.md

[2] http://iotalliance.vn/categories/tutorial/articles/huong-dan-lap-trinh-esp8266-phan-3-lap-trinh-giao-tiep-mqtt.html

[3] https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm?hl=vi

[4] http://eclipse.github.io/kura/doc/configurable_component.html

[5] http://www.indigoo.com/dox/wsmw/1_Middleware/MQTT.pdf

[6] https://developer.ibm.com/recipes/tutorials/connect-eclipse-kura-to-ibm-watson-iot/

[7] http://eclipse.github.io/kura/doc/heater_demo.html
