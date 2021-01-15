import argparse
import socket
import sys
import time


def parse_args(cmd_line_args):
    parser = argparse.ArgumentParser(description='Connect to a "Fight!" server')

    parser.add_argument('server_ip', metavar='server-ip',
                        help='IP of the server to connect with')
    parser.add_argument('--port', '-p',
                        type=int,
                        default=2015,
                        help='port for sockets to communicate over (defaults to 2015)')
    parser.add_argument('--num-msgs', '-n',
                        type=int,
                        default=100,
                        help=('number of messages to send to the server before exiting'
                              '(defaults to 100)'))
    parser.add_argument('--chars-per-msg', '-c',
                        type=int,
                        default=20,
                        help='number of characters for each message to contain')

    args = parser.parse_args(cmd_line_args)
    return args


def main(cmd_line_args):
    args = parse_args(cmd_line_args)
    print(f'Attempting to connect to fight server at {args.server_ip}:{args.port}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.server_ip, args.port))
    print(s.recv(1024))

    msg = '7'*args.chars_per_msg
    recv_msgs = []
    start_time = time.time()
    for _ in range(args.num_msgs):
        s.send(msg.encode('utf-8'))
        recv_msgs.append(s.recv(1024).decode('utf-8'))

    end_time = time.time()

    s.send('exit'.encode('utf-8'))

    print(f'took {end_time-start_time} seconds to send & receive '
          f'{args.num_msgs} {args.chars_per_msg} character messages')

    assert(args.num_msgs == len(recv_msgs))


if __name__ == '__main__':
    main(sys.argv[1:])
