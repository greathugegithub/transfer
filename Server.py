# ！/usr/bin/env python3
# coding:utf8
# from datetime import datetime
import socket
import os
import sys
import struct
import fire


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width
        self.pp = 0

    def move(self, d):
        self.count = d

    def log(self, d):
        sys.stdout.flush()
        p = int(float(d))
        if p - self.pp == 1:
            sys.stdout.write('{0:3}/{1:3}: '.format(d, self.total))
            self.pp = p
            sys.stdout.write('#' * int(p / 2) + '-' * (self.width - int(p / 2)) + '\r')
            if p == self.width:
                sys.stdout.write('\n')
            sys.stdout.flush()


class main(object):
    def __init__(self):
        pass

    def tran(self, ip, tfname='file'):
        p = ProgressBar(total=100)
        tserver_adress = (ip, 1997)
        max_size = 1024
        if os.path.isfile(tfname):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(tserver_adress)
            print('Starting the tran at')
            asize = os.stat(tfname).st_size
            fmessage = struct.pack('128sl', os.path.basename(tfname).encode('utf-8'), asize)
            client.send(fmessage)
            b = 0
            w = open(tfname, 'rb')
            while True:
                p.log('%.2lf' % (b / asize * 100))
                s = w.read(max_size)
                if not s:
                    break
                client.send(s)
                b += 1024
            w.close()
            client.close()
        print('\nsend sucess!!\n')

    def recv(self, ip):
        p = ProgressBar(total=100)
        max_size = 1024
        print('Starting the recv at')
        server_address = (ip, 1997)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(server_address)
        server.listen(1)
        client, addr = server.accept()
        client.settimeout(1000)
        file_size = struct.calcsize('128sl')
        print('wait for a client to call')
        bf = client.recv(file_size)
        if bf:
            fname, fsize = struct.unpack('128sl', bf)
            newfname = fname.strip(b'\x00')
            print('now recv a file %s, filesize is %s' % (newfname, fsize))
            #k = input('please input y or n,Confirm acceptance:')
            k = 'y'
            if k == 'y':
                r = open(newfname, 'wb')
                print('start receiving....')
                alldata = 0
                while not alldata == fsize:
                    p.log('%.2lf' % (alldata / fsize * 100))
                    if fsize - alldata > 1024:
                        data = client.recv(max_size)
                        alldata += len(data)
                    else:
                        data = client.recv(fsize - alldata)
                        alldata = fsize
                    r.write(data)
                r.close()
            elif k == 'n':
                print('over!')
                os._exit(0)
            server.close()
            print('\nrecv success!!!\n')

    def help(self):
        print('Usage:\t\t1.recv:ftf recv [ip]')
        print('      \t\t2.tran:ftf tran [ip] [filename]')
        print('\nWhen using, open the receiver first(recv), development of sending again(tran)!\n')


class F():
    f = fire.Fire(main)


if __name__ == '__main__':
    m = main()
    while True:
        m.recv('###.###.###.###')

