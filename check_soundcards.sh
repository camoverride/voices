#!/bin/bash
echo "Sound Card Mapping:"
echo "==================="

for card in {2..11}; do
    path=$(udevadm info -q path -n /dev/snd/pcmC${card}D0p 2>/dev/null)
    if [ -n "$path" ]; then
        kernel_path=$(udevadm info -a -p "$path" | grep "KERNELS==" | head -3 | tail -1)
        echo "Card $card -> ${kernel_path#KERNELS==\"}"
    fi
done

echo
echo "Current symlinks in /dev/soundcard/:"
ls -la /dev/soundcard/
