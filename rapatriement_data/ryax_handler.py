import json
import paramiko
from scp import SCPClient


def handle(input_values: dict) -> None:
    print("Creating ssh key from file...")
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
        print(f"Uploading file {input_values.get('input_file')} to {input_values.get('ssh_user')}@{input_values.get('ssh_host')}:{input_values.get('remote_location')}")
        scp.put(
            input_values.get("input_file"),
            remote_path=input_values.get("remote_location"),
        )
    except Exception as e:
        print(
            f"Unexpected exception during bulk upload: {e}"
        )
    finally:
        client.close()



if __name__ == "__main__":
    input_json = {
        "ssh_pkey": "secret",
        "ssh_user": "secret",
        "ssh_host": "secret",
        "ssh_port": "secret",
        "input_file": "./test.txt",
        "remote_location": "test.txt",
    }
    with open("../secrets.txt") as f:
        secrets = json.load(f)
        for key in secrets:
            if key in input_json:
                input_json[key] = secrets[key]

    handle(input_json)
