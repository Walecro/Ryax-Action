#!/usr/bin/env python3

def handle(mod_in):

    with open(mod_in.get("script"), 'r') as file:
        data = file.read().replace('\n', '')
    return({"hpcparam":data})
