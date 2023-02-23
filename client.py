import socket
import os
 


#192.168.1.118
SIZE = 1024
 
def main():
    while True:
        IP = input("Enter IP Address for the server:\n")
        PORT = input("Enter PORT on server:\n")
        ADDR = (IP,int(PORT))
        client=None
        response=""
        connectionError=False


        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            response = client.recv(SIZE).decode()
        except:
            connectionError = True



        if response=="OK" and not connectionError:
            print("\nSuccesfully connected to server!")
            command = input("Type help for a list of commands.\n")
            while True:
                match command:
                    case "help":
                        print("view -> see all files on our server")
                        print("upload -> upload a new file to our server")
                        print("download -> download a file from our server")
                        print("quit -> exit the application" )
                        print("help -> get list of commands" )
                        command = input("")
                    case "upload":
                        while True:
                            file = input("Enter path of file for upload.\n")
                            if(os.path.isfile(file)):
                                visbilityFinal = None
                                downloadabilityFinal = None
                                key=""
                                print("- FOUND VALID FILE -")
                                visbility = input("Is this file visibile to all. (y/n):\n")
                                while True:
                                    if(visbility != "y" and visbility != "n" and visbility != "yes" and visbility != "no"):
                                        visbility = input("Invalid response. Try again (y/n)\n")
                                    else:
                                        if(visbility == "y" or visbility=="yes"):
                                            visbilityFinal = "open"
                                        else:
                                            visbilityFinal = "closed"
                                        break
                                downloadability = input("Is this file downloadable for all. (y/n).\n")
                                while True:
                                    if(downloadability != "y" and downloadability != "n" and downloadability != "yes" and downloadability != "no"):
                                        downloadability = input("Invalid response. Try again (y/n).\n")
                                    else:
                                        if(downloadability == "y" or downloadability=="yes"):
                                            downloadabilityFinal = "open"
                                            break
                                        else:
                                            downloadability = input("Specify restriction type. (clientOnly/key):\n")
                                            while True:
                                                match downloadability:
                                                    case 'key':
                                                        invalid = ["/","<",">",":",'"','\\', "|","?","*"]
                                                        downloadabilityFinal = "key"
                                                        key = input("Enter your secret key.\n")
                                                        while True:
                                                            found = False
                                                            for item in invalid:
                                                                if(key.find(item)>-1):
                                                                    found = True
                                                                    key = input("Invalid character in secret key. Please re-enter.\n")
                                                                    break

                                                            if(found==False):

                                                                break
                                                        
                                                        break
                                                    case 'clientOnly':
                                                        downloadabilityFinal = "client"
                                                        break
                                                    case _:
                                                        downloadability = input("Invalid response. Try again (clientOnly/key).\n")
                                            break
                                
                                
                                
                                toSend = "upload,"+visbilityFinal+","+downloadabilityFinal+","+key+","+ str(socket.gethostbyname(socket.gethostname())) +","+ str(os.path.getsize(file))+","+os.path.basename(file)
                                client.send(toSend.encode())

                             
                                f = open(file,'rb')
                                l = f.read(1024)
                                while (l):
                                    client.send(l)
                                    l = f.read(1024)
                                f.close()

                                command = input("Type help for a list of commands.\n")
                                break
                            else:
                                next = input("Could not find that file. Try again (y/n):\n")
                                while True:
                                    if(next != "y" and next != "n" and next != "yes" and next != "no"):
                                        next = input("Invalid response. Try again (y/n).\n")
                                    break
                                    
                                if next == 'n' or next == 'no':
                                    command = input("Type help for a list of commands.\n")
                                    break
                    
                    case "view":

                        next = input("Do you have a secret key? (y/n).\n")
                        key = ""
                        while True:
                            if(next != "y" and next != "n" and next != "yes" and next != "no"):
                                next = input("Invalid response. Try again (y/n).\n")
                            break
                        if(next == "y" or next =="yes"):
                            key = input("Enter your secret key\n")


                        client.send(("view,"+key+","+str(socket.gethostbyname(socket.gethostname()))).encode())
                        command = input("Type help for a list of commands.\n")

                    case "quit":
                        client.close()
                        exit()
                    case _:
                        print("Could not find that command.")
                        command = input("Type help for a list of commands.\n")
        else:
            print('Could not succesfully connect to server.')
            next_move=input("Would you like to retry? (y/n):\n")
            if next_move != 'y' and next_move != 'yes':
                exit()

 
if __name__ == "__main__":
    main()