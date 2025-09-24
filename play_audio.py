import os
import random
import subprocess
import sys
import threading
import time



DEVICES = {
    1: "hw:2,0",
    2: "hw:3,0",
    3: "hw:4,0",
    4: "hw:5,0",
    5: "hw:6,0",
    6: "hw:7,0",
    7: "hw:8,0",
    8: "hw:9,0",
    9: "hw:10,0",
    10: "hw:11,0"
}


def play_audio(
        device_index: int,
        audio_file_base_dir: str,
        test_mode: bool
        ) -> None:
    """
    Play audio on a specific device in a loop.

    Parameters
    ----------
    device_index: int
        The index of the device as indicated in `DEVICES`
    audio_file_base_dir: str
        The path to the directory containing all audio files. This directory
        should consist of 10 files named `1` through `10` corresponding to
        each sound card. Inside should be a single `test_{index}.wav` and
        an actual audio file that is intended to be played.
    test_mode: bool
        True
            Plays a test file to help identify the sound card.
        False
            Plays the other file. NOTE: there should only be one additional
            file, but if there's more than one, a file is randomly selected.

    Returns
    -------
    None
        Continuously plays audio.
    """
    # Get the path to the folder corresponding to this sound card.
    play_dir = f"{audio_file_base_dir}/{device_index}"

    # If test mode, play the test file.
    if test_mode:
        audio_file_path = f"{play_dir}/test_{device_index}.wav"

    # If not test mode, play the other file (not the test file).
    # NOTE: if more than one non-test file is present
    # randomly select a file to play.
    else:
        audio_files = os.listdir(play_dir)
        audio_files = [f for f in audio_files if f != f"test_{device_index}.wav"]
        choice = random.choice(audio_files)

        audio_file_path = f"{play_dir}/{choice}"

    # Get the actual name of the device.
    device_name = DEVICES[device_index]

    # Play the file on a loop.
    while True:
        try:
            cmd = ["aplay", "-D", device_name, "-q", audio_file_path]
            subprocess.run(cmd, check=True)

            print(f"Playing {audio_file_path} on {device_name}")

        except subprocess.CalledProcessError:
            print(f"Error playing {audio_file_path} on {audio_file_path}")

            time.sleep(1)

        except KeyboardInterrupt:
            break



if __name__ == "__main__":

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
