class Mapper:
    def __init__(self, port):
        self.port = port;

    def log(self, text):
        print 'MAPPER\t(' + str(self.port) + '):\t' + text;
