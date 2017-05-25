class Reducer:
    def __init__(self, port):
        self.port = port;

    def log(self, str):
        print 'FROM REDUCER: ' + str;
