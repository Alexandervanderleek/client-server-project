import socket
import os
import math
from _thread import *
 
#SETTING BUFFER SIZE AND IP AND PORT FOR SERVER

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024

 
def main():
    print("[STARTING] Server is starting.")
    print(IP)

    #Create our server bind the ADDR and set a waiting q of 5
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    

    #function for creating new threads with connection variable
    def new_thread_client(conn):

         #Accept a connection and send a OK response to the client
        conn.send('OK'.encode()) 

        #our while loop for taking client commands
        while True:

            #accept client commands, create a array of 'header' style data
            received = conn.recv(SIZE).decode()
            data_split = received.split(",")
            
            #match first client header data, dictating the clients command
            match data_split[0]:

                #UPLOAD COMMAND CASE
                #This case allows clients to upload files with visibility options of open or closed and
                #downloadability options of client specific restriction and secret key based
                #confirmation done through checking of file byte size

                case "upload":
                    try:
                        #Build out a file pathname based on file privacy options (found in header array)
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

                        #our final file pathname (where file to be stored)
                        url = url + data_split[6]
                        
                        #Checking for if that file already exists and sends error with error code
                        if(os.path.isfile(url)):
                            conn.send('ERROR,FILE WITH THAT NAME EXITS'.encode())
                        #otherwise build the file at the pathname (taking in binary of file)
                        else:
                            os.makedirs(os.path.dirname(url), exist_ok=True)
                            with open(url, "wb") as f:
                                for x in range(math.ceil(int(data_split[5])/SIZE)):
                                    bytes_read =conn.recv(SIZE)
                                    f.write(bytes_read)
                                f.close()
                            
                            #check that size of file built is same as size of file on client side, data from header
                            if data_split[5] == str(os.path.getsize(url)):
                                conn.send('OK'.encode())
                            else:
                                os.remove(url)
                                conn.send('ERROR,NOT ALL OF FILE RECEIVED'.encode())
                    except:
                        conn.send('ERROR,SOMETHING HAS GONE WRONG'.encode())


                #VIEW COMMAND CASE
                #This case allows clients to see all of there files they have access to "non-visible" and "visible"
                #including files visible but not downloadable
                case "view":

                    try:
                        downloadable=""

                        #Go through all files in open folder (files visibles)
                        for subdir, dirs, files in os.walk('./open/'):
                            for file in files:

                                #if it is a download protected file
                                if(len(subdir)>7):

                                    #check if you have correct ip/key to download file
                                    if(data_split[2] in subdir):
                                        downloadable+=(file+ "/y/client,")
                                    elif(data_split[1] in subdir and data_split[1] != ""):
                                        downloadable+=(file+ "/y/key,")
                                    else:
                                        if("-client" in subdir):
                                            downloadable+=(file + "/n/client,")
                                        else:
                                            downloadable+=(file + "/n/key,")
                                else:
                                    downloadable+=(file + "/y/,")

                        #Go through all files in closed folder that might be yours (files not visible to all)
                        for subdir, dirs, files in os.walk('./closed/'):
                            for file in files:
                                if(len(subdir)>7):
                                    #check if you have correct ip/key to download file
                                    if(data_split[2] in subdir):
                                        downloadable+=(file+ "/y/client,")
                                    elif(data_split[1] in subdir and data_split[1] != ""):
                                        downloadable+=(file+ "/y/key,")
                
                                


                        #send back all files and download status and restriction types
                        conn.send(downloadable[:-1].encode())

                    except:
                        conn.send("ERROR".encode())
                

                
                #Download command case
                #enter specifications for file requested and download it
                case "download":
                    try:
                        #Build the pathname for where file is to be downloaded
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

                        #our final file pathname (where file should be)
                        url = url + data_split[5]


                        #Checking for if that file exists and sends error with error code if not
                        if(os.path.isfile(url)):
                            conn.send(str(os.path.getsize(url)).encode())

                            f = open(url,'rb')
                            l = f.read(1024)
                            while (l):
                                conn.send(l)
                                l = f.read(1024)
                            f.close()

                        #otherwise error no file found
                        else:
                            restriction = ""
                            if(data_split[2]=="client"):
                                restriction = "with "+data_split[2] + " of "+data_split[4]
                            elif(data_split[2]=="key"):
                                restriction = "with "+data_split[2] + " of "+data_split[3]
                            conn.send(('ERROR,File not in '+data_split[1]+ ' visbility folder '+restriction).encode())
                    except:
                        conn.send('ERROR,SOMETHING HAS GONE WRONG'.encode())



                #QUIT COMMAND CASE
                case "quit":
                    conn.close()
                    break
    
    #main while loop constantly accept connections and allows for multiple threads
    while True:
        conn, addr = server.accept()
        start_new_thread(new_thread_client,(conn,))
    
        


if __name__ == "__main__":
    main()