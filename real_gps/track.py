import serial
import time
import string
import pynmea2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException
import socket
import re
import sys

import re
import pynmea2
import tkinter as tk
import tkintermapview
from time import *
import threading
import os
import geopy
from datetime import datetime
import PIL


pnChannel = "raspi-tracker";
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "KEY"
pnconfig.publish_key = "KEY"
pnconfig.ssl = False
pnconfig.user_id = "jalilmahmud92@gmail.com"
pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(pnChannel).execute()


file = open("GPS_DATA.txt","w")
HOST = "172.20.10.6"  # The server's hostname or IP address
PORT = 50000  # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))
    while True:
    
    
        s.sendall(b".")
        data = s.recv(1024)
        data_d = data.decode()
        #datas = str(datas.split())
        datas = re.search('GPGGA',data_d)
        datas1 = re.search('\n',data_d)
        if (datas):
            location = data_d[datas.start():datas1.start()]
            location_p = pynmea2.parse(location)
        
            #print(data_d)
            print("-----------")
            lnn = location_p.latitude
            lng = location_p.longitude
            sat = location_p.num_sats
            print(location)
            print("Latitude: ",lnn)
            print("Langitude: ",lng)
            print("Active Satellite: ",sat)
            file.write(location)
            file.write("\n")

            try:
                envelope = pubnub.publish().channel(pnChannel).message({
                'lat':lnn,
                'lng':lng
                }).sync()
                print("publish timetoken: %d" % envelope.result.timetoken)
            except PubNubException as e:
                handle_exception(e)
