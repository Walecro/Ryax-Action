import json
import paramiko
from scp import SCPClient


def handle(input_values: dict) -> None:
    pkey = paramiko.RSAKey.from_private_key_file(input_values.get("ssh_pkey"))

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            input_values.get("ssh_host"),
            input_values.get("ssh_port"),
            username=input_values.get("ssh_user"),
            pkey=pkey,
        )
        scp = SCPClient(client.get_transport())
        out = f"Uploading file {input_values.get('input_file')} to {input_values.get('ssh_user')}@{input_values.get('ssh_host')}:{input_values.get('remote_location')}"
        scp.put(
            input_values.get("input_file"),
            remote_path=input_values.get("remote_location"),
        )
    except Exception as e:
        
            err= f"Unexpected exception during bulk upload: {e}"
        
    finally:
        client.close()
    
    return {"err":err,"out": out}


