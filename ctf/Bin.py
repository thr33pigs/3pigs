#!/usr/bin/env python
# encoding: utf-8

import socket
import re

class Pig:
    def __init__(self, status, name, cont, pic):
        self.status = int(status)
        self.name = name
        self.cont = cont if cont else 'No description now.'
        self.pic= pic

class binary():
    def __init__(self):
        host = "192.168.0.2"
        port = 3333
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.s.settimeout(10)
        self.error = ""
        self.err = ["No input",
                      "No this pig",
                      "Pig offline",
                      "No operation",
                      "Wrong secret",
                      "Time Out"]
        print self.recv()

    def send(self, msg):
        self.s.send(msg)
        print "send: " + msg

    def recv(self):
        msg = ''
        while True:
            try:
                tmp = self.s.recv(1)
            except:
                self.close()
                self.error = self.err[5]
                raise Exception
            if tmp == "\n":
                break
            elif ord(tmp)>=128:
                msg += "\\x"+tmp.encode("hex")
            else:
                msg += tmp
        msg = msg.strip()
        print "recv: " + msg
        if re.match("^Error_\d$",msg):
            self.error = self.err[int(msg[6])]
            raise Exception
        return msg

    def close(self):
        try:
            self.s.close()
        except:
            pass

    def getpigs(self):
        pig = []
        try:
            self.recv()
            self.send('3')
            for i in xrange(1,5):
                tmp = self.recv()
                tmp = tmp.split('|')
                pig.append(Pig(tmp[0],tmp[1],tmp[2],"static/pig%d.png"%i))
            self.recv()
            return pig
        except :
            return self.error

    def showpigs(self):
        pig = []
        for i in self.getpigs():
            if i.status:
                pig.append(i)
        return pig

    def addpig(self,pid,cont):
        try:
            self.recv()
            self.send('1')
            self.recv()
            self.send(str(pid))
            self.recv()
            self.send(cont)
            return self.recv()
        except :
            return self.error

    def freepig(self,pid):
        try:
            self.recv()
            self.send('2')
            self.recv()
            self.send(str(pid))
            return self.recv()
        except :
            return self.error

    def flypig(self, secret, u=0):
        if u:
            return self.flying(secret)
        try:
            self.recv()
            self.send('4')
            self.recv()
            self.send(secret)
            return self.recv()
        except :
            return self.error

    def flying(self,cont):
        try:
            self.recv()
            self.send('5')
            self.recv()
            self.send(cont)
            return self.recv()
        except :
            return self.error
