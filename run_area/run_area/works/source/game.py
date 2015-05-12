#!/usr/bin/python 

import socket
import sys

def client():
    ser_ip = sys.argv[1]
    ser_port = sys.argv[2]
    cli_ip = sys.argv[3]
    cli_port = sys.argv[4]
    pid = sys.argv[5]
    
    #print("%s %s %s" %(ser_ip, ser_port, pid))
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #conn.bind((cli_ip, cli_port))
    conn.connect(("127.0.0.1", 6000))

    pid = "pid:=pid"
    pname = "pname:=bowei"
    eol = "eol:=\n"
    msg = "reg: %s %s %s" %(pid, pname, eol)
    conn.send(msg)

    while 1:
        print "a"
        data=conn.recv(1024)
        if data:
            print data
        else:
            break
    conn.close()

if __name__ == "__main__":
    client()
