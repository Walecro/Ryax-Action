#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    
    # Détails de connexion SSH
    hostname = mod_in.get("ip")
    username = mod_in.get("sshname")
    err = ""
    out = ""
    # Fichier à exécuter et fichier à lire
    remote_exe_path = mod_in.get("exec")

    try:
        # Commande pour se connecter en SSH et exécuter le .exe
        ssh_command_execute = f"ssh {username}@{hostname} '/home/{username}/{remote_exe_path}'"
        process_execute = subprocess.Popen(ssh_command_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process_execute.communicate()

        if process_execute.returncode != 0:
            err = (f"Erreur lors de l'exécution du .exe : {stderr.decode().strip()}")
        else:
            out = "ok"

    except Exception as e:
        err = (f"Erreur : {e}")

    return ({"output":out,"err":err})







 

