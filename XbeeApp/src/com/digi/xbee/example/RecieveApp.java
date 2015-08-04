/**
 * Copyright (c) 2014-2015 Digi International Inc.,
 * All rights not expressly granted are reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Digi International Inc. 11001 Bren Road East, Minnetonka, MN 55343
 * =======================================================================
 */
package com.digi.xbee.example;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import com.digi.xbee.api.XBeeDevice;
import com.digi.xbee.api.exceptions.XBeeException;
import com.digi.xbee.api.models.XBeeMessage;
//import com.digi.xbee.api.utils.HexUtils; //used to get the Hex values being received

/**
 * XBee Java Library Receive Data polling sample application.
 * 
 * <p>This example reads data from the local device using the polling mechanism.</p>
 * 
 * <p>For a complete description on the example, refer to the 'ReadMe.txt' file
 * included in the root directory.</p>
 */
public class RecieveApp {

	
	/* Constants */
	
	// TODO Replace with the serial port where your receiver module is connected.
	private static final String PORT = "COM33";
	// TODO Replace with the baud rate of you receiver module.
	private static final int BAUD_RATE = 9600;
	
	//String holding information for line in csv file
	static String info = "";
	static String previousInfo = "";

	/**
	 * Application main method.
	 * 
	 * @param args Command line arguments.
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		System.out.println(" +-----------------------------------------+");
		System.out.println(" |  XBee Java Library Data Polling Sample  |");
		System.out.println(" +-----------------------------------------+\n");
		
		XBeeDevice myDevice = new XBeeDevice(PORT, BAUD_RATE);

		//filename is used to specify to write to a specific directory
		String filename = "C:\\Users\\Sez Cz\\Documents\\GitHub\\d3_data\\temperature_readings\\temp_data.csv";
		//File and BufferedWriter are used in writing to that directory
		File file = new File(filename);
		BufferedWriter writer = new BufferedWriter(new FileWriter(file));

		try {
			myDevice.open();
		} catch (XBeeException e) {
			e.printStackTrace();
			System.exit(1);
		}
		 
		while (true) {
			XBeeMessage xbeeMessage = myDevice.readData();
			if (xbeeMessage != null)
				//this gets the xbee device number and the message being sent across
				System.out.format("From %s >> %s%n", xbeeMessage.getDevice().get64BitAddress(), 
						//HexUtils.prettyHexString(HexUtils.byteArrayToHexString(xbeeMessage.getData())), 
						info = new String(xbeeMessage.getData()));
						
						//check if the first line is a file name
						if (info.contains(".csv")){
							System.out.println("Found file title: "+ info);
							continue;
						}
			
						String[] values = info.split(",");

						for (int i = 0; i <values.length; i++){ 
							if (i < values.length - 1) {
		                        values[i]+= ",";
		                    }
							writer.write(values[i]);
						}
						//if previous info is the same, do nothing, else, send
						if(previousInfo.equals(info)){
							
						}else{
							writer.flush();
						}
						
						//update previousInfo
						previousInfo = info;

		}
	}
}
