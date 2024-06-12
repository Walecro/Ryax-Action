#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    subprocess.Popen("/bin/ssh",mod_in.get("sshname")+"@"+mod_in.get("ip"), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    capture_output=True).communicate("./"+mod_in.get("exec"))

 

