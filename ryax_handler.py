#!/usr/bin/env python3

def handle(mod_in):
    return {"ret": mod_in[0] + 2} 

if __name__ == "__main__":
    handle({"test": 2})