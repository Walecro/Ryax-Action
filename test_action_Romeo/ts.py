#!/usr/bin/env python3

import paramiko
 

    
pkey = paramiko.RSAKey.from_private_key_file("./id_rsa")
err = ""
            
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    "romeologin1.univ-reims.fr",
    22,
    "alabille",
    pkey=pkey,
    )
stdin, stdout, stderr = client.exec_command('echo "#!/bin/bash\n#SBATCH --time=00:01:00\n#SBATCH --nodes=2 \nsrun ls -a" >batch.sh')
stdin, stdout, stderr = client.exec_command('sbatch batch.sh > output.out')

print(stdout.readlines(),stderr.readlines())
client.close()
