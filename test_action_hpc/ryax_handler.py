#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    
    # Détails de connexion SSH
    hostname = mod_in.get("ip")
    username = mod_in.get("sshname")
    err = ""
    # Fichier à exécuter et fichier à lire
    remote_exe_path = mod_in.get("exec")
    output_file_path = "/home/alabille/"+mod_in.get("outname")+ " alabille@10.22.3.99:/home/alabille/rapat.txt"

    try:
        # Commande pour se connecter en SSH et exécuter le .exe
        #ssh_command_execute = f"ssh {username}@{hostname} '{remote_exe_path}'"
        #process_execute = subprocess.Popen(ssh_command_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = process_execute.communicate()

        #if process_execute.returncode != 0:
        #    err = (f"Erreur lors de l'exécution du .exe : {stderr.decode().strip()}")


        # Commande pour récupérer le contenu du fichier de sortie
        ssh_command_scp = f"scp alabille@dgx1.univ-reims.fr:/home/alabille/test.txt alabille@10.22.3.99:/home/alabille/"
        process_scp = subprocess.Popen(ssh_command_scp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process_scp.communicate()

        if process_scp.returncode != 0:
            err = (f"Erreur lors de la lecture du fichier de sortie : {stderr.decode().strip()}")
        err = stdout
    except Exception as e:
        err = (f"Erreur : {e}")

    return ({"output":open("/home/alabille/rapat.txt","r"),"err":err})







 

