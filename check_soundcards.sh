for card in {2..11}; do
    if [ -e "/dev/snd/controlC${card}" ]; then
        echo "--- Card $card ---"
        echo "ALSA name: $(cat /proc/asound/card${card}/id 2>/dev/null || echo 'N/A')"
        
        # Get udev path info
        ctl_path=$(udevadm info -q path -n /dev/snd/controlC${card} 2>/dev/null)
        if [ -n "$ctl_path" ]; then
            echo "Udev path: $ctl_path"
            echo "ID_PATH: $(udevadm info -q property -p "$ctl_path" | grep -o 'ID_PATH=.*' | cut -d= -f2)"
            echo "ID_SERIAL: $(udevadm info -q property -p "$ctl_path" | grep -o 'ID_SERIAL=.*' | cut -d= -f2)"
            echo "Physical path: $(udevadm info -a -p "$ctl_path" | grep 'KERNELS==' | head -3 | tail -1)"
        fi
        echo
    fi
done
