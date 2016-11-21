package org.eclipse.om2m.sample.ipe.test_2;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.eclipse.paho.client.mqttv3.MqttTopic;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MyMqttFogClient implements MqttCallback{

	String _fogTopic = null;
	String _cloudTopic = null;
	String _fogBrokerAddress = null;
	String _cloudBrokerAddress = null;
	String _fogClientId = null;
	String _cloudClientId = null;
	MyMqttCloudClient _mqCloudClient = null;
//	MqttClient _mqCloudClient = null;
	MqttClient _mqFogClient = null;

	public MyMqttFogClient(String fogTopic, String fogBrokerAddress, String cloudTopic, String cloudBrokerAddress, String fogClientId, String cloudClientId) {
		this._fogTopic = fogTopic;
		this._cloudTopic = cloudTopic;
		this._fogBrokerAddress = fogBrokerAddress;
		this._cloudBrokerAddress = cloudBrokerAddress;
		this._fogClientId = fogClientId;
		this._cloudClientId = cloudClientId;
		MemoryPersistence persistence = new MemoryPersistence();
//		try {
//			this._mqCloudClient = new MqttClient(this._cloudBrokerAddress,
//					_cloudClientId, persistence);
//			this._mqCloudClient.setCallback(this);
//			MqttConnectOptions connOpts = new MqttConnectOptions();
//			connOpts.setCleanSession(true);
//			connOpts.setKeepAliveInterval(30);
//			System.out.println("Connecting to cloud broker: " + this._cloudBrokerAddress);
//			this._mqCloudClient.connect(connOpts);
//			System.out.println("Connected");			
//		} catch (MqttException me) {
//			System.out.println("reason " + me.getReasonCode());
//			System.out.println("msg " + me.getMessage());
//			System.out.println("loc " + me.getLocalizedMessage());
//			System.out.println("cause " + me.getCause());
//			System.out.println("excep " + me);
//			me.printStackTrace();
//		}		
		try {
			this._mqFogClient = new MqttClient(this._fogBrokerAddress, this._fogClientId,
					persistence);
			MqttConnectOptions connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);
			connOpts.setKeepAliveInterval(30);
			System.out.println("Connecting to fog broker: " + this._fogBrokerAddress);
			this._mqFogClient.connect(connOpts);
			System.out.println("Connected");
		} catch (MqttException e) {
			e.printStackTrace();
		}
//		this._mqCloudClient = new MyMqttCloudClient(this._cloudTopic, this._cloudBrokerAddress, "oneM2M publisher");
	}
	/**
	 *  
	 * @param content
	 * @param cloudBrokerAddress
	 * @param clientId
	 * @param cloudTopic
	 */
//	public void publishToMQ(String content) {
//		int qos = 2;
//		if(this._mqCloudClient.isConnected()){
//			MqttTopic topic = this._mqCloudClient.getTopic(this._cloudTopic);
//			System.out.println("Publishing message: " + content);
//			MqttMessage message = new MqttMessage(content.getBytes());
//			message.setQos(qos);
//			MqttDeliveryToken token = null;
//	    	try {
//	    		// publish message to broker
//				token = topic.publish(message);
//		    	// Wait until the message has been delivered to the broker
//				token.waitForCompletion();
//				Thread.sleep(100);
//			} catch (Exception e) {
//				e.printStackTrace();
//			}		
//		}
//		
//	}
	/**
	 * Subscribe to MQ
	 * @param fogAddress
	 * @param cliendId
	 * @param topic
	 */
	public void subscribeToMQ() {
		int qos = 2;
		MemoryPersistence persistence = new MemoryPersistence();
		try {
			if(this._mqFogClient.isConnected()){
				this._mqFogClient.subscribe(this._fogTopic, qos);
				this._mqFogClient.setCallback(this);
			}			
		} catch (MqttException e) {
			e.printStackTrace();
		}

	}	
	
	/**
	 * 
	 * connectionLost
	 * This callback is invoked upon losing the MQTT connection.
	 * 
	 */
	@Override
	public void connectionLost(Throwable arg0) {
//		System.out.println("Connection lost! Reconnection");
		// code to reconnect to the broker would go here if desired
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		try {
			while(!this._mqFogClient.isConnected()){
				System.out.println("Connection lost! Reconnection Fog");
				this._mqFogClient.reconnect();
				this._mqFogClient.connect();
				subscribeToMQ();
			}			
			System.out.println("Fog connected!");
//			if(!this._mqCloudClient.isConnected()){
//				System.out.println("Connection lost! Reconnection Cloud");
//				this._mqCloudClient.reconnect();
//			}			
		} catch (MqttException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
		
	}
	
	/**
	 * 
	 * deliveryComplete
	 * This callback is invoked when a message published by this client
	 * is successfully received by the broker.
	 * 
	 */
	@Override
	public void deliveryComplete(IMqttDeliveryToken arg0) {
		 try {
			System.out.println("Pub complete" + new String(arg0.getMessage().getPayload()));
		} catch (MqttException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}
	
	/**
	 * 
	 * messageArrived
	 * This callback is invoked when a message is received on a subscribed topic.
	 * 
	 */
	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
		String strMessage = new String(message.getPayload());
		System.out.println(strMessage);
//		MyMqttFogClient mqCloudClient = new MyMqttFogClient(this._fogTopic, this._fogBrokerAddress, this._cloudTopic, this._cloudBrokerAddress, this._fogClientId, this._cloudClientId);
//		mqCloudClient.publishToMQ(strMessage);		
		this._mqCloudClient = new MyMqttCloudClient(this._cloudTopic, this._cloudBrokerAddress, this._cloudClientId);
		this._mqCloudClient.publishToMQ(strMessage);
//		Gson gson = new Gson();
//	    ArrayList<LinkedTreeMap> object = (ArrayList<LinkedTreeMap>) gson.fromJson(strMessage, Object.class);
//	    for (LinkedTreeMap data : object){
//	    	SensorDataItem sensorItem = new SensorDataItem();
//	//    	sensorItem.mAppId = (String) data.get("appId");
//	//    	sensorItem.mIpeId = (String) data.get("ipeId");
//	    	sensorItem.mSensorId = (String) data.get("sensorId");
//	    	sensorItem.mClusterId = (String) data.get("clusterId");
//	    	sensorItem.mCategory = (String) data.get("category");
//	    	sensorItem.mType = (String) data.get("type");
//	    	sensorItem.mData = (String) data.get("data");
//	    	sensorItem.mUnit = (String) data.get("unit");
//	    	ObixUtil.convertSensorDataRep(sensorItem);
//	    	if (!sersorIdExistedMap.containsKey(sensorItem.mSensorId)){
//	    		// Create sensor instance
//	    		createSensorResources(sensorItem.mSensorId, sensorItem.mType);
//	    		// Add data
//	    		createDataContentInstance(sensorItem);
//	    	}else{
//	    		sersorIdExistedMap.put(sensorItem.mSensorId, 1);
//	    		// Add data to existed sensor instance
//	    		createDataContentInstance(sensorItem);
//	    	}
//	    	
//	    }
		
	}
	
}
