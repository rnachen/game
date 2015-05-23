#!/usr/bin/python 

import socket
import sys
import re

conn = 0
pid = 0
game_info = {}

def get_socket():
    ser_ip = sys.argv[1]
    ser_port = int(sys.argv[2])
    cli_ip = sys.argv[3]
    cli_port = int(sys.argv[4])
    pid = sys.argv[5]

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.bind((cli_ip, cli_port))
    conn.connect((ser_ip, ser_port))
    return conn, pid
def game():
    global conn
    global pid
    conn, pid = get_socket()
    pname = "bowei"
    eol = "\n"
    reg_msg = "reg: %s %s %s" %(pid, pname, eol)

    try:
        conn.send(reg_msg)
    except:
        print("error")
    data = ""
    buf = ""
    index = 0

    while 1:
        while 1:
            if data.find("/hold") != -1:
                break
            data += conn.recv(1024)
        index = data.find('/hold')
        print index





def client():
    global conn
    global pid
    conn, pid = get_socket()
    pname = "bowei"
    eol = "\n"
    msg = "reg: %s %s %s" %(pid, pname, eol)
    try:
        conn.send(msg)
    except:
        print("error")
    
    data = ""
    while 1:
        while 1:
            if data.find('/hold') != -1:
                break
            data += conn.recv(1024)
            
        game_start(data, pid)
        
        while 1:
            try:
                data = conn.recv(1024)
                if data.find('/seat'):
                    break
                conn.send("call")
            except:
                conn.close()
                break
                #time.sleep(1)
                #conn, pid = get_socket()
    
    conn.close()

def game_start(msg, pid):
    print msg.split('\n')
    seat_info = get_info(msg, "seat")
    blind_info = get_info(msg, "blind")
    hold_info = get_info(msg, "hold")
    
    for i in xrange(1,9):
        info = seat_info[i].split(':')
        if len(info) >= 2:
            info = info[1].strip().split()
        else:
            info = info[0].strip().split()
        game_info['pos_%d'%(i)] = info
        if pid in info:
            game_info['mypos'] = i

    game_info['small'] = blind_info[1].split(':')[1].strip()
    game_info['big'] = blind_info[2].split(':')[1].strip()

    game_info['hold_card'] = hold_info[1:3]

def get_info(msg, info):
    msgs = re.search("%s/[\s\S]*/%s"%(info, info), msg)
    return msgs.group(0).split('\n')
    


if __name__ == "__main__":
    #client()
    game()
