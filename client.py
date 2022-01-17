import socket

host = "www.google.com"

#https://www.geeks3d.com/hacklab/20190110/python-3-simple-http-request-with-the-socket-module/
# SOURCE WHERE WE GOT THIS!!!!
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket connected successfully")
except socket.error as err:
    print("Socket conenction failed with error: %s" %(err))

# port 80 is the default for socket
port = 80

try:
    host_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("error getting host ip")
    sys.exit()

# conencting to the server
s.connect((host_ip, port))
request = "GET / HTTP/1.1\r\nHost: %s\n\n" %(host) 
s.send(bytes(request,'utf-8'))
result = s.recv(10000)
while (len(result) > 0):
    print(result)
    result = s.recv(10000)   

# DO WE DISCONNECT??