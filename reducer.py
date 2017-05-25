class Reducer:
    def __init__(self, port):
        self.port = port;

    def log(self, text):
        print 'REDUCER\t(' + str(self.port) + '):\t' + text;
