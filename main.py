from cli import CLI
from mapper import Mapper
from reducer import Reducer
from prm import PRM
from multiprocessing import Process
import time

class Main:

    def __init__(self, num):
        self.num = int(num)

    def createCLI(self):
        cli = CLI(self.num);
        # cli.logging(False)
        cli.log('Starting Up');

        # this maps the CLI looks pretty
        time.sleep(1);
        cli.log('Loading 3...');
        time.sleep(1);
        cli.log('Loading 2...');
        time.sleep(1);
        cli.log('Loading 1...');
        time.sleep(1);

        # pass details
        cli.defineMapperOne(5001 + (self.num-1)*10, "127.0.0.1");
        cli.defineMapperTwo(5002 + (self.num-1)*10, "127.0.0.1");
        cli.defineReducer(5003 + (self.num-1)*10, "127.0.0.1");
        cli.definePRM(5004 + (self.num-1)*10, "127.0.0.1");

        cli.log('Enter commands below. Use ctrl+c to exit.')
        boo = True
        while (boo):
            try:
                command = raw_input('> ')
                cli.handleCommand(command.split());
            except KeyboardInterrupt:
                boo = False;
            time.sleep(1);

        # exiting
        cli.log('Exiting');

    def createMapperOne(self):
        mapperOne = Mapper(5001 + (self.num-1)*10, "127.0.0.1", 1);
        mapperOne.logging(False)
        mapperOne.log('Starting Up');

        # execution code goes here
        mapperOne.listen()

        # exiting
        mapperOne.log('Exiting');

    def createMapperTwo(self):
        mapperTwo = Mapper(5002 + (self.num-1)*10, "127.0.0.1", 2);
        mapperTwo.logging(False)
        mapperTwo.log('Starting Up');

        # execution code goes here
        mapperTwo.listen()

        # exiting
        mapperTwo.log('Exiting');

    def createReducer(self):
        reducer = Reducer(5003 + (self.num-1)*10, "127.0.0.1");
        reducer.logging(False)
        reducer.log('Starting Up');

        # execution code goes here
        reducer.listen()

        # exiting
        reducer.log('Exiting');

    def createPRM(self):
        prm = PRM(5004 + (self.num-1)*10, "127.0.0.1", self.num);
        prm.logging(False)
        prm.log('Starting Up');

        # execution code goes here
        prm.createFlavors()

        # exiting
        prm.log('Exiting');


    def createProcesses(self):
        p1 = Process(target=self.createMapperOne);
        p2 = Process(target=self.createMapperTwo);
        p3 = Process(target=self.createReducer);
        p4 = Process(target=self.createPRM);

        p1.start();
        p2.start();
        p3.start();
        p4.start();

        self.createCLI();
