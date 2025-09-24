import sys
import threading
import time
from _audio_utils import DEVICES, play_audio
from _sound_card_utils import identify_ports_automatically



if __name__ == "__main__":
    # Start the setup phase by manually assigning audio devices.
    # This blocks until a human has assigned the devices.
    # NOTE: if any sound cards are powered on during startup, this will cause trouble!
    identify_ports_automatically()

    print("Starting simultaneous audio playback on all 10 sound cards...")

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
