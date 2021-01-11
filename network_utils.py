import re
import socket

from urllib.request import urlopen

def get_public_ip():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head>'
    #        '<body>Current IP Address: nn.nn.nnn.nnn</body></html>\r\n'

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)


def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # IP that we are trying to connect to is, apparently, unimportant
    s.connect(('10.255.255.255', 1))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == '__main__':
    print(f'public ip: {get_public_ip()}')
    print(f'private ip: {get_private_ip()}')

