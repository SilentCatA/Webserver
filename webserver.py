import socket

HOST = ""
PORT = 8080

def createServer(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    return server

def readRequest(Server):
    request = ""
    while (request == ""):
        client, address = Server.accept()
        print(str(address) + " connected to server")

        client.settimeout(1)
        try:
            temp = client.recv(1024).decode()
            while(temp):
                request = request+temp
                temp = client.recv(1024).decode()
        except socket.timeout:
            print("[time out]")
    return client, request

def moveIndex(Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
    Client.send(header.encode("utf-8"))

def sendIndex(Client):
    file = open("index.html", "rb")
    content = file.read()
    header ="""HTTP/1.1 200 OK
Content-Length: %d

"""%len(content)
    header = header +content.decode()
    Client.send(header.encode("utf-8"))

def homePage(Client, Server, Request):
    if "GET /index.html HTTP/1.1" in Request:
        sendIndex(Client)
        Server.close()
    elif "GET / HTTP/1.1" in Request:
        moveIndex(Client)
        Server.close()
        Server = createServer(HOST, PORT)
        Client, Request = readRequest(Server)
        print(Request)
        print("----------------------------------\n")
        homePage(Client, Server, Request)

def checkPass(Request): 
    if "POST" in Request and "HTTP/1.1" in Request and "uname=admin&psw=admin" in Request:
        print("Login success")
        return True
    return False

def sendImg(Client, NameImg):
	with open(NameImg, 'rb') as f:
		L = f.read()
		header ="""HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)

		header =  header.encode("utf-8") + L
		Client.send(header)

def moveInfo(Server, Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/info.html

"""
	Client.send(header.encode("utf-8"))


def sendFileInfo(Client): 
	f = open ("info.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	header += L.decode()
	Client.send(header.encode("utf-8"))

def sendInfo(Server, Client):
    Server.close()
    Server = createServer(HOST, PORT)
    Client, Request = readRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /info.html HTTP/1.1" in Request:
        sendFileInfo(Client)
    Server.close()
    
    Server = createServer(HOST, PORT)
    Client, Request = readRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /image1.jpg HTTP/1.1" in Request:
        sendImg(Client, "image1.jpg")
    if "GET /image2.jpg HTTP/1.1" in Request:
        sendImg(Client, "image2.jpg")

    Client, Request = readRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /image1.jpg HTTP/1.1" in Request:
        sendImg(Client, "image1.jpg")
    if "GET /image2.jpg HTTP/1.1" in Request:
        sendImg(Client, "image2.jpg")
    Server.close()

def move404(Server, Client): 
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/404.html

"""
	Client.send(header.encode("utf-8"))
	Server.close()

def sendFile404(Client): 
	f = open ("404.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L) 

	header += L.decode()
	Client.send(header.encode("utf-8"))

def send404(Server, Client): 
	Server = createServer("localhost", 8080)
	Client, Request = readRequest(Server)
	print("HTTP Request: ")
	print(Request)
	if "GET /404.html HTTP/1.1" in Request:
		sendFile404(Client)
	Server.close()

def sendPageDownload(Client):
    f = open ("files.html", "rb")
    L = f.read()
    header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
    header += L.decode()
    Client.send(header.encode("utf-8"))


def movePageDownload(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/files.html

"""
    Client.send(header.encode("utf-8"))

def sendFileDownload(client, server, FileName):
    f = open(FileName, "rb")

    header ="""HTTP/1.1 200 OK
Content-Description: File Transfer
Content-Type: application/octet-stream
Expires: 0
Cache-Control: must-revalidate, post-check=0, pre-check=0
Pragma: public
Content-Disposition: attachment; filename="%s"
Content-Transfer-Encoding: chunked

"""%(FileName)

    client.send(header.encode("utf-8"))
    CHUNK_SIZE = 1024*8
    while True:
        data = f.read(CHUNK_SIZE)
        len_data = len(data)
        #client.send(hex(len_data).encode("utf-8"))
        client.send(data)
        if(len_data == 0):
            print("Download finished")
            break
    client.shutdown(socket.SHUT_RDWR)
    server.close()



def handleDownload(server, client):
    server.close()
    server = createServer(HOST, PORT)
    client, request = readRequest(server)
    print("HTTP Request: ")
    print(request)
    print("----------------------------------\n")
    if "GET /files.html HTTP/1.1" in request:
        sendPageDownload(client)
    server.close()

def clicked(Request):
    if "POST" in Request:
        return True
    return False


server = createServer(HOST, PORT)
client, request = readRequest(server)
print(request)
print("----------------------------------\n")
homePage(client, server, request)

server = createServer(HOST, PORT)
client, request = readRequest(server)
print(request)
print("----------------------------------\n")
loginSuccess = checkPass(request)
if(loginSuccess):
    moveInfo(server, client)
    sendInfo(server, client)
    #handle download
    server = createServer(HOST, PORT)
    client, request = readRequest(server)
    print(request)
    print("----------------------------------\n")
    if(clicked(request)):
        movePageDownload(server, client)
        handleDownload(server, client)
        while True:
            server = createServer(HOST, PORT)
            client, request = readRequest(server)
            print(request)
            print("----------------------------------\n")
            if "GET /exit HTTP/1.1" in request:
                print("exited")
                break
            if "GET /file_1 HTTP/1.1" in request:
                sendFileDownload(client, server,"pdf/Chapter_1.pdf")
            if "GET /file_2 HTTP/1.1" in request:
                sendFileDownload(client, server,"pdf/Chapter_2.pdf")
            if "GET /file_3 HTTP/1.1" in request:
                sendFileDownload(client, server,"pdf/Chapter_3.pdf")
            if "GET /file_4 HTTP/1.1" in request:
                sendFileDownload(client, server,"pdf/Chapter_4.pdf")
            if "GET /file_5 HTTP/1.1" in request:
                sendFileDownload(client, server,"pdf/Chapter_5.pdf")
        server.close()


else:
        move404(server, client)
        send404(server, client)
print("end")