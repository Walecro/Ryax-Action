#!/usr/bin/env python3

import subprocess

def handle(mod_in):
    subprocess.Popen(f"ssh {mod_in.get("sshname")}@{mod_in.get("ip")} {"./"+mod_in.get("exec")}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

 

