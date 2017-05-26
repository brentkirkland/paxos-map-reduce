import collections
from proposer import Proposer
from acceptor import Acceptor
from learner import Learner
from multiprocessing import Process

class PRM:

    def __init__(self, port, ip, num):
        self.port = int(port);
        self.ip = ip;
        self.num = int(num);

    def log(self, text):
        print 'PRM (' + str(self.num) + ')\t(' + str(self.port) + '):\t' + text;

    def createProposer(self):
        proposer = Proposer(self.port, self.ip, self.num);
        proposer.log('starting');

        proposer.listen();

        proposer.log('exiting');

    def createAcceptor(self):
        acceptor = Acceptor(self.port+1, self.ip, self.num);
        acceptor.log('starting');

        acceptor.listen();

        acceptor.log('exiting');

    def createLearner(self):
        learner = Learner(self.port+2, self.ip, self.num);
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
