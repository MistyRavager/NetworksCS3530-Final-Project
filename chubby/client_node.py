# from client import Client
import time
import threading
import socket
import sys
import os


server_port = 5000
server_host = '127.0.0.1'
# server_host = '10.0.0.1'

lock_lock = threading.Lock() # lock for appending to locks list
lock_acquired = threading.Lock() # lock for printing lock acquired message

locks = set()
acqu_locks = set()
id = int(sys.argv[1])
# client = Client(server_port, server_host, id, 3)

def send_keepalive(lock_num: int, client):
    # global client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = client.make_message('keepalive', lock_num)
        s.sendto(message.encode(), (server_host, server_port))
        response, addr = s.recvfrom(1024)
        if addr == (server_host, server_port):
            if client.check_keepalive_response(response.decode()):
                time.sleep(client.sleep_time)
            else:
                with lock_lock:
                    locks.remove(lock_num)
                s.close()
                return
        else :
            s.close()
            # print('Invalid response')
            return
        
def get_lock(s: socket.socket, lock_num: int, client):
    # global client
    with lock_lock:
        if lock_num in locks:
            print('Lock', lock_num, 'already acquired')
            return

    with lock_acquired:
        acqu_locks.add(lock_num)
    while True:
        message = client.make_message('request', lock_num)
        s.sendto(message.encode(), (server_host, server_port))
        response, addr = s.recvfrom(1024)
        # print(response, addr)
        if addr == (server_host, server_port):
            if client.check_lock_response(response.decode()):
                with lock_lock:
                    locks.add(lock_num)

                with lock_acquired:
                    acqu_locks.remove(lock_num)
                s.close()
                send_keepalive(lock_num, client)
                return
        else:
            # print('Invalid response')
            s.close()
            return
        time.sleep(client.sleep_time)


# try:
#     print('Client ready....')
#     # while True:
#     #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     #     lock_num = int(input('Enter lock number: '))
#     #     # print('Client requesting lock', lock_num)
#     #     threading.Thread(target=get_lock, args=(s, lock_num)).start()

# except KeyboardInterrupt:
#     # s.close()
#     print('Client closed since keyboard interrupt')
#     os._exit(1)

