import socket

class Learner:
    def __init__(self, port, ip, pid):
        self.port = port;
        self.ip = ip;
        self.pid = pid;

    def log(self, text):
        print 'LEARNER (' + str(self.pid) + ')\t(' + str(self.port) + '):\t' + text;


    def listen(self):
        sock = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(10)
        while 1:
            self.log('waiting to accept')
            stream, addr = sock.accept();
            data = stream.recv(1024);
            self.log('recieved: ' + str(data))

            stream.close();

        sock.close();
