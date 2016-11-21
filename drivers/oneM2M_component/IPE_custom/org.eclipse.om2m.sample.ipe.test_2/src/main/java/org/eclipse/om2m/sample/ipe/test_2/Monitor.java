package org.eclipse.om2m.sample.ipe.test_2;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import org.eclipse.om2m.commons.constants.Constants;
import org.eclipse.om2m.commons.constants.MimeMediaType;
import org.eclipse.om2m.commons.constants.ResourceType;
import org.eclipse.om2m.commons.constants.ResponseStatusCode;
import org.eclipse.om2m.commons.resource.AE;
import org.eclipse.om2m.commons.resource.Container;
import org.eclipse.om2m.commons.resource.ContentInstance;
import org.eclipse.om2m.commons.resource.ResponsePrimitive;
import org.eclipse.om2m.core.service.CseService;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;

import org.eclipse.paho.client.mqttv3.MqttCallback;

public class Monitor {

	static CseService CSE;
	static String CSE_ID = Constants.CSE_ID;
	static String CSE_NAME = Constants.CSE_NAME;
	static String REQUEST_ENTITY = Constants.ADMIN_REQUESTING_ENTITY;
	static String ipeId = "sample";	
//	static String MQ_BROKER_CONFIG = "/usr/src/workspace/src/main/resources/mqbroker";
	static String MQ_BROKER_SUBSCRIBER_CONFIG = "/home/huanpc/oneM2M/ipe_config/mqbrokerSubscriber";
	static String MQ_BROKER_PUBLISHER_CONFIG = "/home/huanpc/oneM2M/ipe_config/mqbrokerPublisher";
	public static String[] sensorIdList = {"TEMPERATURE_SENSOR", "AIR_HUMIDITY_SENSOR", "LIGHT_SENSOR"};
	public static int[] sensorTypeList = {ObixUtil.TEMPERATURE_SENSOR_TYPE, ObixUtil.AIR_HUMIDITY_SENSOR_TYPE, ObixUtil.LIGHT_SENSOR_TYPE};
	static boolean actuatorValue = false;
	static String DESCRIPTOR = "DESCRIPTOR";
	static String DATA = "DATA";
	static long timeResponse = 2000;
//	private SensorListener sensorListener;
	public ArrayList<String> sensorIdListByConfig = new ArrayList<String>();
	public ArrayList<Integer> sensorTypeListByConfig = new ArrayList<Integer>();
	public ArrayList<Long> sensorTimeResponseByConfig = new ArrayList<Long>();
	public ArrayList<String> sensorClusterIdByConfig = new ArrayList<String>();
	String _brokerFogAddress = null;
	String _brokerCloudAddress = null;
	String _fogTopic = null;
	String _cloudTopic = null;
	String _fogClientId = null;
	String _cloudClientId = null;	
	public ArrayList<String> sersorIdExistedList = new ArrayList<String>();
	public HashMap<String, Integer> sersorIdExistedMap = new HashMap<>();
	public MQBrokerSubscriber _subscriber = null;
	
	public Monitor(CseService cseService) {
		CSE = cseService;
	}

	public void start() {
		System.out.println("Starting Monitor");				
		readConfigFromFile();		
		this._subscriber = new MQBrokerSubscriber(this._cloudTopic, this._brokerCloudAddress, this._fogTopic, this._brokerFogAddress, this._fogClientId, this._cloudClientId);
		this._subscriber.start();
	}

	public void stop() {
		if (this._subscriber != null && this._subscriber.isAlive()) {
			this._subscriber.stop();
		}
	}

//	public void startWithDelayTime(final long timeDelay) {
//		new Thread(new Runnable() {
//
//			@Override
//			public void run() {
//				long startTime = System.currentTimeMillis();
//				long currentTime = System.currentTimeMillis();
//				while ((currentTime - startTime) != timeDelay) {
//					currentTime = System.currentTimeMillis();
//				}
//				start();
//			}
//		}).start();
//	}
//
//	public void stopWithDelayTime(final long timeDelay) {
//		new Thread(new Runnable() {
//
//			@Override
//			public void run() {
//				long startTime = System.currentTimeMillis();
//				long currentTime = System.currentTimeMillis();
//				while ((currentTime - startTime) != timeDelay) {
//					currentTime = System.currentTimeMillis();
//				}
//				stop();
//			}
//		}).start();
//	}

	public void setTimeResponse(long timeDelay) {
		if (timeResponse > 1000)
			timeResponse = timeDelay;
	}

//	public void createListSensorResources() {		
//		System.out.println("Create list sensors");
//		for(int i = 0; i < sensorIdListByConfig.size(); i++){
//			createSensorResources(sensorIdListByConfig.get(i), sensorTypeListByConfig.get(i));
//		}
//	}
	public void readConfigFromFile(){			
		// Get FOG config from Environment variable		
		String filePath = Monitor.MQ_BROKER_SUBSCRIBER_CONFIG;
		String dataConfig = "";
        try {
            try(BufferedReader br = new BufferedReader(new FileReader(filePath))) {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();

                while (line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                dataConfig = sb.toString();
            }
        } catch (IOException e) {
        	e.printStackTrace();
        }
        if(!dataConfig.equals("")){
        	Gson gson = new Gson();
            LinkedTreeMap object = (LinkedTreeMap) gson.fromJson(dataConfig, Object.class);
        	this._brokerFogAddress = (String) object.get("brokerAddress");
        	this._fogTopic = (String) object.get("topic");
        	this._fogClientId = (String) object.get("clientId");
        }
        // Get Cloud config
        filePath = Monitor.MQ_BROKER_PUBLISHER_CONFIG;
        dataConfig = "";
        try {
            try(BufferedReader br = new BufferedReader(new FileReader(filePath))) {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();

                while (line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                dataConfig = sb.toString();
            }
        } catch (IOException e) {
        	e.printStackTrace();
        }
        if(!dataConfig.equals("")){
        	Gson gson = new Gson();
            LinkedTreeMap object = (LinkedTreeMap) gson.fromJson(dataConfig, Object.class);
        	this._brokerCloudAddress = (String) object.get("brokerAddress");
        	this._cloudTopic = (String) object.get("topic");
        	this._cloudClientId = (String) object.get("clientId");
        }
        
	}
	private class MQBrokerSubscriber extends Thread {
				
		private boolean mRunning = true;
		String mCloudTopic = null;
		String mFogTopic = null;
		String mFogBrokerAddress = null;
		String mCloudBrokerAddress = null;
		String mFogClientId = null;
		String mCloudClientId = null;
		
		public MQBrokerSubscriber(String cloudTopic, String cloudBrokerAddress, String fogTopic, String fogBrokerAddress, String fogClientId, String cloudClientId){
			this.mCloudBrokerAddress = cloudBrokerAddress;
			this.mCloudTopic = cloudTopic;
			this.mFogBrokerAddress = fogBrokerAddress;
			this.mFogTopic = fogTopic;
			this.mFogClientId = fogClientId;
			this.mCloudClientId = cloudClientId;
		}
		@Override
		public void run() {						
			MyMqttFogClient client = new MyMqttFogClient(this.mFogTopic, this.mFogBrokerAddress, this.mCloudTopic, this.mCloudBrokerAddress, this.mFogClientId, this.mCloudClientId);
			client.subscribeToMQ();
//			MqttCallback callBack = new MqttCallback() {
//				
//				@Override
//				public void messageArrived(String topic, MqttMessage message)
//						throws Exception {
//					String strMessage = new String(message.getPayload());
//					System.out.println(strMessage);
//					for(int i = 0; i < 10; i++){
//						client.publishToMQ(strMessage);
//					}					
////					Gson gson = new Gson();
////				    ArrayList<LinkedTreeMap> object = (ArrayList<LinkedTreeMap>) gson.fromJson(strMessage, Object.class);
////				    for (LinkedTreeMap data : object){
////				    	SensorDataItem sensorItem = new SensorDataItem();
////				//    	sensorItem.mAppId = (String) data.get("appId");
////				//    	sensorItem.mIpeId = (String) data.get("ipeId");
////				    	sensorItem.mSensorId = (String) data.get("sensorId");
////				    	sensorItem.mClusterId = (String) data.get("clusterId");
////				    	sensorItem.mCategory = (String) data.get("category");
////				    	sensorItem.mType = (String) data.get("type");
////				    	sensorItem.mData = (String) data.get("data");
////				    	sensorItem.mUnit = (String) data.get("unit");
////				    	ObixUtil.convertSensorDataRep(sensorItem);
////				    	if (!sersorIdExistedMap.containsKey(sensorItem.mSensorId)){
////				    		// Create sensor instance
////				    		createSensorResources(sensorItem.mSensorId, sensorItem.mType);
////				    		// Add data
////				    		createDataContentInstance(sensorItem);
////				    	}else{
////				    		sersorIdExistedMap.put(sensorItem.mSensorId, 1);
////				    		// Add data to existed sensor instance
////				    		createDataContentInstance(sensorItem);
////				    	}
////				    	
////				    }
//				}
//				
//				@Override
//				public void connectionLost(Throwable arg0) {
//					// TODO Auto-generated method stub
//					
//				}
//				
//				@Override
//				public void deliveryComplete(IMqttDeliveryToken arg0) {
//					// TODO Auto-generated method stub
//					
//				}
//				
//				};
//			client.subscribeToMQ(callBack);
		}

		public void stopThread() {
			mRunning = false;
			
		}

	}
	public class SensorDataItem{
		String mAppId = null;
		String mIpeId = null;
		String mSensorId = null;
		String mClusterId = null;
		String mCategory = null;
		String mType = null;
		String mData = null;
		String mUnit = null;		
	}
	
	public void createListSensor(int type, int number, long timeResponse, String clusterId){		
		String sensorIdPrefix = "";
		switch (type) {
			case ObixUtil.TEMPERATURE_SENSOR_TYPE:			
				sensorIdPrefix = clusterId+"_TEMPERATURE_SENSOR_";
				break;
			case ObixUtil.AIR_HUMIDITY_SENSOR_TYPE:			
				sensorIdPrefix = clusterId+"_AIR_HUMIDITY_SENSOR_";
				break;
			case ObixUtil.LIGHT_SENSOR_TYPE:			
				sensorIdPrefix = clusterId+"_LIGHT_SENSOR_";
				break;
			case ObixUtil.HUMAN_APPEARANCE:			
				sensorIdPrefix = clusterId+"_HUMAN_APPEARANCE_SENSOR_";
				break;
			default:
				sensorIdPrefix = clusterId+"_TEMPERATURE_SENSOR_";
				break;
		}
		for(int i=1;i<=number;i++){
			this.sensorIdListByConfig.add(sensorIdPrefix+String.valueOf(i));
			this.sensorTypeListByConfig.add(type);
			this.sensorTimeResponseByConfig.add(timeResponse);
			this.sensorClusterIdByConfig.add(clusterId);
		}
	}
	
	public void createSensorResources(String sensorId, String type) {
		String targetId, content;

		targetId = "/" + CSE_ID + "/" + CSE_NAME;
		AE ae = new AE();
		ae.setRequestReachability(true);
		ae.setAppID(ipeId);
		ae.getPointOfAccess().add(ipeId);
		ResponsePrimitive response = RequestSender.createAE(ae, sensorId);

		if (response.getResponseStatusCode().equals(ResponseStatusCode.CREATED)) {
			targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + sensorId;
			Container cnt = new Container();
			cnt.setMaxNrOfInstances(BigInteger.valueOf(10));
			// Create the DESCRIPTOR container
			RequestSender.createContainer(targetId, DESCRIPTOR, cnt);

			// Create the DATA container
			RequestSender.createContainer(targetId, DATA, cnt);

			// Create the description contentInstance
			content = ObixUtil.getSensorDescriptorRep(sensorId, ipeId);
			targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + sensorId + "/"
					+ DESCRIPTOR;
			ContentInstance cin = new ContentInstance();
			cin.setContent(content);
			cin.setContentInfo(MimeMediaType.OBIX);
			RequestSender.createContentInstance(targetId, cin);
		}
	}


//	public void listenToListSensor() {
//		sensorListener = new SensorListener();
//		sensorListener.start();
//	}
//
//
//	private class SensorListener extends Thread {
//
//		private boolean running = true;
//		private OneSensorListener[] _listListeners = new OneSensorListener[sensorIdListByConfig.size()];
//		@Override
//		public void run() {	
//				for(int i = 0; i<sensorIdListByConfig.size(); i++){
//					_listListeners[i] = new OneSensorListener(sensorTimeResponseByConfig.get(i), sensorTypeListByConfig.get(i), 
//							sensorIdListByConfig.get(i), sensorClusterIdByConfig.get(i));
//					_listListeners[i].start();
//				}
//		}
//
//		public void stopThread() {
//			running = false;
//			for(int i = 0; i<sensorIdListByConfig.size(); i++){			
//				_listListeners[i].stopThread();;
//			}
//		}
//
//	}
//	private class OneSensorListener extends Thread{
//		
//		private boolean _running = true;
//		private long _timeResponse = 2000;
//		private int _type;
//		private String _sensorId;
//		private String _clusterId;
//		public OneSensorListener(long timeResponse, int type, String sensorId, String clusterId) {
//			if (_timeResponse < timeResponse)
//				this._timeResponse = timeResponse;
//			_type = type;
//			_sensorId = sensorId;
//			_clusterId = clusterId;
////			createSubDataContentInstance(type, sensorId);
//		}
//		@Override
//		public void run() {	
//			while (_running) {					
//				try {
//					createDataContentInstance(_type, _sensorId, _clusterId);
//					Thread.sleep(_timeResponse);
//				} catch (InterruptedException e) {
//					e.printStackTrace();
//				}
//			}
//
//		}
//
//		public void stopThread() {
//			_running = false;
//		}
//
//	}
	public static void createDataContentInstance(SensorDataItem sensorItem){
		// Create the data contentInstance
		String content = ObixUtil.convertSensorDataRep(sensorItem);
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorItem.mSensorId + "/" + DATA;
		ContentInstance cin = new ContentInstance();
		cin.setContent(content);
		cin.setContentInfo(MimeMediaType.OBIX);
		RequestSender.createContentInstance(targetId, cin);		
	}
	
	public static void createSubDataContentInstance(int type, String sensorId){
		// Simulate a random measurement of the sensor
		int sensorValue = 10 + (int) (Math.random() * 100);

		// Create the data contentInstance
		String content = ObixUtil.getDataSubscriber();
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorId + "/" + DATA;
		ContentInstance cin = new ContentInstance();
		cin.setContent(content);
		cin.setContentInfo(MimeMediaType.XML);
		RequestSender.createContentInstanceXML(targetId, "SUBSCRIPTION", cin, ResourceType.SUBSCRIPTION);		
	}
	
	public static void createDataSubscriber(int type, String sensorId){
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorId + "/" + DATA;
	}
	
	public static String generateString(Random rng, String characters, int length)
	{
	    char[] text = new char[length];
	    for (int i = 0; i < length; i++)
	    {
	        text[i] = characters.charAt(rng.nextInt(characters.length()));
	    }
	    return new String(text);
	}

}