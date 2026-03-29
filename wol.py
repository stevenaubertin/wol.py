import sys
import socket
import getopt
import array
import re


def help_message():
    return """
    Name
        wol.py

    Description
        Send the Wake-on-LAN magic packet on the network to wake sleeping computer

    SYNTAX
        python wol.py -m <mac_address> [-i <broadcast ip address>] [-p <port>] [-v <verbose>] [-h <help message>]

    """


def get_wol_ports():
    return [0, 7, 9]


# --- Pre-flight validation ---


def validate_mac(mac):
    """Validate a MAC address string (colon-separated hex octets).

    Returns the normalised lower-case MAC on success, raises ValueError otherwise.
    """
    if not isinstance(mac, str) or not mac:
        raise ValueError("MAC address must be a non-empty string")

    pattern = re.compile(r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')
    if not pattern.match(mac):
        raise ValueError(
            f"Invalid MAC address '{mac}'. "
            "Expected format: XX:XX:XX:XX:XX:XX (hex octets)"
        )
    return mac.lower()


def validate_ip(ip):
    """Validate an IPv4 broadcast address.

    Returns the IP string on success, raises ValueError otherwise.
    """
    if not isinstance(ip, str) or not ip:
        raise ValueError("IP address must be a non-empty string")

    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError(f"Invalid IP address '{ip}'. Expected IPv4 format: X.X.X.X")

    for part in parts:
        try:
            num = int(part)
        except ValueError:
            raise ValueError(f"Invalid IP address '{ip}'. Each octet must be an integer")
        if num < 0 or num > 255:
            raise ValueError(
                f"Invalid IP address '{ip}'. Each octet must be between 0 and 255"
            )
    return ip


def validate_port(port):
    """Validate that *port* is one of the accepted WoL ports.

    Accepts both int and string representations.  Returns the port as an int.
    """
    try:
        port_int = int(port)
    except (TypeError, ValueError):
        raise ValueError(f"Port must be an integer, got '{port}'")

    valid = get_wol_ports()
    if port_int not in valid:
        raise ValueError(f"Invalid port {port_int}. Must be one of {valid}")
    return port_int


def preflight(mac, ip, port):
    """Run all pre-flight checks. Returns (mac, ip, port) normalised."""
    mac = validate_mac(mac)
    ip = validate_ip(ip)
    port = validate_port(port)
    return mac, ip, port


# --- Core logic ---


def build_payload(mac):
    """Build the WoL magic packet payload for the given MAC address."""
    mac = validate_mac(mac)
    header = [0xFF] * 6
    mac_bytes = [int(octet, 16) for octet in mac.split(':')]
    payload = header + mac_bytes * 16
    return array.array('B', payload)


def parse_args(argv):
    ip = '255.255.255.255'
    port = get_wol_ports()[2]
    mac = None
    verbose = False

    if len(argv) == 0:
        print(help_message())
        sys.exit(0)

    options, _remainder = getopt.getopt(
        argv, 'm:i:p:vh', ['mac=', 'ip=', 'port=', 'verbose', 'help']
    )
    for opt, arg in options:
        if opt in ('-m', '--mac'):
            mac = validate_mac(arg)
        elif opt in ('-i', '--ip'):
            ip = validate_ip(arg)
        elif opt in ('-p', '--port'):
            port = validate_port(arg)
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-h', '--help'):
            print(help_message())
            sys.exit(0)

    if not mac:
        print('MAC address is required')
        print(help_message())
        sys.exit(0)

    return ip, port, mac, verbose


def send(payload, ip, port):
    """Send the magic packet over UDP broadcast."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload, (ip, port))
    finally:
        sock.close()


def main(argv):
    ip, port, mac, verbose = parse_args(argv)
    mac, ip, port = preflight(mac, ip, port)
    payload = build_payload(mac)
    if verbose:
        print('Mac  :', mac)
        print('Ip   :', ip)
        print('Port :', port)
    send(payload, ip, port)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
