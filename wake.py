import sys
from wakeonlan import send_magic_packet

if len(sys.argv) != 2:
    print("Usage: python wakeonlan.py <mac_address>")
    sys.exit(1)
mac_address = sys.argv[1]
send_magic_packet(mac_address)
print(f"Sent Wake-on-LAN packet to MAC address: {mac_address}")