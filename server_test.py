import datetime
import socket
import sys

from network_utils import get_private_ip, get_public_ip

port = int(sys.argv[1])
local_ip = get_private_ip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    # We must bind to our server's internal IP address and setup a rule
    # on our router to allow communication from the specified port on
    # this computer.
    server.bind((local_ip, port))
    server.listen(5)
    print('server is online')
    print(f'connect using ip = {get_public_ip()} and port = {port}')
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

