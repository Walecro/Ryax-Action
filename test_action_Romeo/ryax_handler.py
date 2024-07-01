#!/usr/bin/env python3

import paramiko
 
def handle(mod_in):
    
    pkey = paramiko.RSAKey.from_private_key_file(mod_in.get("ssh_pkey"))

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            mod_in.get("ssh_host"),
            mod_in.get("ssh_port"),
            username=mod_in.get("ssh_user"),
            pkey=pkey,
        )
        stdin, stdout, stderr = client.exec_command("cat")
    except Exception as e:
        print(
            f"Unexpected exception during bulk upload: {e}"
        )
    finally:
        client.close()


    stdout_output = ""
    stdout.readlines()
    for line in stdout:
        stdout_output += line

    return({"err":stdout_output})
