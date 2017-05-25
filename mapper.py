import collections
import string

class Mapper:
    def __init__(self, port):
        self.port = port;

    def log(self, text):
        print 'MAPPER\t(' + str(self.port) + '):\t' + text;

    def map(self, filename, offset, size):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = " ".join(content).lower().translate(None, string.punctuation)
        print collections.Counter(content.split());
