# setup_physical_mapping.py
import subprocess
import time

def identify_physical_ports():
    """Help identify which physical port corresponds to which ALSA name"""
    print("Physical Port Identification Utility")
    print("=====================================")
    print()
    print("This script will help you map physical USB ports to persistent ALSA names.")
    print("Please plug in ONE sound card at a time, starting from leftmost port.")
    print()
    
    port_mapping = {}
    
    for physical_port in range(1, 11):
        input(f"Plug a sound card into physical port {physical_port} (left-to-right), then press Enter...")
        
        # Wait for device to be detected
        time.sleep(2)
        
        # Find the newly detected card
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        new_card = None
        for line in lines:
            if 'USB Audio' in line and 'card' in line:
                # Extract card name (like Audio, Audio_1, etc.)
                if 'Audio_' in line:
                    card_name = line.split('Audio_')[1].split(']')[0].strip()
                    card_name = f"Audio_{card_name}"
                else:
                    card_name = "Audio"
                
                if card_name not in port_mapping.values():
                    new_card = card_name
                    break
        
        if new_card:
            port_mapping[physical_port] = new_card
            print(f"✓ Port {physical_port} -> {new_card}")
        else:
            print(f"✗ No new device detected on port {physical_port}")
    
    print("\nFinal Mapping:")
    for port, card in port_mapping.items():
        print(f"Physical Port {port}: ALSA Card '{card}' -> Persistent Name 'port{port}'")
    
    return port_mapping

if __name__ == "__main__":
    identify_physical_ports()
