# persistent_audio_player.py
import os
import random
import subprocess
import sys
import threading
import time

# Use persistent ALSA names instead of card numbers
DEVICES = {
    1: "port1",
    2: "port2", 
    3: "port3",
    4: "port4",
    5: "port5",
    6: "port6",
    7: "port7",
    8: "port8",
    9: "port9",
    10: "port10"
}

def play_audio(device_index: int, audio_file_base_dir: str, test_mode: bool) -> None:
    """
    Play audio on a specific device in a loop using persistent ALSA names.
    """
    # Get the persistent ALSA device name
    device_name = DEVICES[device_index]
    
    # Get the path to the folder corresponding to this sound card.
    play_dir = f"{audio_file_base_dir}/{device_index}"

    # If test mode, play the test file.
    if test_mode:
        audio_file_path = f"{play_dir}/test_{device_index}.wav"
    else:
        audio_files = os.listdir(play_dir)
        audio_files = [f for f in audio_files if f != f"test_{device_index}.wav"]
        choice = random.choice(audio_files)
        audio_file_path = f"{play_dir}/{choice}"

    # Play the file on a loop using the persistent ALSA name
    while True:
        try:
            cmd = ["aplay", "-D", device_name, "-q", audio_file_path]
            subprocess.run(cmd, check=True)
            print(f"Playing {audio_file_path} on persistent device {device_name} (physical port {device_index})")

        except subprocess.CalledProcessError:
            print(f"Error playing {audio_file_path} on {device_name}")
            time.sleep(1)

        except KeyboardInterrupt:
            break

def verify_devices():
    """Verify that all persistent devices are available"""
    print("Verifying persistent ALSA devices...")
    for port in range(1, 11):
        device_name = DEVICES[port]
        test_cmd = ["aplay", "-D", device_name, "-l"]
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Port {port} ({device_name}): Working")
        else:
            print(f"✗ Port {port} ({device_name}): Failed - {result.stderr}")

if __name__ == "__main__":
    print("Starting simultaneous audio playback on all 10 sound cards...")
    
    # Verify devices first
    verify_devices()
    
    # Check if we are using test mode.
    IS_TEST = "TEST" in sys.argv

    # Create threads for each sound card.
    threads = []
    for device_index in DEVICES:
        thread = threading.Thread(
            target=play_audio,
            args=(device_index, "sound_files", IS_TEST),
            daemon=True)
        threads.append(thread)

    # Start all threads.
    for thread in threads:
        thread.start()

    # Keep main thread alive.
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping audio playback...")