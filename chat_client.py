"""
群聊聊天室
客户端
"""
from socket import *
import os
import sys
#服务端地址
ADDR = ("176.215.55.250",8812)

def send_msg(sockfd,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == "quit":
            msg = "Q "+name
            sockfd.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name,text)
        sockfd.sendto(msg.encode(),ADDR)

def recv_msg(sockfd,name):
    while True:
        try:
            data,addr = sockfd.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        if data.decode()=="EXIT":
            sys.exit()
        print(data.decode())

#启动客户端
def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名：")
        msg = "L "+name
        sockfd.sendto(msg.encode(),ADDR)
        #等待反馈
        data,addr = sockfd.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    #创建新的进程
    pid = os.fork()
    if pid <0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(sockfd,name)
    else:
        recv_msg(sockfd,name)

if __name__ =="__main__":
    main()
