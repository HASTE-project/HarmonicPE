#import cPickle as pickle
import socket
#import urllib3
import sys
import time
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
    # BB: moved this in from outer context
    Setting.set_params_from_env()

    s = None
    print("attempting to open local port: " + Setting.get_node_addr() + ":" + str(Setting.get_node_data_port()))

    for res in socket.getaddrinfo(Setting.get_node_addr(), Setting.get_node_data_port(), socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(msg)
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            print(msg)
            s.close()
            s = None
            continue
        break
    if s is None:
        print('Open Socket Error')
        sys.exit(BatchErrorCode.OPEN_SOCKET_ERROR)

    try:
        while True:
            # Send a stream request to server
            time1 = time.time()
            data = bytearray()
            Services.send_stream_request_data(data)
            time2 = time3 = time.time()
            if len(data) == 0:
                # No data return from the system, waiting for stream.
                conn, addr = s.accept()
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
        s.close()
        sys.exit(BatchErrorCode.DATA_SOCKET_ERROR)

    # unreachable
    #s.close()
    #print("Terminated by controller.")
    #sys.exit(BatchErrorCode.SUCCESS)
