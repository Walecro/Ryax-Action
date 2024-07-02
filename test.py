#!/usr/bin/env python3

import paramiko
 
def main():
    err = ""
    pkey = paramiko.RSAKey.from_private_key_file("C:\\Users\\Alexx\\.ssh\\id_rsa")

    #Partie de "ping" des machines disponibles 
    list_server_ok = [["dgx1.univ-reims.fr",1],["romeologin1.univ-reims.fr",1],["romeologin2.univ-reims.fr",1],["10.255.255.1",1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for server_and_ok in list_server_ok:

        try:
            client.connect(
                server_and_ok[0],
                22,
                username="alabille",
                pkey=pkey,
                timeout = 10
            )
        except (TimeoutError , ConnectionRefusedError) as e: 
            err += str(e)
            server_and_ok[1] = 0
        
        client.close()

    
    cmdromeo = 'sinfo -h | grep idle'
    #stdin, stdout, stderr = client.exec_command(cmdromeo)

    #out = stdout.readlines()
   # out = list(filter(lambda x: "long" in x, out))

    cmddgx = "nvidia-smi"


    
    #for i in out:
    #    availnode = i.split()
    #    print(availnode[3])



if __name__ == '__main__':
    main()