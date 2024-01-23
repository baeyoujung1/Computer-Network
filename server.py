#2021036835 배유정

from socket import *
import threading


#host의 값은 레포트에 나와있는 방법을 이용해 연결 중인 공유기 주소로 바꿔준다.
host = '127.0.0.1'
port = 9999

lock = threading.Lock()

serv = socket(AF_INET, SOCK_STREAM)
serv.bind((host, port))
serv.listen(3)

users = {}


#client가 입력한 메시지를 받고 알맞게 처리한다.
def get(user_socket, address, user):
    while 1:                                 
        infor = user_socket.recv(1024)
        mes = infor.decode() 

        if mes == "quit" or mes == 'q' :                          
            message = f'[{user.decode()}] 접속 종료'
            print(message)
            break
        mes = "[%s] %s"%(user.decode(), mes)
        print(mes)
        for value in users.values():
            try:
                value.sendall(mes.encode())
            except:
                print("비정상적인 접근")
                
    lock.acquire()
    del users[user]
    lock.release()
    
    print('[%d]명의 사용자 접속 중'%len(users))
    user_socket.close()


#thread를 통해 get 함수를 실행한다.
while True:
    user_socket, address = serv.accept()
    user = user_socket.recv(1024)
    
    lock.acquire()
    users[user] = user_socket
    lock.release()

    print(f'[{user.decode()}] 접속')
    print('[%d]명의 사용자 접속 중'%len(users))

    thread = threading.Thread(target=get, args=(user_socket, address,user))
    thread.start()
