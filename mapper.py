import collections
import string
import ast
import socket

class Mapper:
    def __init__(self, port, ip, mid):
        self.port = port;
        self.ip = ip;
        self.mid = mid;

    def log(self, text):
        print 'MAPPER\t(' + str(self.port) + '):\t' + text + ' - ' + str(self.mid);

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

            command = data.split();
            self.map(command[1], int(command[2]), int(command[3]))

            stream.close();

        sock.close();

    def writeToFile(self, filename, contents):
        fname = filename + '_I_' + str(self.mid) + '.txt';
        file = open(fname, 'w');
        file.write(contents);
        file.close();
        self.log('File ' + fname + ' saved.');

    def map(self, filename, offset, size):
        with open(filename) as f:
            content = f.read();

        bb = '';
        for x in range(offset, offset + size):
            bb += content[x].lower().translate(None, string.punctuation);

        c = collections.Counter(bb.split());
        cd = dict(c);

        self.log('Counting complete');
        self.writeToFile(filename.split('.')[0], str(cd));
