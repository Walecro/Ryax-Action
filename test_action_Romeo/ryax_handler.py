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
    stdin, stdout, stderr = client.exec_command('echo "#!/bin/bash\n#SBATCH --time=00:01:00\n#SBATCH --nodes=2 \nsrun ls -a" >batch.sh')
    stdin, stdout, stderr = client.exec_command('sbatch batch.sh > output.out')
    client.close()

    for line in stderr.readlines():
        err += line

    return({"err":str(err)})
