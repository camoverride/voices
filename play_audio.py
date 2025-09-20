import subprocess
import threading
import time
import os



# Device mapping - ALSA hardware devices for each sound card.
DEVICES = {
    "card1": "hw:2,0",
    "card2": "hw:3,0",
    "card3": "hw:4,0",
    "card4": "hw:5,0",
    "card5": "hw:6,0",
    "card6": "hw:7,0",
    "card7": "hw:8,0",
    "card8": "hw:9,0",
    "card9": "hw:10,0",
    "card10": "hw:11,0",
}

# Audio files to play.
AUDIO_FILES = [os.path.join("sound_files", f) for f in os.listdir("sound_files")]


def play_audio(
    device : str,
    audio_file : str) -> None:
    """
    Play audio on a specific device in a loop
    """
    while True:
        try:
            cmd = ["aplay", "-D", device, "-q", audio_file]
            subprocess.run(cmd, check=True)
            print(f"Replaying {audio_file} on {device}")

        except subprocess.CalledProcessError:
            print(f"Error playing {audio_file} on {device}")
            time.sleep(1)  # Wait before retrying

        except KeyboardInterrupt:
            break



if __name__ == "__main__":

    print("Starting simultaneous audio playback on all 10 sound cards...")
    print("Press Ctrl+C to stop")

    # Check if audio files exist.
    for i, audio_file in enumerate(AUDIO_FILES):
        if not os.path.exists(audio_file):
            print(f"Error: Audio file not found: {audio_file}")
            raise FileNotFoundError

    # Create threads for each sound card.
    threads = []
    for i, (device_name, device) in enumerate(DEVICES.items()):
        if i < len(AUDIO_FILES):
            thread = threading.Thread(
                target=play_audio,
                args=(device, AUDIO_FILES[i]),
                daemon=True
            )
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
