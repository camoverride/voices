# Voices 🗣️ 📞

Many voices played simultaneously through telephone handsets.


## Hardware setup




## Software setup

- `python -m venv .venv`
- `source .venv/bin/activate`


## Test

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
