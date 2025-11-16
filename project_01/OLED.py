import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO
import time

# --- Import THE OLD (GOOD) OLED Libraries ---
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# ----------------------------
# USER CONFIGURATION
# ----------------------------
fs = 44100          # Sampling rate (Hz)
device = 'hw:1,0'   # Your USB microphone device
output_file = "waveform.png"
BUTTON_PIN = "P1_36" # Your working button pin

# --- OLED CONFIGURATION ---
# !! SET THIS to the bus number that worked in i2cdetect (1 or 2) !!
I2C_BUS = 1         
RST = None          # Use None if the RST pin isn't connected
# 128x64 or 128x32. Change this to match your display.
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=I2C_BUS)
# ----------------------------

# --- GPIO Setup ---
try:
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except Exception as e:
    print(f"Error setting up GPIO: {e}")
    exit(1)

# --- OLED Display Setup ---
try:
    disp.begin()
    disp.clear()
    disp.display()
    print("OLED Display Initialized.")
    # Create blank image for drawing.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    # Load a default font.
    font = ImageFont.load_default()
except Exception as e:
    print(f"Error initializing OLED: {e}")
    print("Check your I2C bus number and connections.")
    exit(1)

# --- Helper Function to Display Messages ---
def display_message(line1, line2=""):
    """Draws 1 or 2 lines of text to the OLED screen."""
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # Clear image
    draw.text((0, 0),  line1, font=font, fill=255)
    draw.text((0, 10), line2, font=font, fill=255)
    disp.image(image)
    disp.display()

# --- Main Loop ---
try:
    display_message("Press button", "to record.") # <-- Changed!
    print("Stethoscope script initialized.")
    print(f"Press and hold the button on {BUTTON_PIN} to record.")

    while True:
        print("\nWaiting for button press...")
        display_message("Press button", "to record.") # <-- Changed!
        
        # 1. Wait for button press (FALLING edge)
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        
        print("Recording started. Release button to stop.")
        display_message("RECORDING...", "(Hold button)")

        recorded_chunks = []

        # 2. Audio callback
        def audio_callback(indata, frames, time, status):
            if status:
                print(status, flush=True)
            recorded_chunks.append(indata.copy())

        # 3. Start the audio stream
        stream = sd.InputStream(
            samplerate=fs,
            device=device,
            channels=1,
            dtype='int16',
            callback=audio_callback
        )
        stream.start()

        # 4. Wait for button release (RISING edge)
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        
        print("Recording stopped.")
        display_message("Processing...", "Please wait.")
        
        # 5. Stop and close the stream
        stream.stop()
        stream.close()

        if not recorded_chunks:
            print("No audio recorded.")
            continue 

        # 6. Process the audio
        audio = np.concatenate(recorded_chunks)
        audio = audio.flatten()
        print(f"{len(audio)} samples captured.")

# 7. Plot waveform (This is your original code)
        plt.figure(figsize=(10, 4))
        plt.plot(audio, color='blue')
        plt.title("Audio Waveform")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.tight_layout()
        plt.savefig(output_file)

        print(f"Waveform saved as {output_file}")
        
        # --- NEW: DISPLAY WAVEFORM ON OLED ---
        display_message("Loading PNG...", "") # Show a loading message
        try:
            # Open the saved waveform using Pillow
            img = Image.open(output_file)
            
            # Resize it to fit the display (128x64)
            # We use ANTIALIAS for a better-looking resize
            img = img.resize((disp.width, disp.height), Image.ANTIALIAS)
            
            # Convert the image to 1-bit (black and white)
            img = img.convert('1') 
            
            # Display the processed image on the OLED
            disp.image(img)
            disp.display()
            print("Waveform image displayed on OLED.")
            
            # Show the image for 4 seconds
            time.sleep(4)
            
        except Exception as e:
            print(f"Error displaying image on OLED: {e}")
            display_message("Error:", "Image load fail")
            time.sleep(2)
        # --- END OF NEW CODE ---

except KeyboardInterrupt:
    print("\nExiting script.")
finally:
    GPIO.cleanup()
    display_message("Goodbye!") # Clear display on exit
    time.sleep(1)
    disp.clear()
    disp.display()
    print("GPIO cleanup complete.")