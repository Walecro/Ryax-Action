#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))
    err = ""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            mod_in.get("ssh_host"),
            mod_in.get("ssh_port"),
            username=mod_in.get("ssh_user"),
            pkey=pkey,
        )
        stdin, stdout, stderr = client.exec_command("ls -a")
    except Exception as e:
        err = f"Unexpected exception during bulk upload: {e}"
    finally:
        client.close()


    return({"err":str(err)})
