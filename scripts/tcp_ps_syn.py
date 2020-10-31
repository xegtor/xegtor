#!/usr/bin/env python3

'''
this script performs tcp port scan (syn method)
'''

from argparse import ArgumentParser
import socket
from threading import Thread
from time import sleep

class TcpSynPortScanner():
    def __init__(self,target_ip,port,timeout):
        self.target_ip = target_ip
        self.port_argument = port
        try:
            self.timeout = float(timeout)
        except ValueError :
            print('error : invalid timeout [e.g 0.1] [--script-help or -sh for help]')

    def start(self):
        self.ports_list = [] # ports which should be scanned
        print('target : ' + self.target_ip)
        print('timeout : ' + str(self.timeout))
        self.check_port() # check port argument and adds ports in self.ports_list var
        self.open_ports_list = [] # a list that contains open ports

        try:
            for p in self.ports_list :
                thread = Thread(target=self.scan,args=(p,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt :
            print()
            print('Scan Stopped!')
            exit()  # exit when ctrl+c is pressed

        sleep(1)
        for op in self.open_ports_list :
            print("[+] Port " + str(op) + "/TCP is open")

    def check_port(self):

        if ',' in self.port_argument: # for specific ports
            self.ports_to_check = self.port_argument.split(',')
            num = 0
            for p in self.ports_to_check :
                try:
                    int(p)
                except:
                    print()
                    print('error : invalid port ---> e.g 80,22 or 1-65535 [--script-help or -sh for help]')
                    exit()
                else:
                    if (num < 1):
                        print('ports : ',end='')
                        num += 1
                    self.ports_list.append(int(p))
                    print(p + ' ',end='')

        elif '-' in self.port_argument : # for ports range
            try :
                port_start = int(self.port_argument.split('-')[0])
                port_end = int(self.port_argument.split('-')[1])
            except :
                print()
                print('error : invalid port ---> e.g 80,22 or 1-65535 [--script-help or -sh for help]')
                exit()
            else:
                self.ports_list = list(range(port_start,port_end + 1))
                print('ports : ' + str(port_start) + ' to ' + str(port_end))

        else: # for single port
            try :
                int(self.port_argument)
            except ValueError:
                print()
                print('error : invalid port ---> e.g 80,22 or 1-65535 [--script-help or -sh for help]')
                exit()
            else:
                self.ports_list.append(int(self.port_argument))
        print()

    def scan(self,port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.target_ip, port))
        except:
            pass
        else:
            self.open_ports_list.append(str(port))
            sock.close()


def print_parser_help():
    help_text = '''
optional arguments:
  --script-help, -sh           Show Script Help
  --target                     Target To Attack *
  --port   x,y,z, x-z          Port Number(s) To Attack *
  --timeout default 0.1 sec    Timeout For Response
    '''
    print(help_text)


parser = ArgumentParser(usage='sudo python3 %(prog)s --script tcp_ps_syn.py [--script-help or -sh for help] [--target TARGET] [--port PORT(S)] [--timeout sec (default 0.1 sec)]',allow_abbrev=False)
parser.add_argument('--script-help', '-sh', help='Show Script Help', action='store_true')
parser.add_argument('--target', help='Target To Attack', metavar='')
parser.add_argument('--port','-p',help='Port Numbers To Attack', metavar='x,y,z')
parser.add_argument('--timeout', help='Timeout For Response', metavar='default : 0.1 sec',default=0.1)
args, unknown = parser.parse_known_args()

if ((args.script_help is not None) and (args.script_help is True)):
    print_parser_help()

if ((args.target != None) and (args.port != None)):
    pass
else:
    parser.print_usage()
    exit()

scanner = TcpSynPortScanner(target_ip=args.target,port=args.port,timeout=args.timeout)
scanner.start()