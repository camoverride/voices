import os
import glob
import re



ASOUND_CONF_PATH = "/etc/asound.conf"  # Change to ~/.asoundrc for user-space

def get_card_usb_paths():
    """
    Returns a list of tuples: (card_index, usb_path), e.g. ('2', '1-1.2.3')
    """
    cards = []
    for card_path in glob.glob('/sys/class/sound/card*'):
        card_dir = os.path.basename(card_path)  # e.g., 'card2'
        card_index = card_dir.replace('card', '')

        try:
            device_path = os.path.realpath(os.path.join(card_path, 'device'))
            usb_path = os.path.basename(device_path)

            # Remove ":1.0" interface detail if present
            usb_path = usb_path.split(":")[0]

            cards.append((card_index, usb_path))
        except Exception as e:
            print(f"Skipping {card_dir}: {e}")
    return cards

def usb_sort_key(usb_path):
    """
    Converts '1-1.2.3' into [1, 1, 2, 3] for natural sorting
    """
    return list(map(int, re.findall(r'\d+', usb_path)))

def generate_asound_conf():
    cards = get_card_usb_paths()

    # Sort cards by USB topology for deterministic assignment
    sorted_cards = sorted(cards, key=lambda x: usb_sort_key(x[1]))

    with open(ASOUND_CONF_PATH, 'w') as f:
        f.write("# Auto-generated /etc/asound.conf\n\n")
        for i, (card_index, usb_path) in enumerate(sorted_cards):
            logical_name = f"port{i+1}"
            f.write(f"""pcm.{logical_name} {{
    type plug
    slave.pcm {{
        type hw
        card {card_index}
    }}
}}\n\n""")
        print(f"✓ Generated {len(sorted_cards)} device mappings in {ASOUND_CONF_PATH}")



if __name__ == "__main__":
    generate_asound_conf()
