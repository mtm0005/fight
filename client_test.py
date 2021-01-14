import argparse
import socket
import sys


def parse_args(cmd_line_args):
    parser = argparse.ArgumentParser(description='Connect to a "Fight!" server')

    parser.add_argument('server_ip', metavar='server-ip',
                        help='IP of the server to connect with')
    parser.add_argument('--port', '-p',
                        type=int,
                        default=2015,
                        help='port for sockets to communicate over (defaults to 2015)')

    args = parser.parse_args(cmd_line_args)
    return args


def main(cmd_line_args):
    args = parse_args(cmd_line_args)
    print(f'Attempting to connect to fight server at {args.server_ip}:{args.port}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.server_ip, args.port))
    print(s.recv(1024))
    s.send('exit'.encode('utf-8'))

    print('done')


if __name__ == '__main__':
    main(sys.argv[1:])
