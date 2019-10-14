
# coding: utf-8

# In[ ]:


import socket
import threading
import sys
import hashlib
def get():
    global message_no
    return(message_no.pop(0))
def wait_ack(i):
    global sock,p,window,t,check,ack_mat,message_no
    temp=0
    flag=0
    data,addr=sock.recvfrom(1024)
    if not data:
        flag=1
    if(flag==0):
        data=data.decode().split()
        print("recived ack ",data[2])
        ack_mat[int(data[2])]=1
        if(int(data[2])==check+1):
            check=int(data[2])
            window.pop(0)
            message_no.append(message_no[-1]+1)
            window.append(window[-1]+1)
            p=sorted(p)
            x=0
            for j in range(len(p)):
                if(p[j]==int(data[2])+1):
                    message_no.append(window[-1]+1)
                    window.append(window[-1]+1)
                    window.pop(0)
                    message_no.pop(0)
                    x+=1
            check=j
            p=p[x:]
        else:
            p.append(data[2])
host="127.0.0.1"
s_port=20016
r_port=20020
n=int(sys.argv[3])
w=int(sys.argv[1])
ack_mat=[0 *i for i in range(12)]
seq=int(sys.argv[2])
t=int(sys.argv[4])
i=0
message_no=[1*i for i in range(w)]
window=[1*i for i in range(w)]
check=-1
p=[]
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((host,r_port))
i=0
z=0
while (i<n):
    try:
        m=get()
        message=str(z)+" message number "+str(m)
        md5chksum= hashlib.md5(message.encode())
        message=message+" "+md5chksum.hexdigest()
        sock.sendto(message.encode(),(host,s_port))
        print(message)
        t1=threading.Thread(target=wait_ack,args=(i,))
        t1.start()
        i+=1
        z+=1
        z%=seq
    except:
        i=window[0]
        message=str(z) +" message number "+str(m)
        md5chksum= hashlib.md5(message.encode())
        message=message+" "+md5chksum.hexdigest()
        sock.sendto(message.encode(),(host,s_port))
        print(message)
        t2=threading.Thread(target=wait_ack,args=(i,))
        t2.start()
        i+=1
        z+=1
        z%=seq

