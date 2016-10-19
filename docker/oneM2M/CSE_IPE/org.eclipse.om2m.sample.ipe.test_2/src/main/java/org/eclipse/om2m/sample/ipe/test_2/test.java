package org.eclipse.om2m.sample.ipe.test_2;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class test {
	
	public void main(String [] args){	
		String filePath = "/home/huanpc/oneM2M/sensor_data.json";
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
	}
}
