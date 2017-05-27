import sys
import socket
import getopt
import array


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


def build_payload(mac):
    ffs = [0xff] * 6
    macs = map(lambda x: int(x, 16), mac.split(':')) * 16
    return array.array('B', ffs + macs)


def parse_args(argv):
    ip = '192.168.0.255'
    port = get_wol_ports()[2]
    mac = None
    verbose = False

    if len(argv) == 0:
        print help_message()
        sys.exit(0)

    options, remainder = getopt.getopt(argv, 'm:i:p:vh', ['mac=', 'ip=', 'port=', 'verbose=', 'help='])
    for opt, arg in options:
        if opt in ('-m', '--mac'):
            if len(arg.split(':')) != 6 and filter(lambda x: len(str(x)) != 2, arg.split(':')):
                print 'mac should be formatted like', '01:23:45:67:89:ab'
                return 2
            mac = arg
        elif opt in ('-i', '--ip'):
            ip = arg
        elif opt in ('-p', '--port'):
            if arg not in get_wol_ports():
                print 'Error : port invalid should be one of', get_wol_ports()
                return 2
            port = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-h', '--help'):
            print help_message()
            sys.exit(0)

    if not mac:
        print 'Mac address is required'
        print help_message()
        sys.exit(0)

    return ip, port, mac, verbose


def send(payload, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(payload, (ip, port))


def main(argv):
    ip, port, mac, verbose = parse_args(argv)
    payload = build_payload(mac)
    if verbose:
        print 'Mac  :', mac
        print 'Ip   :', ip
        print 'Port :', port
    send(payload, ip, port)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
