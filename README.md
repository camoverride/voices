# Voices

Many voices played simultaneously through telephone handsets.


## Hardware setup

- First plug in a powered USB hub with 10 ports.
- Plug a sound card into each port.
- Get detailed information for each USB sound device:

```
for card in {2..11}; do
    echo "=== Card $card ==="
    udevadm info -a -p $(udevadm info -q path -n /dev/snd/pcmC${card}D0p) | grep -E "(idVendor|idProduct|KERNELS|serial|product)"
    echo
done
```

- Create udev rules: `sudo vim /etc/udev/rules.d/99-usb-sound-cards.rules` with the 
following contents:

```
# Card 2
SUBSYSTEM=="sound", KERNELS=="1-1.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_1"

# Card 3
SUBSYSTEM=="sound", KERNELS=="1-1.1.1", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_2"

# Card 4
SUBSYSTEM=="sound", KERNELS=="1-1.2.1", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_3"

# Card 5
SUBSYSTEM=="sound", KERNELS=="1-1.1.2", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_4"

# Card 6
SUBSYSTEM=="sound", KERNELS=="1-1.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_5"

# Card 7
SUBSYSTEM=="sound", KERNELS=="1-1.2.2", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_6"

# Card 8
SUBSYSTEM=="sound", KERNELS=="1-1.1.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_7"

# Card 9
SUBSYSTEM=="sound", KERNELS=="1-1.2.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_8"

# Card 10
SUBSYSTEM=="sound", KERNELS=="1-1.1.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_9"

# Card 11
SUBSYSTEM=="sound", KERNELS=="1-1.2.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", SYMLINK+="soundcard/soundcard_10"



# Environment variables for easier identification in scripts.
SUBSYSTEM=="sound", KERNELS=="1-1.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_1"

SUBSYSTEM=="sound", KERNELS=="1.1.1.1", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_2"

SUBSYSTEM=="sound", KERNELS=="1-1.2.1", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_3"

SUBSYSTEM=="sound", KERNELS=="1-1.1.2", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_4"

SUBSYSTEM=="sound", KERNELS=="1-1.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_5"

SUBSYSTEM=="sound", KERNELS=="1-1.2.2", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_6"

SUBSYSTEM=="sound", KERNELS=="1-1.1.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_7"

SUBSYSTEM=="sound", KERNELS=="1-1.2.3", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_8"

SUBSYSTEM=="sound", KERNELS=="1-1.1.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_9"

SUBSYSTEM=="sound", KERNELS=="1-1.2.4", ATTRS{idVendor}=="001f", ATTRS{idProduct}=="0b21", ENV{SOUNDCARD_NAME}="soundcard_10"
```

Notice that `KERNELS` differs in each of these. Because they are the same produce, all other information is the same.

- Apply the rules:
```
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo mkdir -p /dev/soundcard
ls -la /dev/soundcard/
```

- Verify the mapping:
- `chmod +x ~/check_soundcards.sh`
- `./check_soundcards.sh`


## Software setup

- `python -m venv .venv`
- `source .venv/bin/activate`


## Test

- `python play_audio.py`
