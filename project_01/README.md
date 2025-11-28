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


<p>Step 1: Install the System's Dependecies
  
This project relies on several python libraries that require system-level tools for compilation and audio handling. 

#Update package list 

sudo apt update 

#Install required tools and audio libraries 

sudo apt install -y python3-dev libasound-dev libportaudio2 libatlas-base-dev 
</p>
