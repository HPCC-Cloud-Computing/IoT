package org.eclipse.om2m.sample.ipe.test_2;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttTopic;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MyMqttCloudClient implements MqttCallback{
	String _cloudTopic = null;
	String _cloudBrokerAddress = null;
	String _clientId = null;
	MqttClient _mqCloudClient = null;	
	
	public MyMqttCloudClient(String cloudTopic, String cloudBrokerAddress, String clientId) {
		this._cloudTopic = cloudTopic;
		this._cloudBrokerAddress = cloudBrokerAddress;
		this._clientId = clientId;
		MemoryPersistence persistence = new MemoryPersistence();
		try {
			this._mqCloudClient = new MqttClient(this._cloudBrokerAddress,
					"sfdf", persistence);
			this._mqCloudClient.setCallback(this);
			MqttConnectOptions connOpts = new MqttConnectOptions();
//			connOpts.setCleanSession(true);
			connOpts.setKeepAliveInterval(30);
			System.out.println("Connecting to cloud broker: " + this._cloudBrokerAddress);
			this._mqCloudClient.connect(connOpts);
			System.out.println("Connected");			
		} catch (MqttException me) {
			System.out.println("reason " + me.getReasonCode());
			System.out.println("msg " + me.getMessage());
			System.out.println("loc " + me.getLocalizedMessage());
			System.out.println("cause " + me.getCause());
			System.out.println("excep " + me);
			me.printStackTrace();
		}
	}
	
	/**
	 *  
	 * @param content
	 * @param cloudBrokerAddress
	 * @param clientId
	 * @param cloudTopic
	 */
	public void publishToMQ(String content) {
		int qos = 2;
		if(this._mqCloudClient.isConnected()){
			MqttTopic topic = this._mqCloudClient.getTopic(this._cloudTopic);			
			MqttMessage message = new MqttMessage(content.getBytes());
			message.setQos(qos);
			MqttDeliveryToken token = null;
	    	try {
	    		// publish message to broker
				token = topic.publish(message);
		    	// Wait until the message has been delivered to the broker
//				token.waitForCompletion();
				System.out.println("Publishing message: " + content);
				Thread.sleep(100);
//				this._mqCloudClient.disconnect();
			} catch (Exception e) {
				e.printStackTrace();
			}		
		}
		else{
			try {
				this._mqCloudClient.reconnect();
				MqttTopic topic = this._mqCloudClient.getTopic(this._cloudTopic);
				System.out.println("Publishing message: " + content);
				MqttMessage message = new MqttMessage(content.getBytes());
				message.setQos(qos);
				MqttDeliveryToken token = null;
		    	try {
		    		// publish message to broker
					token = topic.publish(message);
			    	// Wait until the message has been delivered to the broker
					token.waitForCompletion();
					this._mqCloudClient.disconnect();
					Thread.sleep(100);
				} catch (Exception e) {
					e.printStackTrace();
				}		
			} catch (MqttException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		try {
//			this._mqCloudClient.disconnect();
			this._mqCloudClient.close();
		} catch (MqttException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
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
			while(!this._mqCloudClient.isConnected()){
				System.out.println("Connection lost! Reconnection Cloud");
				this._mqCloudClient.reconnect();
			}	
			System.out.println("Cloud connected!");
		} catch (MqttException e) {
			// TODO Auto-generated catch block
//			e.printStackTrace();
			
		}	
		
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken arg0) {
		 try {
				System.out.println("Pub complete" + new String(arg0.getMessage().getPayload()));
			} catch (MqttException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}	
		
	}

	@Override
	public void messageArrived(String arg0, MqttMessage arg1) throws Exception {
		// TODO Auto-generated method stub
		
	}

}
