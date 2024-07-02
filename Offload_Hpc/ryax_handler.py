#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""
    list_server_ok = [["dgx1.univ-reims.fr",1],["romeologin1.univ-reims.fr",1],["romeologin2.univ-reims.fr",1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #"Ping" des machines
    for server_and_ok in list_server_ok:

        try:
            client.connect(
            server_and_ok[0],
            22,
            username=mod_in.get("ssh_user"),
            pkey=pkey,
        )
        except (TimeoutError , ConnectionRefusedError) as e: 
            err += str(e)
            server_and_ok[1] = 0
        
        client.close()

    #Questionnement sur les ressources disponibles
    for server_and_ok in list_server_ok:
        if(server_and_ok[1] == 1 ):
            client.connect(
            server_and_ok[0],
            22,
            username=mod_in.get("ssh_user"),
            pkey=pkey,
        )

        
        client.close()

    cmdromeo = 'sinfo -h | grep idle'
    stdin, stdout, stderr = client.exec_command(cmdromeo)

    out = stdout.readlines()
    availnode = out.strip("\t")
    cmddgx = "nvidia-smi"
    
    print(availnode)
    

    for line in stderr.readlines():
        err += line
    client.close()


    return({"err":"osekour"})
