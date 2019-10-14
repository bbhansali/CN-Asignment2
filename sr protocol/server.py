
# coding: utf-8

# In[ ]:


import socket
import time
import sys
UDP_IP = "127.0.0.1"
UDP_PORT = 20016
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
i=int(sys.argv[2])
k=int(sys.argv[1])
j=1
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if(len(data)>0):
        data=data.decode().split()
        print ("received message:", data)
        if(j%i!=0 ):
            sock.sendto(("ack number "+str(data[3])).encode(),(UDP_IP,20020))
            print ("sent ack:", data[3])
        j+=1

