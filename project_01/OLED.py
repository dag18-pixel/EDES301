import sounddevice as sd #Library for the audio input/output (microphone/speakers)
import numpy as np #Library for the numerical operations, especially array manipulation
import matplotlib #This is matplotlib it is meant for plotting and visualization 
matplotlib.use('Agg')  # Sets the matplotlib for plotting and visualization 
import matplotlib.pyplot as plt #Pyplot module allows for creating plots
import Adafruit_BBIO.GPIO as GPIO #This library is for general purpose Input/Output (GPIO) 
import time #Library for time-related functions, such as delays 

# --- Import THE OLED Libraries ---
import Adafruit_SSD1306 #This is the driver library for the SSD1306-based OLED display
from PIL import Image, ImageDraw, ImageFont #Pillow (PIL) library for the prupose of image manipulation and drawing text 

# ----------------------------
# USER CONFIGURATION
# ----------------------------
fs = 44100          # This is the sampling rate in Hertz (Hz) - which is the standard for CD quality audio 
device = 'hw:1,0'   # This specifies the usb microphone in ALSA format 
output_file = "waveform.png" #This is the file name for the saved waveform image 
BUTTON_PIN = "P1_36" # GPIO pin name for the button input 

# --- OLED CONFIGURATION ---
I2C_BUS = 1         # I2C bus number connected to the OLED display 
RST = None          # Not connected 
# The following initializes the 128x64 OLED display object, using the specified I2C bus
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=I2C_BUS)
# ----------------------------

# --- GPIO Setup ---
#The following configures the specified button pin as an input, with an internal pull-up resistor 
#PUD_UP means that the pin is normally high (3.3V) and goes Low when the button is pressed (falling edge)
try:
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except Exception as e:
    # The following catches any errors during GPIO setup (such as an invalid pin name) and exits
    print(f"Error setting up GPIO: {e}")
    exit(1)

# --- OLED Display Setup ---
try:
    disp.begin() #This initializes the display by turning it on 
    disp.clear() # This command clears the display buffer (sets all the pixels to black)
    disp.display() #Write the cleared buffer to the screen
    print("OLED Display Initialized.")
    # Creates a blank image for drawing in 1-bit (black and white) format.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image) #This gets the drawing object for the image
    # The following loads the default font for displaying the text.
    font = ImageFont.load_default()
except Exception as e:
    # The following catches any error during the OLED initialization and exits 
    print(f"Error initializing OLED: {e}")
    print("Check your I2C bus number and connections.")
    exit(1)

# --- Helper Function to Display Messages ---
def display_message(line1, line2=""):
    """Draws 1 or 2 lines of text to the OLED screen."""
    #The following draws a filled black rectangle over the whole image to clear it 
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # Clear image
    #Draws the first line of text at the top-left corner (0, 0)
    draw.text((0, 0),  line1, font=font, fill=255)
    # Draws the second line of text, offset by 10 pixels vertically 
    draw.text((0, 10), line2, font=font, fill=255)
    disp.image(image) #Copies the PIL image buffer to the display driver 
    disp.display() #Updates the physical OLED screen with the new image 

# --- Main Loop ---
try:
    display_message("Press button", "to record.") # Initial message on OLED
    print("Stethoscope script initialized.")
    print(f"Press and hold the button on {BUTTON_PIN} to record.")

    while True:
        print("\nWaiting for button press...")
        display_message("Press button", "to record.") # Show ready message
        
        time.sleep(0.1) 
        
        # 1. Wait for button press (FALLING edge)
        #Block the execution until the button is pressed (pin voltage drops from HIGH to LOW) )
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        
        print("Recording started. Release button to stop.")
        display_message("RECORDING...", "(Hold button)")

        recorded_chunks = [] #List to store blocks of recorded audio data 

        # 2. Audio callback function
        def audio_callback(indata, frames, time, status):
            # Function is called automatically by sounddevice when a new block of audio is available 
            if status:
                print(status, flush=True) # Print any status information/warnings
            recorded_chunks.append(indata.copy()) # Append a copy of the new audio data to the list 

        # 3. Start the audio stream
        stream = sd.InputStream( 
            samplerate=fs, #sets the sample rate
            device=device, #specifies the microphone device 
            channels=1,    # Mono recording 
            dtype='int16', # Data type for the samples (16-bit integers)
            callback=audio_callback #function that calls with new audio data 
        )
        stream.start() # Begins the non-blocking audio recording stream 

        # 4. Waits for button release (RISING edge) 
        # Blocks execution until the button is released (pin voltage rises from LOW to High)
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        
        print("Recording stopped.")
        display_message("Processing...", "Please wait.")
        
        # 5. Stop and close the stream
        stream.stop()
        stream.close()

        if not recorded_chunks:
            print("No audio recorded.")
            continue # skips to the next iteration of the while loop 

        # 6. Process the audio
        # Combines all recorded NumPy arrays into a single array 
        audio = np.concatenate(recorded_chunks)
        # Flattens the array (e.g., converts (N, 1) shape to (N,))
        audio = audio.flatten()
        print(f"{len(audio)} samples captured.")

# 7. Plots waveform
        plt.figure(figsize=(10, 4)) #Creates a new Matplotlib figure
        plt.plot(audio, color='blue') #Plots the audio data as a line graph 
        plt.title("Audio Waveform")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.tight_layout() #Adjusts plot parameters for the tight layout 
        plt.savefig(output_file) #Saves the plot to the specified PNG file 

        print(f"Waveform saved as {output_file}")
        
        # --- NEW: DISPLAY WAVEFORM ON OLED ---
        display_message("Loading PNG...", "") # Shows a loading message
        try:
            # Opens the saved waveform using Pillow
            img = Image.open(output_file)
            
            # Resize it to fit the display (128x64)
            # Employs Image.LANCZOS (a high-quality resampling filter for shrinking) for better-looking resized images
            img = img.resize((disp.width, disp.height), Image.ANTIALIAS)
            
            # Converts the image to 1-bit (black and white) format 
            img = img.convert('1') 
            
            # Display the processed image on the OLED
            disp.image(img)
            disp.display()
            print("Waveform image displayed on OLED.")
            
            # Shows the image for a set duration (4 seconds)
            time.sleep(4)
            
        except Exception as e:
            print(f"Error displaying image on OLED: {e}")
            display_message("Error:", "Image load fail")
            time.sleep(2)
        

except KeyboardInterrupt:
    # Allows the user to exit the script gracefully with Ctrl+C
    print("\nExiting script.")
finally:
    # Cleanup block always executed before the script finishes 
    GPIO.cleanup() #reset all used GPIO pins to their default state 
    display_message("Goodbye!") # Display final message on OLED
    time.sleep(1)
    disp.clear() #Clear the display buffer
    disp.display() #update the screen to be blank 
    print("GPIO cleanup complete.")