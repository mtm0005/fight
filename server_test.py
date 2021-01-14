import argparse
import datetime
import socket
import sys

#from multiprocessing import Process, Queue
from threading import Thread as Process
from queue import Queue
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


def app(client_socket, address, q):
    msgs = []
    while True:
        recv_msg = client_socket.recv(1024).decode('utf-8')
        msgs.append(recv_msg)

        client_socket.send(recv_msg.encode('utf-8'))
        if recv_msg == 'exit':
            client_socket.close()
            q.put((address, msgs))
            return


def print_msgs_from_address(address, msgs):
    print(f'Messages received from {address}:')
    for msg in msgs:
        print(f'        * {msg}')


def handle_closed_conn(active_conns, address, msgs):
    if not address in active_conns:
        print(f'Error: no address in matching {address} found in active connections')
        print(f'active address: {list(active_conns.keys())}')
        active_conns[address].append(None)
        return active_conns

    print_msgs_from_address(address, msgs)
    active_conns[address].join()
    del active_conns[address]
    return active_conns


def run_server(args):
    local_ip = 'localhost' if args.local_host else get_private_ip()
    public_ip = 'localhost' if args.local_host else get_public_ip()
    active_conns = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        # We must bind to our server's internal IP address and setup a rule
        # on our router to allow communication from the specified port on
        # this computer.
        server.bind((local_ip, args.port))
        server.listen(5)
        server.settimeout(5)
        print('server is online')
        print(f'connect using ip:{public_ip} or {local_ip} and port:{args.port}')
        q = Queue()  # used to signal to the main process that a connection has been closed
        try:
            while True:
                while not q.empty():
                    print('reading queue')
                    active_conns = handle_closed_conn(active_conns, *q.get_nowait())

                try:
                    client, address = server.accept()
                except socket.timeout:
                    continue

                while address in active_conns.keys():
                    print('duplicate address detected')
                    address += '1'

                current_date_and_time = datetime.datetime.now()
                log_msg = f'new connection from {address} at {current_date_and_time}'
                print(log_msg)
                with open('server_test_log.txt', 'a') as log_file:
                    log_file.write(f'{log_msg}\n')

                msg = f'Hey from Tad\'s Pi Server at {current_date_and_time}'
                client.send(msg.encode('utf-8'))

                active_conns[address] = Process(target=app, args=(client, address, q))
                active_conns[address].start()

        except BaseException as e:
            server.close()
            print(f'Exception occurred: {e}')
            print('Closing all active connections.')
            for process in active_conns.values():
                process.join()

    print('server is offline')


def main(cmd_line_args):
    args = parse_args(cmd_line_args)
    run_server(args)


if __name__ == '__main__':
    main(sys.argv[1:])
