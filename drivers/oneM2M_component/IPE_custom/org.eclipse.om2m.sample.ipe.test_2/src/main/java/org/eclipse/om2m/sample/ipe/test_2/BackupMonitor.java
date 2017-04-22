package org.eclipse.om2m.sample.ipe.test_2;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;
import java.util.ArrayList;
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
import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;


public class BackupMonitor {

	static CseService CSE;
	static String CSE_ID = Constants.CSE_ID;
	static String CSE_NAME = Constants.CSE_NAME;
	static String REQUEST_ENTITY = Constants.ADMIN_REQUESTING_ENTITY;
	static String ipeId = "sample";
	static String SENSOR_CONFIG = "/usr/src/workspace/src/main/resources/sensor_data";
	static String MQ_BROKER_CONFIG = "/usr/src/workspace/src/main/resources/mq_broker_config";
	public static String[] sensorIdList = {"TEMPERATURE_SENSOR", "AIR_HUMIDITY_SENSOR", "LIGHT_SENSOR"};
	public static int[] sensorTypeList = {ObixUtil.TEMPERATURE_SENSOR_TYPE, ObixUtil.AIR_HUMIDITY_SENSOR_TYPE, ObixUtil.LIGHT_SENSOR_TYPE};
	static boolean actuatorValue = false;
	static String DESCRIPTOR = "DESCRIPTOR";
	static String DATA = "DATA";
	static long timeResponse = 2000;
	private SensorListener sensorListener;
	public ArrayList<String> sensorIdListByConfig = new ArrayList<String>();
	public ArrayList<Integer> sensorTypeListByConfig = new ArrayList<Integer>();
	public ArrayList<Long> sensorTimeResponseByConfig = new ArrayList<Long>();
	public ArrayList<String> sensorClusterIdByConfig = new ArrayList<String>();

	public BackupMonitor(CseService cseService) {
		CSE = cseService;
	}

	public void start() {
		System.out.println("Starting Monitor");				
		readConfigFromFile();		
		// Create sensor resources
		createListSensorResources();
		// Listen for the sensor data
		listenToListSensor();
	}

	public void stop() {
		if (sensorListener != null && sensorListener.isAlive()) {
			sensorListener.stopThread();
		}
	}

	public void startWithDelayTime(final long timeDelay) {
		new Thread(new Runnable() {

			@Override
			public void run() {
				long startTime = System.currentTimeMillis();
				long currentTime = System.currentTimeMillis();
				while ((currentTime - startTime) != timeDelay) {
					currentTime = System.currentTimeMillis();
				}
				start();
			}
		}).start();
	}

	public void stopWithDelayTime(final long timeDelay) {
		new Thread(new Runnable() {

			@Override
			public void run() {
				long startTime = System.currentTimeMillis();
				long currentTime = System.currentTimeMillis();
				while ((currentTime - startTime) != timeDelay) {
					currentTime = System.currentTimeMillis();
				}
				stop();
			}
		}).start();
	}

	public void setTimeResponse(long timeDelay) {
		if (timeResponse > 1000)
			timeResponse = timeDelay;
	}

	public void createListSensorResources() {		
		System.out.println("Create list sensors");
		for(int i = 0; i < sensorIdListByConfig.size(); i++){
			createSensorResources(sensorIdListByConfig.get(i), sensorTypeListByConfig.get(i));
		}
	}
	public void readConfigFromFile(){			
		// Get from Environment variable
		
		String filePath = BackupMonitor.SENSOR_CONFIG;
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
            ArrayList<LinkedTreeMap> object = (ArrayList<LinkedTreeMap>) gson.fromJson(dataConfig, Object.class);
            for (LinkedTreeMap data : object){
            	String clusterId = (String) data.get("cluster_id");
                ArrayList<LinkedTreeMap> listSensor = (ArrayList<LinkedTreeMap>)data.get("sensor_list");
                for (LinkedTreeMap sensor : listSensor) {        
                	if(sensor != null){
                		if(sensor.containsKey("sensor_type")){
                			Double sensor_type = new Double((double)sensor.get("sensor_type"));
                			Double quantity = new Double((double)sensor.get("quantity"));
                			Double response_time = new Double((double)sensor.get("response_time"));                			
                			createListSensor(sensor_type.intValue(), quantity.intValue(), response_time.intValue(), clusterId);                		
                    	}
                	}        	        	
        		}

            }
        }
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
	
	public void createSensorResources(String sensorId, int type) {
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


	public void listenToListSensor() {
		sensorListener = new SensorListener();
		sensorListener.start();
	}


	private class SensorListener extends Thread {

		private boolean running = true;
		private OneSensorListener[] _listListeners = new OneSensorListener[sensorIdListByConfig.size()];
		@Override
		public void run() {	
				for(int i = 0; i<sensorIdListByConfig.size(); i++){
					_listListeners[i] = new OneSensorListener(sensorTimeResponseByConfig.get(i), sensorTypeListByConfig.get(i), 
							sensorIdListByConfig.get(i), sensorClusterIdByConfig.get(i));
					_listListeners[i].start();
				}
		}

		public void stopThread() {
			running = false;
			for(int i = 0; i<sensorIdListByConfig.size(); i++){			
				_listListeners[i].stopThread();;
			}
		}

	}
	private class OneSensorListener extends Thread{
		
		private boolean _running = true;
		private long _timeResponse = 2000;
		private int _type;
		private String _sensorId;
		private String _clusterId;
		public OneSensorListener(long timeResponse, int type, String sensorId, String clusterId) {
			if (_timeResponse < timeResponse)
				this._timeResponse = timeResponse;
			_type = type;
			_sensorId = sensorId;
			_clusterId = clusterId;
//			createSubDataContentInstance(type, sensorId);
		}
		@Override
		public void run() {	
			while (_running) {					
				try {
					createDataContentInstance(_type, _sensorId, _clusterId);
					Thread.sleep(_timeResponse);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}

		}

		public void stopThread() {
			_running = false;
		}

	}
	public static void createDataContentInstance(int type, String sensorId, String clusterId){
		// Simulate a random measurement of the sensor
		int sensorValue = 10 + (int) (Math.random() * 100);

		// Create the data contentInstance
		String content = ObixUtil.getSensorDataRep(sensorValue, type, sensorId, ipeId, clusterId);
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorId + "/" + DATA;
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