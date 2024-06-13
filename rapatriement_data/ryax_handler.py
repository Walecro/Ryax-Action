#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    
    # Détails de connexion SSH
    hostname = mod_in.get("ip")
    username = mod_in.get("sshname")
    out_name = mod_in.get("outname")

    err = ""
     # Fichier à exécuter et fichier à lire
    remote_rsult_path = f"/home/{username}/{out_name}"

    try:
        # Commande pour se connecter en SSH et exécuter le .exe
        ssh_command_execute = f"/bin/scp {username}@{hostname}:{remote_rsult_path} {username}@10.22.3.99:/home/{hostname}/{remote_rsult_path}"
        process_execute = subprocess.Popen(ssh_command_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process_execute.communicate()

        if process_execute.returncode != 0:
            err = (f"Erreur lors de la récupération : {stderr.decode().strip()}")
        else:
            err = "ok"

    except Exception as e:
        err = (f"Erreur : {e}")

    return ({"err":err})







 

