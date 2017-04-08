package org.eclipse.om2m.sample.ipe.test_2;

import org.eclipse.om2m.commons.constants.Constants;
import org.eclipse.om2m.commons.obix.Bool;
import org.eclipse.om2m.commons.obix.Contract;
import org.eclipse.om2m.commons.obix.Int;
import org.eclipse.om2m.commons.obix.Obj;
import org.eclipse.om2m.commons.obix.Op;
import org.eclipse.om2m.commons.obix.Str;
import org.eclipse.om2m.commons.obix.Uri;
import org.eclipse.om2m.commons.obix.io.ObixEncoder;

public class ObixUtil {
	
	public final static int TEMPERATURE_SENSOR_TYPE = 1;
	public final static int AIR_HUMIDITY_SENSOR_TYPE = 2;
	public final static int LIGHT_SENSOR_TYPE = 3;
	public final static int HUMAN_APPEARANCE = 4;
	
	public static String getSensorDescriptorRep(String appId, String ipeId) {
		String prefix = "/" + Constants.CSE_ID + "/" + Constants.CSE_NAME + "/"
				+ appId;
		Obj obj = new Obj();
		

		Op opGet = new Op();
		opGet.setName("GET");
		opGet.setHref(new Uri(prefix + "/DATA/la"));
		opGet.setIs(new Contract("retrieve"));
		obj.add(opGet);

		Op opGetDirect = new Op();
		opGetDirect.setName("GET(Direct)");
		opGetDirect.setHref(new Uri(prefix + "?appId=" + appId + "&op=get"));
		opGetDirect.setIs(new Contract("execute"));
		obj.add(opGetDirect);

		Op switchOn = new Op();
		switchOn.setName("switchOn(Direct)");
		switchOn.setHref(new Uri(prefix + "?appId=" + appId
				+ "&op=switchOn&timeDelay=0"));
		switchOn.setIs(new Contract("execute"));
		obj.add(switchOn);

		Op switchOff = new Op();
		switchOff.setName("switchOff(Direct)");
		switchOff.setHref(new Uri(prefix + "?appId=" + appId
				+ "&op=switchOff&timeDelay=0"));
		switchOff.setIs(new Contract("execute"));
		obj.add(switchOff);

		Op timeResponse = new Op();
		timeResponse.setName("timeResponse");
		timeResponse.setHref(new Uri(prefix + "?appId=" + appId
				+ "&op=timeResponse&timeDelay=5000"));
		timeResponse.setIs(new Contract("execute"));
		obj.add(timeResponse);

		return ObixEncoder.toString(obj);
	}

	public static String getActuatorDescriptorRep(String appId, String ipeId) {
		String prefix = "/" + Constants.CSE_ID + "/" + Constants.CSE_NAME + "/"
				+ appId;
		Obj obj = new Obj();

		Op opGet = new Op();
		opGet.setName("GET");
		opGet.setHref(new Uri(prefix + "/DATA/la"));
		opGet.setIs(new Contract("retrieve"));
		obj.add(opGet);

		Op opGetDirect = new Op();
		opGetDirect.setName("GET(Direct)");
		opGetDirect.setHref(new Uri(prefix + "?op=get"));
		opGetDirect.setIs(new Contract("execute"));
		obj.add(opGetDirect);

		Op opON = new Op();
		opON.setName("ON");
		opON.setHref(new Uri(prefix + "?op=true"));
		opON.setIs(new Contract("execute"));
		obj.add(opON);

		Op opOFF = new Op();
		opOFF.setName("OFF");
		opOFF.setHref(new Uri(prefix + "?op=false"));
		opOFF.setIs(new Contract("execute"));
		obj.add(opOFF);

		return ObixEncoder.toString(obj);
	}

	public static String getActuatorDataRep(boolean value) {
		Obj obj = new Obj();
		obj.add(new Bool("data", value));
		return ObixEncoder.toString(obj);
	}

	public static String getSensorDataRep(int value, int type, String appId, String ipeId, String clusterId) {
		Obj obj = new Obj();
		obj.add(new Str("appId", appId));
		String category = " ";
		String unit = "";
		switch(type){
			case TEMPERATURE_SENSOR_TYPE:
				category = "temperature";
				unit = "celsius";
				break;
			case AIR_HUMIDITY_SENSOR_TYPE:
				category = "air_humidity";
				unit = "ratio";
				break;
			case LIGHT_SENSOR_TYPE:
				category = "light";
				unit = "ISO";
				break;
			case HUMAN_APPEARANCE:
				category = "human_appearance";
				unit = "s";
				break;
		}
		obj.add(new Str("ipeId", ipeId));
		obj.add(new Str("clusterId", clusterId));
		obj.add(new Str("category", category));
		obj.add(new Int("data", value));
		obj.add(new Str("unit", unit));
		return ObixEncoder.toString(obj);
	}
	public static String convertSensorDataRep(Monitor.SensorDataItem sensorItem){
		Obj obj = new Obj();
//		obj.add(new Str("appId", sensorItem.mAppId));		
//		obj.add(new Str("ipeId", sensorItem.mIpeId));
		obj.add(new Str("sensorId", sensorItem.mSensorId));
		obj.add(new Str("clusterId", sensorItem.mClusterId));
		obj.add(new Str("category", sensorItem.mCategory));
		obj.add(new Str("type", sensorItem.mType));
		obj.add(new Int("data", Integer.valueOf(sensorItem.mData)));
		obj.add(new Str("unit", sensorItem.mUnit));
		return ObixEncoder.toString(obj);
	}
	
	public static String convertItemToDataRep(Monitor.Item item, int value, String timestampSensor, String numOfSensor, long timeReceived){
		Obj obj = new Obj();
		obj.add(new Str("itemId", item.itemName));
		String category = " ";
		String unit = "";
		switch(Integer.valueOf(item.itemType)){
			case TEMPERATURE_SENSOR_TYPE:
				category = "temperature";
				unit = "celsius";
				break;
			case AIR_HUMIDITY_SENSOR_TYPE:
				category = "air_humidity";
				unit = "ratio";
				break;
			case LIGHT_SENSOR_TYPE:
				category = "light";
				unit = "ISO";
				break;
			case HUMAN_APPEARANCE:
				category = "human_appearance";
				unit = "s";
				break;
		}
		obj.add(new Str("platformId", "onem2m_1"));
		obj.add(new Str("platformType", "onem2m"));
		obj.add(new Str("clusterId", "fog_1"));
		obj.add(new Str("category", category));
		obj.add(new Int("data", value));
		obj.add(new Str("timestamp_sensor", timestampSensor));
		long timeSend = System.currentTimeMillis();
		String timemillis = String.valueOf(timeSend);
		String timeseconds = timemillis.substring(0, 10);
		String millis = timemillis.substring(10);
		String time = timeseconds+'.'+millis;
		obj.add(new Str("timestamp_platform", time));
		obj.add(new Str("time_platform_process", String.valueOf((timeSend-timeReceived)/1000.0)));
		obj.add(new Str("num_of_sensor", numOfSensor));
		obj.add(new Str("unit", unit));
		return ObixEncoder.toString(obj);
	}
	
	public static String getDataSubscriber(){
//		Obj obj = new Obj();
//		obj.add(new Str("su", "http://0.0.0.0:9090/monitor"));
//		obj.add(new Int("nct", 2));
//		return ObixEncoder.toString(obj);
		String s = "<m2m:sub xmlns:m2m=&quot;http://www.onem2m.org/xml/protocols&quot;>"+ 
				"<nct>2</nct>"+
				"<nu>http://0.0.0.0:9090/monitor</nu>"+
				"</m2m:sub>";
		return s;
	}
	public static String getMessage(String message) {
		Obj obj = new Obj();
		obj.add(new Str("message", message));
		return ObixEncoder.toString(obj);
	}
}
