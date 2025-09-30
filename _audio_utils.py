import os
import random
import subprocess
import time



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
    9: "MyDev_9",
    10: "MyDev_10"
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
