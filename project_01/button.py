import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO # <-- Import the GPIO library

# ----------------------------
# USER CONFIGURATION
# ----------------------------
fs = 44100          # Sampling rate (Hz)
device = 'hw:1,0'   # Your USB microphone device
output_file = "waveform.png"
BUTTON_PIN = "P1_36" # <-- Your button pin (P2.02 maps to GPIO 59)
# ----------------------------

# --- GPIO Setup ---
# We use PUD_UP (internal pull-up resistor).
# This means:
#   - Button NOT pressed: Pin is HIGH (3.3V)
#   - Button IS pressed (connected to GND): Pin is LOW (0V)
try:
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except Exception as e:
    print(f"Error setting up GPIO: {e}")
    print("Please ensure:")
    print("  1. You are running this script as root (use 'sudo python your_script.py')")
    print("  2. The 'Adafruit-BBIO' library is installed ('pip install Adafruit-BBIO')")
    exit(1)

print("Stethoscope script initialized.")
print(f"Press and hold the button on {BUTTON_PIN} to record.")

# --- Main Loop ---
try:
    while True:
        print("\nWaiting for button press...")
        
        # 1. Wait for button press (a FALLING edge, from HIGH to LOW)
        # This function blocks the script until the button is pressed.
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        
        print("Recording started. Release button to stop.")

        # This list will store all the audio chunks we record
        recorded_chunks = []

        # 2. Define a callback function
        # This function will be called by 'sounddevice' every time
        # it gets a new block of audio data from the microphone.
        def audio_callback(indata, frames, time, status):
            """This is called for each audio block."""
            if status:
                print(status, flush=True)
            # Add the new audio data (indata) to our list
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

        # 4. Wait for button release (a RISING edge, from LOW back to HIGH)
        # The stream will keep running and calling the 'audio_callback'
        # in the background while we wait here.
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        
        print("Recording stopped.")
        
        # 5. Stop and close the stream
        stream.stop()
        stream.close()

        # Check if we actually recorded anything
        if not recorded_chunks:
            print("No audio recorded (button press was too short).")
            continue # Go back to the start of the 'while True' loop

        # 6. Process the audio
        # Combine all the small chunks into one big NumPy array
        audio = np.concatenate(recorded_chunks)
        audio = audio.flatten() # Make it a 1D array

        print(f"Recording complete. {len(audio)} samples captured.")
        print("Saving waveform...")

        # 7. Plot waveform (this is your original code)
        plt.figure(figsize=(10, 4))
        plt.plot(audio, color='blue')
        plt.title("Audio Waveform")
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.tight_layout()
        plt.savefig(output_file)

        print(f"Waveform saved as {output_file}")

except KeyboardInterrupt:
    # This block runs if you press Ctrl+C
    print("\nExiting script.")
finally:
    # This block always runs, even on exit or error
    GPIO.cleanup() # Clean up the GPIO pins
    print("GPIO cleanup complete.")