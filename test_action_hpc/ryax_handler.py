#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    
    # Détails de connexion SSH
    hostname = mod_in.get("ip")
    username = mod_in.get("sshname")

    # Fichier à exécuter et fichier à lire
    remote_exe_path = mod_in.get("exec")
    output_file_path = "/home/alabille/"+mod_in.get("outname") 

    try:
        # Commande pour se connecter en SSH et exécuter le .exe
        ssh_command_execute = f"ssh {username}@{hostname} '{remote_exe_path}'"
        process_execute = subprocess.Popen(ssh_command_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process_execute.communicate()

        if process_execute.returncode != 0:
            print(f"Erreur lors de l'exécution du .exe : {stderr.decode().strip()}")
        else:
            print("Exécution du .exe réussie.")

        # Commande pour récupérer le contenu du fichier de sortie
        ssh_command_scp = f"scp {username}@{hostname}:{output_file_path} {username}@10.22.3.99:{output_file_path}"
        process_scp = subprocess.Popen(ssh_command_scp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process_scp.communicate()

        if process_scp.returncode != 0:
            print(f"Erreur lors de la lecture du fichier de sortie : {stderr.decode().strip()}")
        else:
            print("Contenu du fichier de sortie :")
            print(open("./test.txt","r").read())

    except Exception as e:
        print(f"Erreur : {e}")

    return ({"output":open("/home/alabille/test.txt","r")})







 

