#!/usr/bin/env python3

import paramiko
 
def handle(input_values : dict) -> None:
    
    cmd=input_values.get("ssh_cmd")

    print("Creating ssh key from file...")
    pkey = paramiko.RSAKey.from_private_key_file(input_values.get("ssh_pkey"))

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        input_values.get("ssh_host"),
        input_values.get("ssh_port"),
        username=input_values.get("ssh_user"),
        pkey=pkey,
    )
    print(f"Executing command '{cmd}'")
    stdin, stdout, stderr = client.exec_command(cmd)

    stdout_output=""
    stdout = stdout.readlines() if stdout else []
    for line in stdout:
        stdout_output += line
    if stdout_output != "":
        print("STDOUT===> "+stdout_output)

    stderr_output=""
    stderr = stderr.readlines() if stderr else []
    for line in stderr:
        stderr_output += line
    if stderr_output != "":
        print("STDERR===> "+stderr_output)

    client.close()

    return { "stdout": str(stdout_output), "stderr": str(stderr_output)}








 

