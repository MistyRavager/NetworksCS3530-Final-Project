# This is code for the accepter process in the Paxos algorithm

import socket
import json
import threading
import sys

# make a lock for the shared variables
lock_Np = threading.Lock()
lock_Na = threading.Lock()
lock_va = threading.Lock()

N_promised = 0 # The highest proposal number proposed to this accepter
N_acc = 0 # The highest proposal number accepted by this accepter
v_acc = 0

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = "localhost"
print(host)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Bind to the port
serversocket.bind((host, port))

# Start listening on the port
serversocket.listen(5)

def process(clientsocket, addr):
    global N_promised, N_acc, v_acc
    print()
    msg = clientsocket.recv(1024)
    msg = msg.decode('ascii')
    msg = json.loads(msg)
    print(f"Got {msg}")
    res_msg = None

    type, N_proposed = msg['type'], msg['proposal_number']
    lock_Np.acquire()
    if N_proposed < N_promised:
        res_msg = {'type':'reject'}
        clientsocket.send(json.dumps(res_msg).encode('ascii'))
        lock_Np.release()
        return
    lock_Np.release()
    
    if type == 'promise':
        lock_Na.acquire()
        if N_acc > 0:
            res_msg = {'type':'promise', 'proposal_number':N_acc, 'value':v_acc}
        else:
            res_msg = {'type':'promise'}
        lock_Na.release()

        lock_Np.acquire()
        N_promised = N_proposed
        lock_Np.release()
    elif type == 'commit':
        if not 'value' in msg:
            res_msg = {'type':'reject'}
            clientsocket.send(json.dumps(res_msg).encode('ascii'))
            return
        
        lock_Np.acquire()
        if N_proposed != N_promised:
            res_msg = {'type':'reject'}
            clientsocket.send(json.dumps(res_msg).encode('ascii'))
            lock_Np.release()
            return
        lock_Np.release()
        lock_Na.acquire()
        lock_va.acquire()
        N_acc, v_acc = N_proposed, msg['value']
        lock_va.release()
        lock_Na.release()
        res_msg = {'type':'ack'}

    print(f"Sending {res_msg}")
    clientsocket.send(json.dumps(res_msg).encode('ascii'))

try:
    while True:
        clientsocket,addr = serversocket.accept()

        threading.Thread(target=process, args=(clientsocket, addr)).start()
except KeyboardInterrupt:
    serversocket.close()
