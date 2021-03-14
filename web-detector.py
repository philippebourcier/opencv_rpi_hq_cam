#!/usr/bin/python3

import sys
from daemonize import Daemonize
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import yaml

def writef(f,c):
    with open("/dev/shm/detector_"+f+".run",'w') as file: file.write(c)

def getf(f):
    with open("/dev/shm/detector_"+f+".run",'r') as file: return(file.read())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path == "/on":
                self.wfile.write("ON".encode('utf-8'))
                writef("status","ON\n")
        elif self.path == "/off":
                self.wfile.write("OFF".encode('utf-8'))
                writef("status","OFF\n")
        elif self.path == "/status":
                self.wfile.write(getf("output").encode('utf-8'))
        else:
                self.wfile.write("".encode('utf-8'))
    def log_message(self,format,*args):
        return

class ThreadingSimpleServer(ThreadingMixIn,HTTPServer): pass

def main():
    try:
        server=ThreadingSimpleServer(('0.0.0.0',8002),Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nFinished.')

if len(sys.argv)==2 and sys.argv[1]=="-d":
    daemon=Daemonize(app="web-detector",pid=pid,action=main)
    daemon.start()
else:
    main()

