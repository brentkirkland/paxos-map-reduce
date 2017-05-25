import collections
import string
import ast

class Mapper:
    def __init__(self, port, ip):
        self.port = port;
        self.ip = ip;

    def log(self, text):
        print 'MAPPER\t(' + str(self.port) + '):\t' + text;

    def listen():
        sock = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



    def map(self, filename, offset, size):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = " ".join(content).lower().translate(None, string.punctuation)
        print collections.Counter(content.split());

        strr = "{'name': 3, 'is': 3, 'my': 3, 'christian': 1, 'middle': 1, 'kirkland': 1, 'last': 1, 'brent': 1, 'first': 1}"
        d = ast.literal_eval(strr);
        print d['name']
        print d;
