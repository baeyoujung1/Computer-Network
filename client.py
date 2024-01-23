#2021036835 배유정

from socket import *
import argparse
import threading


#host의 값은 레포트에 나와있는 방법을 이용해 연결 중인 공유기 주소로 바꿔준다.
host = '127.0.0.1'
port = 9999

lock = threading.Lock()

user_socket = socket(AF_INET, SOCK_STREAM)  
user_socket.connect((host, port))

arg = argparse.ArgumentParser()
arg.add_argument('user')
args = arg.parse_args()
users = args.user

print(f'[{users}] 접속')


# client의 socket 정보를 받는다.
def receive(user_socket, user):
    while 1:
        try:
            infor = user_socket.recv(1024)
        except:
            print("접속 해제")
            break
        infor = infor.decode()
        if not user in infor:
            print(infor)


# client의 메시지를 모두에게 전송한다.
def send(user_socket, user):
    while 1:
        infor = input()
        user_socket.sendall(infor.encode())
        if infor == "quit" or infor == 'q':
            break
    user_socket.close()


# thread를 통해 receive와 send를 수행한다.
receiving = threading.Thread(target=receive, args=(user_socket, users,))
receiving.start()
sending = threading.Thread(target=send, args=(user_socket, users))
sending.start()

user_socket.sendall(users.encode())
