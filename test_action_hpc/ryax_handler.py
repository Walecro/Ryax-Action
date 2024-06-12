#!/usr/bin/env python3

import subprocess
 
def handle(mod_in):
    ssh = subprocess.Popen(["ssh","-T" ,mod_in.get("sshname")+"@"+mod_in.get("ip")], stdin=subprocess.PIPE stdout=subprocess.PIPE, stderr=subprocess.PIPE ,capture_output=True).communicate("./"+mod_in.get("exec"))
 

