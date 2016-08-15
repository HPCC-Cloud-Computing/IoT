package org.eclipse.om2m.sample.ipe.test_2;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.math.BigInteger;
import java.util.ArrayList;

import org.eclipse.om2m.commons.constants.Constants;
import org.eclipse.om2m.commons.constants.MimeMediaType;
import org.eclipse.om2m.commons.constants.ResponseStatusCode;
import org.eclipse.om2m.commons.resource.AE;
import org.eclipse.om2m.commons.resource.Container;
import org.eclipse.om2m.commons.resource.ContentInstance;
import org.eclipse.om2m.commons.resource.ResponsePrimitive;
import org.eclipse.om2m.core.service.CseService;
import org.omg.CORBA.Environment;

public class Monitor {

	static CseService CSE;
	static String CSE_ID = Constants.CSE_ID;
	static String CSE_NAME = Constants.CSE_NAME;
	static String REQUEST_ENTITY = Constants.ADMIN_REQUESTING_ENTITY;
	static String ipeId = "sample";
	static String CONFIG_FILE = "config.txt";
	public static String[] sensorIdList = {"TEMPERATURE_SENSOR", "AIR_HUMIDITY_SENSOR", "LIGHT_SENSOR"};
	public static int[] sensorTypeList = {ObixUtil.TEMPERATURE_SENSOR_TYPE, ObixUtil.AIR_HUMIDITY_SENSOR_TYPE, ObixUtil.LIGHT_SENSOR_TYPE};
	static boolean actuatorValue = false;
	static String DESCRIPTOR = "DESCRIPTOR";
	static String DATA = "DATA";
	static long timeResponse = 2000;
	private SensorListener sensorListener;
	public ArrayList<String> sensorIdListByConfig = new ArrayList<String>();
	public ArrayList<Integer> sensorTypeListByConfig = new ArrayList<Integer>();
	public ArrayList<Long> sensorResponseByConfig = new ArrayList<Long>();

	public Monitor(CseService cseService) {
		CSE = cseService;
	}

	public void start() {
		System.out.println("Starting Monitor");				
		this.sensorIdListByConfig.add("HUMAN_APPEARANCE");
		this.sensorTypeListByConfig.add(ObixUtil.HUMAN_APPEARANCE);
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
//		if (actuatorListener != null && actuatorListener.isAlive()) {
//			actuatorListener.stopThread();
//		}
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
//		for(int i = 0; i < sensorIdList.length; i++){
//			createSensorResources(sensorIdList[i], sensorTypeList[i]);
//		}
		System.out.println("Create list sensors");
		for(int i = 0; i < sensorIdListByConfig.size(); i++){
			createSensorResources(sensorIdListByConfig.get(i), sensorTypeListByConfig.get(i));
		}
	}
	public void readConfigFromFile(){
		ClassLoader classloader = Thread.currentThread().getContextClassLoader();
		InputStream is = classloader.getResourceAsStream(this.CONFIG_FILE);
		
		try(BufferedReader br = new BufferedReader(new InputStreamReader(is))) {
		    String line = br.readLine();
		    while (line != null) {		   
		        String [] tokens = line.split(",");
		        int typeOfSensor = Integer.valueOf(tokens[0]);
		        int numOfSensor = Integer.valueOf(tokens[1]);
		        createListSensor(typeOfSensor, numOfSensor);
		        line = br.readLine();
		    }		    
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void createListSensor(int type, int number){		
		String sensorIdPrefix = "";
		switch (type) {
			case ObixUtil.TEMPERATURE_SENSOR_TYPE:			
				sensorIdPrefix = "TEMPERATURE_SENSOR_";
				break;
			case ObixUtil.AIR_HUMIDITY_SENSOR_TYPE:			
				sensorIdPrefix = "AIR_HUMIDITY_SENSOR_";
				break;
			case ObixUtil.LIGHT_SENSOR_TYPE:			
				sensorIdPrefix = "LIGHT_SENSOR_";
				break;
			default:
				sensorIdPrefix = "TEMPERATURE_SENSOR_";
				break;
		}
		for(int i=1;i<=number;i++){
			this.sensorIdListByConfig.add(sensorIdPrefix+String.valueOf(i));
			this.sensorTypeListByConfig.add(type);
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
		private OneSensorListener[] _listListeners = new OneSensorListener[8];
		@Override
		public void run() {	
			while (running) {	
//				for(int i = 0; i<sensorIdList.length; i++){
//					createDataContentInstance(sensorTypeList[i], sensorIdList[i]);
//				}
//				for(int i = 0; i<sensorIdListByConfig.size(); i++){
//					createDataContentInstance(sensorTypeListByConfig.get(i), sensorIdListByConfig.get(i));
//				}
//				try {
//					Thread.sleep(timeResponse);
//				} catch (InterruptedException e) {
//					e.printStackTrace();
//				}
//			}				
				for(int i = 0; i<sensorIdListByConfig.size(); i++){
					_listListeners[i] = new OneSensorListener(sensorResponseByConfig.get(i), sensorTypeListByConfig.get(i), sensorIdListByConfig.get(i));
					_listListeners[i].start();
				}
			}

		}

		public void stopThread() {
			running = false;
			for(int i = 0; i<sensorIdListByConfig.size(); i++){			
				_listListeners[i].stop();
			}
		}

	}
	private class OneSensorListener extends Thread{
		
		private boolean _running = true;
		private long _timeResponse = 2000;
		private int _type;
		private String _sensorId;
		public OneSensorListener(long timeResponse, int type, String sensorId ) {
			if (_timeResponse < timeResponse)
				this._timeResponse = timeResponse;
			_type = type;
			_sensorId = sensorId;
		}
		@Override
		public void run() {	
			while (_running) {					
				try {
					createDataContentInstance(_type, _sensorId);
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
	public static void createDataContentInstance(int type, String sensorId){
		// Simulate a random measurement of the sensor
		int sensorValue = 10 + (int) (Math.random() * 100);

		// Create the data contentInstance
		String content = ObixUtil.getSensorDataRep(sensorValue, type, sensorId);
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorId + "/" + DATA;
		ContentInstance cin = new ContentInstance();
		cin.setContent(content);
		cin.setContentInfo(MimeMediaType.OBIX);
		RequestSender.createContentInstance(targetId, cin);
		
	}
	public static void createDataSubscriber(int type, String sensorId){
		String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
				+ sensorId + "/" + DATA;
	}


}