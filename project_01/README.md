<h1>Electronic Stethoscope Project</h1>
This repository contains the software and instructions for an electronic stethoscope that transforms a pocket beagle into a dedicated digital stethoscope or audio recording device. The device uses a USB microphone for input and an SSD1306 OLED display for user feedback and waveform visualization. 

<h2>Prerequisites (Hardware & Software)</h2>
<h3>Hardware Components</h3>

- Pocketbeagle 
- SSD1306 based OLED Display (128x32)
- Push Button (for triggering recording) 
- USB Microphone
- Wires and Breadboard

<h3>Hardware Wiring Instructions</h3>

1. OLED Display: Connect the OLED display to the Pocket Beagle's I2c bus

- OLED VCC-> Pocket Beagle VCC (3.3V or 5V)
- OLED GND -> Pocket Beagle GND
- OLED SCL -> Pocket Beagle SCL (e.g., P_19)
- OLED SDA -> Pocket Beagle SDA ( e.g., P_20)

2. Recording Button: Connect the momentory push button to the configured GPIO pin and grouund. The code is set up to use an internal pull-up resistor.

- One side of the button -> Pocketbeagle GND
- Other side of the button -> Pocketbeagle P1_36

3. USB microphone: Connect USB port to Pocket Beagle to use USB microphone 

- USB VBUS -> Pocket Beagle VBUS
- USB D- -> Pocket Beagle D-
- USB D+ -> Pocket Beagle D+
- USB GND -> Pocket Beagle GND

<h3>Software Build and Installation Instructions</h3>
<p>These instructions assume you are logged into your PocketBeagle via Cloud9</p>


<h3>Step 1: Install the System's Dependecies</h3>
  
<p>This project relies on several python libraries that require system-level tools for compilation and audio handling. 

#Update package list 

sudo apt update 

#Install required tools and audio libraries 

sudo apt install -y python3-dev libasound-dev libportaudio2 libatlas-base-dev </p>

<h3>Step 2: Install Python Libraries</h3>

<p>Use pip to install the necessary Python packages, including those for audio, GPIO, plotting, and the OLED display driver. 

#Install core dependancies 
pip3 install numpy sounddevice matplotlib pillow 

#Install PocketBeagle specific libraries (for GPIO and OLED) 
#The Adafruit BBIO library is required for the GPIO control 
pip3 install Adafruit BBIO

#Install the OLED driver library (Adafruit_SSD1306) 

git clone [https://github.com/adafruit/Adafruit_Python_SSD1306.git] (https://github.com/adafruit/Adafruit_Python_SSD1306.git)

cd Adafruit_Python_SSD1306 

sudo python3 setup.py install 

cd...

rm -rf Adafruit_Python_SSD1306 </p>

<h3>Step3: Configure Audio Device (Microphone)
</h3>

<p>The OLED.py file uses the device string 'hw:1,0'. You must verify this is the correct ID for your USB microphone</p>

1. List your audio capture devices:

arecord -l 

2. Examine the output to find your USB microphone (e.g., "card 1: Device [USB Audio Device], device O: USB Audio [USB Audio]")
3. If the card number is different from 1, you must update the device variable inside OLED.py to match (e.g., change 'hw:1,0' to 'hw:X,0').

<h2>Software Operation Instructions</h2>

Once all hardware and software are set up, you can run the main script. 

<h3> Step 1: Execute the project Script</h3>

Navigate to the project directory (e.g., /var/lib/cloud9/EDES301/project_01) and run the project using python3:

#Execute the main script

python3 OLED.py

<h3>Step 2: Running with the Shell Script</h3>

For convenience, you can use the run_project.sh script to launch the application. Ensure it has execute permissions: 

#Make the script executable 

chmod +x run_project.sh 

#Run the project 

./run_project.sh

<h3>Step 3: Recording Audio</h3>

1. The OLED display will show: "Press button to record."

2. Press and hold the momentary push button connected to the specified GPIO pin. 

3. The OLED display will change to: "Recording... (Hold button)"
Audio is streamed from the USB microphone and captured in memory

4. Audio is streamed from the USB microphone and captured in memory '

5. Release the momentary push button to stop recording.

6. The PocketBeagle will then:

- Process the audio data.
- Generate a waveform plot and save it as waveform.png
- Display the compressed, black-and-white waveform image on the OLED screen for 4 seconds.

7. The script returns to the waiting state, ready for the next button press.

<h3>Step 4: Exiting the Application</h3>

To stop the script safely and perform necessary GPIO cleanup, press Ctrl+C in the terminal where the script is running. The OLED will briefly display "Goodbye!" before clearing. 

