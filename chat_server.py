"""
群聊聊天室
env:python 3.5
socket udp fork 练习
"""

from socket import *
import os

ADDR = ("0.0.0.0", 8812)
#存储用户{name:address}
user = {}

def do_login(sockfd,name,addr):
    if name in user:
        sockfd.sendto("该用户已存在".encode(),addr)
        return
    sockfd.sendto(b"OK",addr)

    #通知其他人
    msg = "欢迎%s进入聊天室" % name
    for i in user:
        sockfd.sendto(msg.encode(),user[i])
    #插入字典
    user[name] = addr

def do_chat(sockfd,name,text):
    msg = "%s : %s"%(name,text)
    for i in user:
        if i != name :
            sockfd.sendto(msg.encode(),user[i])



# 搭建udp网络
def main():
    # udp套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.bind(ADDR)
    pid = os.fork()

    if pid <0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员消息 "+msg
            sockfd.sendto(msg.encode(),ADDR)
    else:
        do_request(sockfd)

#退出
def do_quit(sockfd,name):
    msg = "%s 退出了聊天室"% name
    for i in user:
        if i!=name:
            sockfd.sendto(msg.encode(),user[i])
        else:
            sockfd.sendto(b"EXIT",user[i])
    del user[name]


# 请求处理函数
def do_request(sockfd):
    while True:
        data, addr = sockfd.recvfrom(1024)
        tem =data.decode().split(" ")#拆分请求
        #根据请求类型执行不同内容
        if tem[0]=="L":
            do_login(sockfd,tem[1],addr)#完成具体服务端登录工作
        elif tem[0] == "C":
            text = " ".join(tem[2:])#拼接消息内容
            do_chat(sockfd,tem[1],text)
        elif tem[0] == "Q":
            if tem[1] not in user:
                sockfd.sendto(b"EXIT",addr)
                continue
            do_quit(sockfd,tem[1])



main()