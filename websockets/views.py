from django.shortcuts import render, redirect
from socket import * 

# Create your views here.
def index(request):
    return render(request, 'websockets/index.html')

def client(request):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', 8080))

    print("연결 확인")
    clientSocket.send('나는야 클라이언트', encode('utf-8'))

    print('메시지를 전송했습니다.')

    data = clientSocket.recv(1024)

    print('받은 데이터 : ', data.decode('utf-8'))
    return render(request, 'websockets/index.html')



def server(request):
    print('나는야 서버')
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 8080))
    # 클라이언트의 접속 기다렷
    serverSocket.listen(1)

    connectionSock, addr = serverSocket.accept()

    print(str(addr), '에서의 접속 확인')

    data = connectionSock.recv(1024)
    
    print('받은 데이터 : ', data.decode('utf-8'))

    connectionSock.send('I am a server.'.encode('utf-8'))

    print('메시지를 전송했습니다.')
    
    return render(request, 'websockets/index.html')
