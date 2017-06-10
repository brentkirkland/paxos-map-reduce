import collections
from proposer import Proposer
from acceptor import Acceptor
from learner import Learner
from multiprocessing import Process

class PRM:

    def __init__(self, port, ips, ip, num):
        self.port = int(port);
        self.ips = ips;
        self.ip = ip;
        self.num = int(num);
        self.logging_switch = True

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'PRM (' + str(self.num) + ')\t(' + str(self.port) + '):\t' + text;

    def createProposer(self):
        proposer = Proposer(self.port, self.ips, self.ip, self.num);
        if not self.logging_switch:
            proposer.logging(False)
        proposer.log('starting');

        proposer.listen();

        proposer.log('exiting');

    def createAcceptor(self):
        acceptor = Acceptor(self.port+1, self.ips, self.ip, self.num);
        if not self.logging_switch:
            acceptor.logging(False)
        acceptor.log('starting');

        acceptor.listen();

        acceptor.log('exiting');

    def createLearner(self):
        learner = Learner(self.port+2, self.ips, self.ip, self.num);
        if not self.logging_switch:
            learner.logging(False)
        learner.log('starting');

        learner.listen();

        learner.log('exiting');

    def createFlavors(self):
        p1 = Process(target=self.createProposer);
        p2 = Process(target=self.createAcceptor);
        p3 = Process(target=self.createLearner);

        p1.start();
        p2.start();
        p3.start();
