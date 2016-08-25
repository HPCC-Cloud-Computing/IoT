package com.company;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;

import static java.nio.file.StandardWatchEventKinds.ENTRY_CREATE;
import static java.nio.file.StandardWatchEventKinds.ENTRY_DELETE;
import static java.nio.file.StandardWatchEventKinds.ENTRY_MODIFY;

public class Main {

    private static Thread watchFileTopic;
    private static ArrayList<String> listTopics = new ArrayList<>();
    private static String filePathTopic = "/home/nguyenbinh/Programming/Java/Java_WorkSpace/list_topics.txt";
    private static String filePathSave = "/home/nguyenbinh/Programming/Java/Java_WorkSpace/save_message.txt";
    private static MqttClient sampleClient;
    private static FileWriter fileWriter;
    private static BufferedWriter bufferWritter;
    private static String addressBroker;

    public static void main(String[] args) {

        if (args.length == 3){
            addressBroker = args[0];
            filePathTopic = args[1];
            filePathSave = args[2];

            //Tao file de ghi message nhan duoc
            try {
                fileWriter = new FileWriter(filePathSave, true);
                bufferWritter = new BufferedWriter(fileWriter);
            } catch (IOException e) {
                e.printStackTrace();
            }
            //Dang ky lang nghe su kien thay doi file tu file ghi cac topic
            createWatchService();

            //Doc file topic de lay ra cac topic can lang nghe
            updateTopicName(filePathTopic);

            //Dang ky lang nghe nhung topic nay
            registerSubcribeTopic(listTopics);
            //Chay service lang nghe thay doi file
            watchFileTopic.start();

        }else{
            System.out.println("java -jar mqttclientnb.jar ip_address file_topic file_save");
        }
    }

    private static void createWatchService(){
        watchFileTopic = new Thread(() -> {
            try {
                WatchService watcher = FileSystems.getDefault().newWatchService();
                Path dir = Paths.get(filePathTopic.substring(0, filePathTopic.lastIndexOf("/") + 1));
                dir.register(watcher, ENTRY_CREATE, ENTRY_DELETE, ENTRY_MODIFY);

                System.out.println("Watch Service registered for dir: " + dir.getFileName());

                while (true) {
                    WatchKey key;
                    try {
                        key = watcher.take();
                    } catch (InterruptedException ex) {
                        return;
                    }

                    for (WatchEvent<?> event : key.pollEvents()) {
                        WatchEvent.Kind<?> kind = event.kind();

                        @SuppressWarnings("unchecked")
                        WatchEvent<Path> ev = (WatchEvent<Path>) event;
                        Path fileName = ev.context();
                        if (kind == ENTRY_MODIFY &&
                                fileName.toString().equals(filePathTopic.substring(filePathTopic.lastIndexOf("/") + 1))) {
                            if(updateTopicName(filePathTopic)){
                                try {
                                    sampleClient.disconnect();
                                } catch (MqttException e) {
                                    e.printStackTrace();
                                }
                                System.out.println("Reregister topic");
                                registerSubcribeTopic(listTopics);
                            }
                        }
                    }

                    boolean valid = key.reset();
                    if (!valid) {
                        break;
                    }
                    Thread.sleep(10000);
                }

            } catch (IOException ex) {
                System.err.println(ex);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
    }

    /**
     * Doc file va kiem tra xem co topic nao moi khong
     * @param filePath
     * @return
     */
    private static boolean updateTopicName(String filePath){
        boolean isChange = false;
        try {
            try(BufferedReader br = new BufferedReader(new FileReader(filePath))) {
                String line = br.readLine();
                if(line != null) line = line.trim();
                while (line != null && !line.equals("")) {
                    if(!listTopics.contains(line)) {
                        listTopics.add(line);
                        isChange = true;
                    }
                    line = br.readLine();
                    if(line != null) line = line.trim();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return isChange;
    }

    private static void registerSubcribeTopic(ArrayList<String> listTopics){
        String broker = "tcp://"+addressBroker+":1883";
        String clientId = "JavaSample";
        MemoryPersistence persistence = new MemoryPersistence();

        try {
            sampleClient = new MqttClient(broker, clientId, persistence);
            MqttConnectOptions connOpts = new MqttConnectOptions();
            connOpts.setCleanSession(true);
            System.out.println("Connecting to broker: " + broker);
            sampleClient.connect(connOpts);
            String[] arrListTopic = new String[listTopics.size()];
            int[] arrQoS = new int[listTopics.size()];
            for(int i = 0; i < listTopics.size(); i++){
                arrListTopic[i] = listTopics.get(i);
                arrQoS[i] = 1;
            }
            sampleClient.subscribe(arrListTopic, arrQoS);
            System.out.println("Connected");
            sampleClient.setCallback(new SimpleCallback());
        } catch(MqttException me){
            System.out.println("reason " + me.getReasonCode());
            System.out.println("msg " + me.getMessage());
            System.out.println("loc " + me.getLocalizedMessage());
            System.out.println("cause " + me.getCause());
            System.out.println("except " + me);
            me.printStackTrace();
        }
    }


    static class SimpleCallback implements MqttCallback {
        @Override
        public void connectionLost(Throwable cause) { //Called when the client lost the connection to the broker
        }

        @Override
        public void messageArrived(String topic, MqttMessage message) throws Exception {
            String strMessage = new String(message.getPayload()) + "\n";
            strMessage = strMessage.substring(strMessage.indexOf("|") + 1);
            System.out.println("-------------------------------------------------");
            System.out.println("| Topic:" + topic);
            System.out.println("| Message: " + strMessage);
            System.out.println("-------------------------------------------------");
            bufferWritter.write(strMessage);
            bufferWritter.flush();
        }

        @Override
        public void deliveryComplete(IMqttDeliveryToken token) {//Called when a outgoing publish is complete
        }
    }

}
