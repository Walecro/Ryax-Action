#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""

    #On récup les noeuds libres 
    cmdromeo = 'sinfo -h | grep idle'
    cmddgx = "nvidia-smi"
    cmdjuliet = ""

    list_server_ok = [["dgx1.univ-reims.fr",1],["romeologin1.univ-reims.fr",1],["romeologin2.univ-reims.fr",1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #"Ping" des machines
    for server_and_ok in list_server_ok:
        #Tentative de co SSH avec un timeout de 5s, si on y arrive pas, la machine est considérée injoinable 
        try:
            client.connect(
            server_and_ok[0],
            22,
            username=mod_in.get("ssh_user"),
            pkey=pkey,
            timeout=5
        )
        except (TimeoutError , ConnectionRefusedError) as e: 
            err += str(e)
            server_and_ok[1] = 0
        
        client.close()

    #Si les deux noeuds de login de romeo sont dispos pas besoin du 2eme
    list_server_ok.pop()

    #Questionnement sur les ressources disponibles
    for server_and_ok in list_server_ok:
        if(server_and_ok[1] == 1 ):
            client.connect(
            server_and_ok[0],
            22,
            username=mod_in.get("ssh_user"),
            pkey=pkey,
        )
        if "romeo" in server_and_ok[0]:
            r_stdin, r_stdout, r_stderr = client.exec_command(cmdromeo)
        elif "dgx" in server_and_ok[0]:
            d_stdin, d_stdout, d_stderr = client.exec_command(cmddgx)

        client.close()

    

    r_out = r_stdout.readlines()
    d_out = d_stdout.readlines()
    
    ret = r_out + d_out    

    return({"err":"osekour","res_DEBUG":str(ret)})
