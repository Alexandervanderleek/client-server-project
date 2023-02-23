import socket
import os
import math
 
IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024

 
def main():
    print("[STARTING] Server is starting.")
    print(IP)
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
 
    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")
 
    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        conn.send('OK'.encode())
        

        while True:
            received = conn.recv(SIZE).decode()
            data_split = received.split(",")
            match data_split[0]:
                case "upload":
                    url = ""
                    match data_split[1]:
                        case "open":
                            url += "./open/"
                        case "closed":
                            url += "./closed/"
                    
                    match data_split[2]:
                        case "client":
                            url +=  data_split[4] + "/"
                        case "key":
                            url +=  data_split[3] + "/"


                    url = url + data_split[6]
                    os.makedirs(os.path.dirname(url), exist_ok=True)
                    with open(url, "wb") as f:
                        for x in range(math.ceil(int(data_split[5])/SIZE)):
                            bytes_read =conn.recv(SIZE)
                            f.write(bytes_read)
                        f.close()
                case "view":
                    for subdir, dirs, files in os.walk('./open/'):
                        for file in files:
                            if(len(subdir)>7):
                  
                                if(data_split[2] in subdir):
                                    print(file + " [d]")
                                elif(data_split[1] in subdir and data_split[1] != ""):
                                    print(file + " [d]")
                                else:
                                    if(data_split[1]==""):
                                        print(file + "[x]" +"clientOnly restriction")
                                    else:
                                        print(file + "[x]" +"key restriction")
                            else:
                                print(file + "[d]")
if __name__ == "__main__":
    main()