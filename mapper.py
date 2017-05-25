import collections
import string
import ast

class Mapper:
    def __init__(self, port, ip, mid):
        self.port = port;
        self.ip = ip;
        self.mid = mid;

    def log(self, text):
        print 'MAPPER\t(' + str(self.port) + '):\t' + text + ' - ' + str(self.mid);

    def listen():
        sock = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def writeToFile(self, filename, contents):
        fname = filename + '_I_' + str(self.mid) + '.txt';
        file = open(fname, 'w')
        file.write(contents)
        file.close()
        self.log('File ' + fname + ' saved.')

    def map(self, filename, offset, size):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = " ".join(content).lower().translate(None, string.punctuation)
        c = collections.Counter(content.split());
        cd = dict(c)

        self.log('Counting complete')

        self.writeToFile(filename, str(cd))
