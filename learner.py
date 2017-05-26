class Learner:
    def __init__(self, port, ip, num):
        self.port = port;
        self.ip = ip;
        self.num = num;

    def log(self, text):
        print 'LEARNER (' + str(self.num) + ')\t(' + str(self.port) + '):\t' + text;
