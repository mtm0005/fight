import argparse
import datetime
import socket
import sys

from network_utils import get_private_ip, get_public_ip


def parse_args(cmd_line_args):
    parser = argparse.ArgumentParser(description='Run a "Fight!" server')

    parser.add_argument('--local-host', '-l',
                        action='store_true',
                        default=False,
                        help='Only run the server on the host')
    parser.add_argument('--port', '-p',
                        type=int,
                        default=2015,
                        help='port for server to listen on (defaults to 2015)')

    args = parser.parse_args(cmd_line_args)
    return args


def run_server(args):
    local_ip = 'localhost' if args.local_host else get_private_ip()
    public_ip = 'localhost' if args.local_host else get_public_ip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        # We must bind to our server's internal IP address and setup a rule
        # on our router to allow communication from the specified port on
        # this computer.
        server.bind((local_ip, args.port))
        server.listen(5)
        print('server is online')
        print(f'connect using ip:{public_ip} or {local_ip} and port:{args.port}')
        try:
            while True:
                client, address = server.accept()
                current_date_and_time = datetime.datetime.now()
                log_msg = f'new connection from {address} at {current_date_and_time}'
                print(log_msg)
                with open('server_test_log.txt', 'a') as log_file:
                    log_file.write(f'{log_msg}\n')

                msg = f'Hey from Tad\'s Pi Server at {current_date_and_time}'
                client.send(msg.encode('utf-8'))
                client.close()
        except BaseException as e:
            server.close()
            print(f'Exception occurred: {e}')

    print('server is offline')


def main(cmd_line_args):
    args = parse_args(cmd_line_args)
    run_server(args)


if __name__ == '__main__':
    main(sys.argv[1:])
