import sounddevice as sd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

# ----------------------------
# USER CONFIGURATION
# ----------------------------
fs = 44100         # Sampling rate (Hz)
duration = 20        # Recording duration (seconds)
device = 'hw:1,0'   # Your USB microphone device
output_file = "waveform.png"
# ----------------------------

print(f"Recording {duration} seconds from device {device}...")

# Record audio
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=device)
sd.wait()  # Wait until recording finishes
audio = np.array(audio).flatten()

print("Recording complete. Saving waveform...")

# Plot waveform
plt.figure(figsize=(10, 4))
plt.plot(audio, color='blue')
plt.title("Audio Waveform")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.savefig(output_file)

print(f"Waveform saved as {output_file}")
