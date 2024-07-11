#!/usr/bin/env python3

import paramiko
 
def main():
    
    pkey = paramiko.RSAKey.from_private_key_file("../id_rsa")
    err = ""
    res = "gpu"
    #On récup les noeuds libres 
    cmdromeo = f'sinfo -h | grep idle | grep -w {res}'
    cmddgx = "nvidia-smi"
    cmdsbatchromeo = f'echo "#!/bin/bash\n#SBATCH --time=00:01:00\n#SBATCH --nodes=1 \n#SBATCH --cores=2\n#SBATCH --output=data.out\nmake\nsrun ./test > out.txt" > batch.sh'
    cmdexecromeo = 'sbatch batch.sh'

    cmdexecdgx = "nvidia-docker exec" 

    #Remplacer par un dict ? clé = nom ? 
    #Serait bien d'avoir un service externe à ping pour avoir la liste si c'est mis à jour 
    list_server_ok = [["romeologin1.univ-reims.fr",1],["romeologin2.univ-reims.fr",1],["dgx1.univ-reims.fr",1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Si on veut du temps sur CPU alors la DGX est inutile, à voir si ce système de pop ne peut pas être retiré plus tard
    if(res == "cpu"):
        list_server_ok.pop()
    #"Ping" des machines
    for server_and_ok in list_server_ok:
        #Tentative de co SSH avec un timeout de 5s, si on y arrive pas, la machine est considérée injoinable 
        try:
            client.connect(
            server_and_ok[0],
            22,
            username="alabille",
            pkey=pkey,
            timeout=5
        )
        except (TimeoutError , ConnectionRefusedError) as e: 
            err += str(e)
            server_and_ok[1] = 0
        
        client.close()

    print(list_server_ok)
    #Si les deux noeuds de login de romeo sont au même état pas besoin du 2eme
    if(list_server_ok[0][1] == list_server_ok[1][1]):
        list_server_ok.pop(1)

    print(list_server_ok)
    #Questionnement sur les ressources disponibles
    for server_and_ok in list_server_ok:
        if(server_and_ok[1] == 1 ):
            client.connect(
            server_and_ok[0],
            22,
            username="alabille",
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

    if(r_out):
        res_avail_romeo = int(r_out[0].split()[3])

    
    

    if(res_avail_romeo >= 1):
        client.connect(
            list_server_ok[0][0],
            22,
            username="alabille",
            pkey=pkey,
        )
        rb_stdin, rb_stdout, rb_stderr = client.exec_command(cmdsbatchromeo)
        rex_stdin, rex_stdout, rex_stderr = client.exec_command(cmdexecromeo)

        client.close()
    elif(res_avail_dgx >= 1):
        ret = "Assez de ressource DGX"
    else:
        ret = "Pas de ressource"


    err = r_stderr.readlines() + rb_stderr.readlines() + rex_stderr.readlines()

    print(err)

    
main()