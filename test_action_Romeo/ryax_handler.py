#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        mod_in.get("ssh_host"),
        mod_in.get("ssh_port"),
        username=mod_in.get("ssh_user"),
        pkey=pkey,
    )
    
    cmd = f'echo "#!/bin/bash\n#SBATCH --time={mod_in.get("time")}\n#SBATCH --nodes={mod_in.get("nodes")} \n#SBATCH --output={mod_in.get("out_name")}\nsrun ls -a" >batch.sh''
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stderr.readlines():
       err += line

    stdin, stdout, stderr = client.exec_command('sbatch batch.sh > output.out')
    for line in stderr.readlines():
        err += line
    client.close()


    return({"err":"osekour"})
