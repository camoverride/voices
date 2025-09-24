import subprocess
import time



def get_current_usb_audio_cards():
    """
    Returns a set of detected ALSA USB audio card identifiers, e.g. 'card 1', 'card 2'.
    """
    result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    cards = set()
    for line in lines:
        if 'USB Audio' in line and 'card' in line:
            # Example line: card 1: Audio [USB Audio], device 0: ...
            parts = line.split()
            try:
                card_index = parts.index('card') + 1
                card_id = parts[card_index].rstrip(':')
                cards.add(card_id)
            except (ValueError, IndexError):
                continue
    return cards

def identify_ports_automatically(expected_ports=10, poll_interval=0.5, timeout=30):
    print("Starting automatic port identification...")
    print("Please plug in sound cards sequentially, one after another.")
    print("Waiting for devices...")

    mapped_ports = {}
    detected_cards = set()
    last_change_time = time.time()
    next_port_to_assign = 1

    while next_port_to_assign <= expected_ports:
        current_cards = get_current_usb_audio_cards()

        new_cards = current_cards - detected_cards
        if new_cards:
            for card in sorted(new_cards):  # just in case multiple appear
                mapped_ports[next_port_to_assign] = card
                print(f"✓ Detected new card '{card}' on physical port {next_port_to_assign}")
                next_port_to_assign += 1
                if next_port_to_assign > expected_ports:
                    break
            detected_cards = current_cards
            last_change_time = time.time()
        else:
            # No new cards detected
            if time.time() - last_change_time > timeout:
                print(f"No new devices detected for {timeout} seconds. Assuming all plugged in.")
                break

        time.sleep(poll_interval)

    print("\nFinal mapping:")
    for port, card in mapped_ports.items():
        print(f"Physical Port {port}: ALSA Card 'card {card}'")

    return mapped_ports

if __name__ == "__main__":
    identify_ports_automatically()
