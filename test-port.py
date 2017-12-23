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


for res in socket.getaddrinfo('0.0.0.0', 80, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    print(res)
    s = socket.socket(af, socktype, proto)