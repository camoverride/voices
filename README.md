# Voices 🗣️ 📞

Many voices played simultaneously through telephone handsets.


## Hardware setup

First plug in a powered USB hub with 10 ports.

Then Plug a sound card into each port.

Get detailed information for each USB sound device (Notice that `ENV{ID_PATH}` differs in each of these):

```
for card in {2..11}; do
    if [ -e "/dev/snd/controlC${card}" ]; then
        echo "=== Card $card ==="
        udevadm info -q property -n /dev/snd/controlC${card} | grep -E "(ID_PATH|ID_SERIAL)"
        echo "---"
    fi
done
```

Create udev rules: `sudo vim /etc/udev/rules.d/99-usb-sound-cards.rules` with the 
following contents:

```
# Card 2 -> soundcard_1
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.1:1.0", SYMLINK+="soundcard/soundcard_1"

# Card 3 -> soundcard_2
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.3:1.0", SYMLINK+="soundcard/soundcard_2"

# Card 4 -> soundcard_3
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.1:1.0", SYMLINK+="soundcard/soundcard_3"

# Card 5 -> soundcard_4
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.2:1.0", SYMLINK+="soundcard/soundcard_4"

# Card 6 -> soundcard_5
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.4:1.0", SYMLINK+="soundcard/soundcard_5"

# Card 7 -> soundcard_6
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.2:1.0", SYMLINK+="soundcard/soundcard_6"

# Card 8 -> soundcard_7
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.3:1.0", SYMLINK+="soundcard/soundcard_7"

# Card 9 -> soundcard_8
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.3:1.0", SYMLINK+="soundcard/soundcard_8"

# Card 10 -> soundcard_9
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.4:1.0", SYMLINK+="soundcard/soundcard_9"

# Card 11 -> soundcard_10
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.4:1.0", SYMLINK+="soundcard/soundcard_10"


# Environment variables for scripting
SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.1:1.0", ENV{SOUNDCARD_NAME}="soundcard_1"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.3:1.0", ENV{SOUNDCARD_NAME}="soundcard_2"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.1:1.0", ENV{SOUNDCARD_NAME}="soundcard_3"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.2:1.0", ENV{SOUNDCARD_NAME}="soundcard_4"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.4:1.0", ENV{SOUNDCARD_NAME}="soundcard_5"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.2:1.0", ENV{SOUNDCARD_NAME}="soundcard_6"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.3:1.0", ENV{SOUNDCARD_NAME}="soundcard_7"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.3:1.0", ENV{SOUNDCARD_NAME}="soundcard_8"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.1.4:1.0", ENV{SOUNDCARD_NAME}="soundcard_9"

SUBSYSTEM=="sound", ENV{ID_PATH}=="platform-xhci-hcd.0-usb-0:1.2.4:1.0", ENV{SOUNDCARD_NAME}="soundcard_10"
```

Apply the rules:

- `sudo udevadm control --reload-rules`
- `sudo udevadm trigger`
- `sudo mkdir -p /dev/soundcard`
- `ls -la /dev/soundcard/`

Verify the mapping:
- `chmod +x ~/check_soundcards.sh`
- `./check_soundcards.sh`

The mappings will persist through reboots **BUT** the order of the mappings will likely **not** correspond to the physical order of the USB sound cards. So mark each sound card with its mapping (1, 2, 3, etc).


## Software setup

- `python -m venv .venv`
- `source .venv/bin/activate`


## Test

- `python play_audio.py`
