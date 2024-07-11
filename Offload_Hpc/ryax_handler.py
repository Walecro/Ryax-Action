#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""

    #On récup les noeuds libres 
    cmdromeo = f'sinfo -h | grep idle | grep -w {mod_in.get("resource")}'
    cmddgx = "nvidia-smi"
    cmdsbatchromeo = f'echo "#!/bin/bash\n#SBATCH --time={mod_in.get("time")}\n#SBATCH --cores={mod_in.get("cores")} \n#SBATCH --nodes={mod_in.get("nodes")} \nmake\nsrun ./{mod_in.get("exec")} > {mod_in.get("name_file")}" > batch.sh'
    cmdexecromeo = 'sbatch batch.sh '

    #Cela ne convient pas au système en place sur la DGX, mais actuellement j'ai pas les droits alors on va dire que
    cmdexecdgx = f"make && ./{mod_in.get("exec")} > {mod_in.get("name_file")}" 

    #Remplacer par un dict ? clé = nom ? 
    #Serait bien d'avoir un service externe à ping pour avoir la liste si c'est mis à jour 
    list_server_ok = [["romeologin1.univ-reims.fr",1],["romeologin2.univ-reims.fr",1],["dgx1.univ-reims.fr",1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Si on veut du temps sur CPU alors la DGX est inutile, à voir si ce système de pop ne peut pas être retiré plus tard
    if(mod_in.get("resource") == "cpu"):
        list_server_ok.pop()
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
    if(list_server_ok[0][1] == list_server_ok[1][1]):
        list_server_ok.remove(["romeologin2.univ-reims.fr",1])

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

    res_avail_romeo = 0 
    res_avail_dgx = 0

    #On récup l'entier des nodes dispos pour la ressource
    if(r_out):
        res_avail_romeo = int(r_out[0].split()[3])



    if(res_avail_romeo >= mod_in.get("nodes")):
        #Exec sur ROMEO
        client.connect(
            list_server_ok[0][0],
            22,
            username="alabille",
            pkey=pkey,
        )
        rb_stdin, rb_stdout, rb_stderr = client.exec_command(cmdsbatchromeo)
        rex_stdin, rex_stdout, rex_stderr = client.exec_command(cmdexecromeo)
    elif(res_avail_dgx >= mod_in.get("nodes") and mod_in.get("resource") == "gpu"):
        #Exec sur DGX
        client.connect(
            list_server_ok[1][0],
            22,
            username="alabille",
            pkey=pkey,
        )
        client.exec_command(cmdexecdgx)
    else:
        ret = "Pas de ressource"

    client.close()


    err = r_stderr.readlines() + d_stderr.readlines() + rb_stderr.readlines() + rex_stderr.readlines()

    return({"err":"osef","res_DEBUG":ret})
