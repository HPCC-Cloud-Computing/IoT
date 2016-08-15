package org.eclipse.om2m.sample.ipe.test_2;

import java.math.BigInteger;

import org.eclipse.om2m.commons.constants.Constants;
import org.eclipse.om2m.commons.constants.MimeMediaType;
import org.eclipse.om2m.commons.constants.ResponseStatusCode;
import org.eclipse.om2m.commons.resource.AE;
import org.eclipse.om2m.commons.resource.Container;
import org.eclipse.om2m.commons.resource.ContentInstance;
import org.eclipse.om2m.commons.resource.ResponsePrimitive;
import org.eclipse.om2m.core.service.CseService;

public class Monitor {

	static CseService CSE;
	static String CSE_ID = Constants.CSE_ID;
	static String CSE_NAME = Constants.CSE_NAME;
	static String REQUEST_ENTITY = Constants.ADMIN_REQUESTING_ENTITY;
	static String ipeId = "sample";
//	static String actuatorId = "MY_ACTUATOR";
//	static String sensorId = "MY_SENSOR";
	public static String[] sensorIdList = {"TEMPERATURE_SENSOR", "AIR_HUMIDITY_SENSOR", "LIGHT_SENSOR"};
	public static int[] sensorTypeList = {ObixUtil.TEMPERATURE_SENSOR_TYPE, ObixUtil.AIR_HUMIDITY_SENSOR_TYPE, ObixUtil.LIGHT_SENSOR_TYPE};
	static boolean actuatorValue = false;
//	static int sensorValue = 0;
	static String DESCRIPTOR = "DESCRIPTOR";
	static String DATA = "DATA";
	static long timeResponse = 2000;
	private SensorListener sensorListener;
//	private ActuatorListener actuatorListener;

	public Monitor(CseService cseService) {
		CSE = cseService;
	}

	public void start() {
		// Create sensor resources
//		createSensorResources();
		createListSensorResources();
		// Listen for the sensor data
		listenToListSensor();

		// Create required resources for the Actuator
//		createActuatorResource();
		// Listen for the Actuator data
//		listenToActuator();
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
		for(int i = 0; i < sensorIdList.length; i++){
			createSensorResources(sensorIdList[i], sensorTypeList[i]);
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

//	public void createActuatorResource() {
//		String targetId, content;
//
//		targetId = "/" + CSE_ID + "/" + CSE_NAME;
//		AE ae = new AE();
//		ae.setRequestReachability(true);
//		ae.setAppID(ipeId);
//		ae.getPointOfAccess().add(ipeId);
//		ResponsePrimitive response = RequestSender.createAE(ae, actuatorId);
//
//		if (response.getResponseStatusCode().equals(ResponseStatusCode.CREATED)) {
//			targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + actuatorId;
//			Container cnt = new Container();
//			cnt.setMaxNrOfInstances(BigInteger.valueOf(10));
//			// Create the DESCRIPTOR container
//			RequestSender.createContainer(targetId, DESCRIPTOR, cnt);
//
//			// Create the DATA container
//			RequestSender.createContainer(targetId, DATA, cnt);
//
//			
//			// Create the description contentInstance
//			content = ObixUtil.getActuatorDescriptorRep(actuatorId, ipeId);
//			targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + actuatorId + "/"
//					+ DESCRIPTOR;
//			ContentInstance cin = new ContentInstance();
//			cin.setContent(content);
//			cin.setContentInfo(MimeMediaType.OBIX);
//			RequestSender.createContentInstance(targetId, cin);
//		}
//	}

	public void listenToListSensor() {
		sensorListener = new SensorListener();
		sensorListener.start();
	}

//	public void listenToActuator() {
//		actuatorListener = new ActuatorListener();
//		actuatorListener.start();
//	}

	private static class SensorListener extends Thread {

		private boolean running = true;

		@Override
		public void run() {	
			while (running) {
				// Simulate a random measurement of the sensor
//				sensorValue = 10 + (int) (Math.random() * 100);
//
//				// Create the data contentInstance
//				String content = ObixUtil.getSensorDataRep(sensorValue);
//				String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
//						+ sensorId + "/" + DATA;
//				ContentInstance cin = new ContentInstance();
//				cin.setContent(content);
//				cin.setContentInfo(MimeMediaType.OBIX);
//				RequestSender.createContentInstance(targetId, cin);
				for(int i = 0; i<sensorIdList.length; i++){
					createDataContentInstance(sensorTypeList[i], sensorIdList[i]);
				}
				try {
					Thread.sleep(timeResponse);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}

		}

		public void stopThread() {
			running = false;
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

//	private static class ActuatorListener extends Thread {
//
//		private boolean running = true;
//		private boolean memorizedActuatorValue = false;
//
//		@Override
//		public void run() {
//			while (running) {
//				// If the actuator state has changed
//				if (memorizedActuatorValue != actuatorValue) {
//					// Memorize the new actuator state
//					memorizedActuatorValue = actuatorValue;
//
//					// Create a data contentInstance
//					String content = ObixUtil
//							.getActuatorDataRep(memorizedActuatorValue);
//					String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/"
//							+ actuatorId + "/" + DATA;
//					ContentInstance cin = new ContentInstance();
//					cin.setContent(content);
//					cin.setContentInfo(MimeMediaType.OBIX);
//					RequestSender.createContentInstance(targetId, cin);
//				}
//
//				// Wait for timeResponse seconds
//				try {
//					Thread.sleep(timeResponse);
//				} catch (InterruptedException e) {
//					e.printStackTrace();
//				}
//			}
//		}
//
//		public void stopThread() {
//			running = false;
//		}

//	}

}