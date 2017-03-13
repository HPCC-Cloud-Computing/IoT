package org.eclipse.om2m.sample.ipe.test_2;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.eclipse.om2m.commons.constants.Constants;
import org.eclipse.om2m.commons.constants.MimeMediaType;
import org.eclipse.om2m.commons.constants.ResponseStatusCode;
import org.eclipse.om2m.commons.resource.RequestPrimitive;
import org.eclipse.om2m.commons.resource.ResponsePrimitive;
import org.eclipse.om2m.interworking.service.InterworkingService;

public class Controller implements InterworkingService {
	static String CSE_ID = Constants.CSE_ID;
	static String CSE_NAME = Constants.CSE_NAME;
	private static Log LOGGER = LogFactory.getLog(Controller.class);

	// private static Monitor mMonitor;

	// public Controller(Monitor monitor){
	// mMonitor = monitor;
	// }

	@Override
	public ResponsePrimitive doExecute(RequestPrimitive request) {
		// String[] parts = request.getTo().split("/");
		// String appId = parts[3];
		ResponsePrimitive response = new ResponsePrimitive(request);
		String appId = null;
		if (request.getQueryStrings().containsKey("appId")) {
			appId = request.getQueryStrings().get("appId").get(0);
		} else {
			response.setResponseStatusCode(ResponseStatusCode.BAD_REQUEST);
			return response;
		}
		if (request.getQueryStrings().containsKey("op")) {
			String valueOp = request.getQueryStrings().get("op").get(0);
			String timeDelay = null;
			if (request.getQueryStrings().containsKey("timeDelay")) {
				timeDelay = request.getQueryStrings().get("timeDelay").get(0);
			}
			
			LOGGER.info("Received request in Sample Test IPE: op=" + valueOp
					+ " ; timeDelay=" + timeDelay);
			switch (valueOp) {
			case "get":
//				if (appId.equals(Monitor.sensorId)) {
//					response.setContent(ObixUtil
//							.getSensorDataRep(Monitor.sensorValue));
//					request.setReturnContentType(MimeMediaType.OBIX);
//					response.setResponseStatusCode(ResponseStatusCode.OK);
//				} else if (appId.equals(Monitor.actuatorId)) {
//					response.setContent(ObixUtil
//							.getActuatorDataRep(Monitor.actuatorValue));
//					response.setResponseStatusCode(ResponseStatusCode.OK);
//				} else {
//					response.setResponseStatusCode(ResponseStatusCode.BAD_REQUEST);
//				}
				String contents = "";
				Object conts = null;
				if(appId == "all"){					
					for (String sensorId : Monitor.sensorIdList) {
						String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + sensorId+"/DATA/la";
						ResponsePrimitive resp = RequestSender.getRequest(targetId);
						if (resp.getResponseStatusCode().equals(ResponseStatusCode.OK)) {
							contents += resp.getContent(); 
						}
					}							
				}else{
					String targetId = "/" + CSE_ID + "/" + CSE_NAME + "/" + appId+"/DATA/la";
					ResponsePrimitive resp = RequestSender.getRequest(targetId);
					if (resp.getResponseStatusCode().equals(ResponseStatusCode.OK)) {
						conts = resp.getContent(); 
					}
				}
				System.out.println("-----------------------------");
				System.out.println(conts.toString());
				response.setContent(conts);
				response.setContentType(MimeMediaType.OBJ);
				response.setResponseStatusCode(ResponseStatusCode.OK);
				return response;
				// Bat, tat lap lich
//			case "switchOn":
//				if (timeDelay == null)
//					timeDelay = "0";
//				if (Activator.monitor != null) {
//					Activator.monitor.startWithDelayTime(Long
//							.valueOf(timeDelay));
//					response.setContent(ObixUtil.getMessage("switchOn"));
//				} else {
//					response.setContent(ObixUtil.getMessage("watting..."));
//				}
//				request.setReturnContentType(MimeMediaType.OBIX);
//				response.setResponseStatusCode(ResponseStatusCode.OK);
//				return response;
//			case "switchOff":
//				if (timeDelay == null)
//					timeDelay = "0";
//				if (Activator.monitor != null) {
//					Activator.monitor
//							.stopWithDelayTime(Long.valueOf(timeDelay));
//					response.setContent(ObixUtil.getMessage("switchOff"));
//				} else {
//					response.setContent(ObixUtil.getMessage("watting..."));
//				}
//				request.setReturnContentType(MimeMediaType.OBIX);
//				response.setResponseStatusCode(ResponseStatusCode.OK);
//				return response;
			case "timeResponse":
				// Thoi gian gui du lieu
				if (timeDelay != null) {
					if (Activator.monitor != null) {
						Activator.monitor.setTimeResponse(Long
								.valueOf(timeDelay));
						response.setContent(ObixUtil.getMessage("set schedule"));
					}
				}
				request.setReturnContentType(MimeMediaType.OBIX);
				response.setResponseStatusCode(ResponseStatusCode.OK);
				return response;
//			case "true":
//			case "false":
//				if (appId.equals(Monitor.actuatorId)) {
//					Monitor.actuatorValue = Boolean.parseBoolean(valueOp);
//					response.setResponseStatusCode(ResponseStatusCode.OK);
//				} else {
//					response.setResponseStatusCode(ResponseStatusCode.BAD_REQUEST);
//				}
//				return response;
			default:
				response.setResponseStatusCode(ResponseStatusCode.BAD_REQUEST);
			}
		} else {
			response.setResponseStatusCode(ResponseStatusCode.BAD_REQUEST);
		}
		return response;
	}

	@Override
	public String getAPOCPath() {
		return Monitor.ipeId;
	}

}