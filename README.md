# Voices 🗣️ 📞

Many voices played simultaneously through telephone handsets.


## Hardware setup

- Run this code on a Raspberry Pi 5.
- Plug a USB 3.0 hub into one of the Pi 5's USB 3.0 ports.
- NOTE: The Pi's USB 3 controller can support up to 8 devices before running out of bandwidth.
- Plug a sound card into every port.
- Plug a 3.5mm jack into the audio (green) port on every sound card.
- Splice the 3.5mm jack's internal to red and ground to black.
- Solder this wire to a rj9 jack (red to red, black to green).
- Plug into a phone handset.


## Software setup

Create udev rules [link](https://www.alsa-project.org/wiki/Changing_card_IDs_with_udev) and save them to `audio.rules`:

- `sudo cat audio.rules > /lib/udev/rules.d/85-my-usb-audio.rules`
- `sudo udevadm control --reload-rules`
- `sudo udevadm trigger`

Create alsa aliases:

- `sudo cat alsa.conf > /etc/asound.conf`

Test alsa aliases (only first three shown):

- `speaker-test -D MyDev_1 -c 2 -t wav`
- `speaker-test -D MyDev_2 -c 2 -t wav`
- `speaker-test -D MyDev_3 -c 2 -t wav`

Set up python:

- `python -m venv .venv`
- `source .venv/bin/activate`


## Test

- Power on the Pi. Wait approximately 1 minute for software to load.
- Make sure all the sound cards are either unplugged or powered off, as we need to re-map them at start-up.
- Power on/plug in each of the USB sound card ports sequentially, 1-10, waiting 2 seconds between each.
- `python play_audio.py TEST`


## Run in Production

There must be a sound file for every sound card. Place wav files in `sound_files/{card_num}/` where `card_num` corresponds to the index of the sound card. For example: `sound_files/1/birds_singing.wav`

Start a system service:

- `mkdir -p ~/.config/systemd/user`
- `cat voices.service > ~/.config/systemd/user/voices.service`
- `systemctl --user daemon-reload`
- `systemctl --user enable voices.service`
- `systemctl --user start voices.service`
- `sudo loginctl enable-linger $(whoami)`

Show the logs:

- `journalctl --user -u voices.service`

Clear logs:

- `sudo journalctl --unit=voices.service --rotate`
- `sudo journalctl --vacuum-time=1s`
