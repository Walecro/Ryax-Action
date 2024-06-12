#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    print(mod_in.get("sshname")+"@"+mod_in.get("ip"))
    ssh = subprocess.Popen("/bin/ssh",mod_in.get("sshname")+"@"+mod_in.get("ip"), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    capture_output=True)
    ssh.communicate("./"+mod_in.get("exec"))
    ssh.wait()

 

