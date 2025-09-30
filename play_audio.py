import sys
import threading
import time
from _audio_utils import play_audio



# Use persistent ALSA names instead of card numbers.
DEVICES = {
    1: "MyDev_1",
    2: "MyDev_2", 
    3: "MyDev_3",
    4: "MyDev_4",
    5: "MyDev_5",
    6: "MyDev_6",
    7: "MyDev_7",
    8: "MyDev_8",
    8: "MyDev_9"
}


if __name__ == "__main__":
    print("Starting simultaneous audio playback on all 9 sound cards...")

    # Check if we are using test mode.
    IS_TEST = "TEST" in sys.argv

    # Create threads for each sound card.
    threads = []
    for device_index in DEVICES:
        thread = threading.Thread(
            target=play_audio,
            args=(device_index, "sound_files", DEVICES, IS_TEST),
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
