#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""

    #On récup les noeuds libres 
    cmdromeo = f'sinfo -h | grep idle | grep -w {mod_in.get("resource")}'
    cmddgx = "nvidia-smi"
    cmdsbatchromeo = f'echo "#!/bin/bash\n#SBATCH --time={mod_in.get("time")}\n#SBATCH --nodes={mod_in.get("nodes")} \n#SBATCH --output={mod_in.get("out_name")}\nsrun {mod_in.get("exec")}" > batch.sh'
    cmdexecromeo = 'sbatch batch.sh > output.out'

    cmdexecdgx = "nvidia-docker exec" 

    #Remplacer par un dict ? clé = nom ? 
    #Serait bien d'avoir un service externe à ping pour avoir la liste si c'est mis à jour 
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

    #Si les deux noeuds de login de romeo sont au même état pas besoin du 2eme
    if(list_server_ok[1][1] == list_server_ok[2][1]):
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
            r_out = r_stdout.readlines()

        elif "dgx" in server_and_ok[0]:
            d_stdin, d_stdout, d_stderr = client.exec_command(cmddgx)
            d_out = d_stdout.readlines()

        client.close()

    if(r_out):
        res_avail_romeo = r_out[0].split()[3]

    res_avail_dgx = 0
    

    if(int(res_avail_romeo) >= mod_in.get("nodes")):
        ret = "Assez de ressource Romeo"
    elif(res_avail_dgx >= mod_in.get("nodes")):
        ret = "Assez de ressource DGX"
    else:
        ret = "Pas de ressource"

    err = r_stderr + d_stderr

    return({"err":e,"res_DEBUG":ret})
