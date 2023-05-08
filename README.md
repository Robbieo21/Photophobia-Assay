# Photophobia-Assay

Design and development of a system to assess photophobia in rats/mice in response to different wavelengths of light.

This system requires a computer running Python that is connected via USB to the two video cameras and the Arduino microcontroller. The Python script uses OpenCV to interface with the video cameras and for video processing and tracking of the rodent. Python also handles the tracking of the time in which the rodent spends in each chamber. Python communicates with the Arduino through a serial port. The Arduino handles reading data from Python and turning on/off the LED strips of the system.

Setup and Running Instructions:
1. Plug both video cameras and the Arduino microcontroller (all via USB) to the computer running Python.
2. The Ardunio should already have the code uploaded to it so reupload is not necessary unless the code is changed.
3. Check which port the Arduino is connected to the computer with and ensure that it matches the port in the Python setup code

	3.1  To check the port that the Arduino is on open the Arduino IDE and go to Tools --> Port (the board is an Arduino Uno)
	
	3.2  The line that declares the serial communication port is currently line 21: "SerialPort.port = 'COM6'" (just need to change the number to match)
	
4. Run the Python code
5. The program will open both live video feeds and the program's output will be a timer of how long the rodent has stayed on each side
6. The program currently flips the colors of LEDs after 30 seconds of a rodent staying on one side 

    6.1  This may be changed in lines 74 and 87: "if a > 30 and count == 0:" and "if b > 30 and count == 0:"
    
    6.2  Change the "30" value to whatever value is desired in seconds
    
    6.3  Feel free to change the value in the corresponsing print statements to make them match
