mport SocketServer
from time import ctime
import logging
import socket

HOST = '192.168.2.83'
PORT = 4321
ADDR = (HOST, PORT)
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='log.txt',
        filemode='a+')

class MyRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print '...connected from:', self.client_address
        while True:
            try:
                data = self.request.recv(1024)
                if(not data):
                    break
                self.request.sendall('[%s] %s' % (ctime(),data[0]))
            except socket.timeout:
                print "caught socket.timeout exception"
    def LogTemplate(self, s):
        return '[id.' + str(id(self.request)) + ']:  ' + str(s)
    def Log(self, s):
        ss =  self.LogTemplate(s)
        print ss
        logging.info(ss)
    def LogErr(self, s):
        ss =  self.LogTemplate(s)
        print ss
        logging.error(ss)

    def setup(self):
        self.Log('进入处理线程')
        self.request.settimeout(60)
    def finish(self):
        self.request.close()
        self.Log("退出处理线程")

tcpServ = SocketServer.ThreadingTCPServer(ADDR, MyRequestHandler)
print 'waiting for connection...'
tcpServ.serve_forever()

