#!/usr/bin/env python3
import socket
import time
import sys
import multiprocessing

#define address & buffer size
HOST = ""
PORT = 8002
BUFFER_SIZE = 1024         

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print(f'Failed to create socket. Error code: {err[0]} , Error message : {err[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def client(conn, payload):
    try:
        #define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        #payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 4096

        #make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
            conn.send(data)
            print("data length sent to client: ", len(data))
        print(full_data)
        print("SENDING TO CLIENT")
        time.sleep(0.5)
        

    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
        #conn.sendall(full_data)
        conn.close()
        print("CONNECTION CLOSED")
        

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        try:
            s.bind((HOST, PORT))
        except socket.error as err:
            print('Bind failed. Message: ', err)
            sys.exit()
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            p1 = multiprocessing.Process(target=client, args=(conn, full_data))
            #client(conn, full_data)
            p1.start()
            p1.join()
            
            
            
            #conn.sendall(full_data)
            #conn.close()


if __name__ == "__main__":
    main()