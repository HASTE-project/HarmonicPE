#import cPickle as pickle
import socket
#import urllib3
import sys
import time
import requests
import os

#import zlib
#from pyurdme import *
#import struct
#import requests
#import os
#import pickle

from .batch_error_code import BatchErrorCode
from .setting import Setting, Services

# was 'batch.py'


"""
Entry point
"""

# if __name__ == '__main__':

""" (turned off in HW's code)
# Check for parameter (port)
argvs = sys.argv[1:]
if len(argvs) == 0:
    Services.print_help()
    exit(BatchErrorCode.INVALID_PARAMETERS)

if argvs[0] == 0:
    print("Terminated by controller.")
    exit(BatchErrorCode.SUCCESS)

if argvs[0] == '--help' or argvs[0] == '-h':
    Services.print_help()
    exit(BatchErrorCode.SUCCESS)

# Unpacking parameters
try:
    Setting.set_params(argvs[0], int(argvs[1]), argvs[2], int(argvs[3]), int(argvs[4]), argvs[5], int(argvs[6]))
except:
    print("Invalid Parameters!")
    exit(BatchErrorCode.INVALID_PARAMETERS)

# Run the flow
print("Batch " + Setting.get_node_name() + " opening socket on " + Setting.get_node_addr() + ":" + str(
    Setting.get_node_data_port()))
"""


def listen_for_tasks(fn_process_message):
    print('Listening for tasks...', flush=True)
    # BB: moved this in from outer context
    Setting.set_params_from_env()

    listening_socket = None
    # host = Setting.get_node_addr()
    host = '0.0.0.0' # Listen on all interfaces (inside the container)
    print("attempting to open local port: " + host + ":" + str(Setting.get_node_data_port()))

    # Cycle thru all the IP addresses (IPv4, IPv6, etc.) for the given host.
    # BB: my guess is this approach is being used for v4/v6 issues?
    for res in socket.getaddrinfo(host, Setting.get_node_data_port(), socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            listening_socket = socket.socket(af, socktype, proto)
            if not Setting.get_idle_timeout() == None:
                listening_socket.settimeout(Setting.get_idle_timeout()) # set the socket timeout to specified value from Settings

        except socket.error as msg:
            print(msg)
            listening_socket = None
            continue
        try:
            listening_socket.bind(sa)
            listening_socket.listen(1)
        except socket.error as msg:
            print(msg)
            listening_socket.close()
            listening_socket = None
            continue
        break

    if listening_socket is None:
        print('Open Socket Error')
        sys.exit(BatchErrorCode.OPEN_SOCKET_ERROR)

    restarted = False
    try:
        while True:
            # Send a stream request to server
            time1 = time.time()
            data = bytearray()
            if not restarted:
                Services.send_stream_request_data(data)
            time2 = time3 = time.time()
            if len(data) == 0:
                # No data return from the system, waiting for stream.
                try:
                    conn, addr = listening_socket.accept()
                    restarted = False
                except socket.timeout as t:
                    # graceful container exit - notify master I want to quit because I didn't get data within timeout
                    url = "http://{}:{}/docker?token=None&command=finished&c_name={}&short_id={}".format(
                        Setting.get_node_addr(),
                        Setting.get_worker_port(),
                        Setting.get_node_name(),
                        os.getenv('HOSTNAME')
                    )
                    content = "I am exiting with timeout exception: {}\n".format(t)
                    req = requests.get(url)

                    if req.status_code == 200:
                        # master has acknowledged termination
                        listening_socket.shutdown(socket.SHUT_RDWR)
                        listening_socket.close()
                        sys.exit(BatchErrorCode.IDLE_TIMEOUT)

                    # master did not allow termination, move to next iteration of while True
                    restarted = True
                    continue


                print('Streaming from ', addr[0], ":", addr[1])

                # Extracting object id
                # object_id = struct.unpack(">Q", conn.recv(8))[0] #(HW)

                while 1:
                    content = conn.recv(2048)
                    if not content: break
                    data += content
                conn.close()
                time3 = time.time()

                # ret = pickle.loads(str(data)) #(HW)
            else:
                # Extracting object id
                # print 'Streaming from messaging system.' #(HW)
                # object_id = struct.unpack(">Q", data[0:8])[0] #(HW)

                # ret = pickle.loads(str(data[8:])) #(HW)
                pass #HW

            # (# HW)
            # print("[Time [ " + str(time2 - time1) + " : " + str(time3 - time2) + " ]")
            # print(Setting.get_node_name() + " processing object " + str(object_id))
            # feature_list = []
            # for i, item in enumerate(ret.result):
            #     feature_list.append(Services.g2(item))

            fn_process_message(data)

            # encoder = zlib.compressobj() #(HW)
            # compressed_feature = encoder.compress(pickle.dumps(feature_list)) + encoder.flush() #(HW)

            # Services.push_feature_to_repo(compressed_feature, object_id) #(HW)

    except IOError as e:
        print(str(e))
        listening_socket.shutdown(socket.SHUT_RDWR)
        listening_socket.close()
        sys.exit(BatchErrorCode.DATA_SOCKET_ERROR)

    # unreachable
    #listening_socket.close()
    #print("Terminated by controller.")
    #sys.exit(BatchErrorCode.SUCCESS)
