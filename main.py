from cli import CLI
from mapper import Mapper
from reducer import Reducer
from multiprocessing import Process
import time

class Main:

    def __init__(self, num):
        self.num = int(num)

    def createCLI(self):
        cli = CLI();
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
        cli.defineMapperOne(5001, "127.0.0.1");
        cli.defineMapperTwo(5002, "127.0.0.1");
        cli.defineReducer(5003, "127.0.0.1");

        cli.log('Enter commands below. Use ctrl+c to exit.')
        boo = True
        while (boo):
            try:
                command = raw_input('> ')
                cli.handleCommand(command.split());
            except KeyboardInterrupt:
                boo = False;

        # exiting
        cli.log('Exiting');

    def createMapperOne(self):
        mapperOne = Mapper(5001 + (self.num-1)*10, "127.0.0.1", 1);
        mapperOne.log('Starting Up');
        # execution code goes here

        # mapperOne.map('test/first.txt', 0, 0)
        mapperOne.listen()

        # exiting
        mapperOne.log('Exiting');

    def createMapperTwo(self):
        mapperTwo = Mapper(5002 + (self.num-1)*10, "127.0.0.1", 2);
        mapperTwo.log('Starting Up');
        # execution code goes here

        # mapperTwo.map('test/second.txt', 0, 0)
        mapperTwo.listen()

        # exiting
        mapperTwo.log('Exiting');

    def createReducer(self):
        reducer = Reducer(5003 + (self.num-1)*10, "127.0.0.1");
        reducer.log('Starting Up');
        # execution code goes here

        reducer.listen()
        # exiting
        reducer.log('Exiting');


    def createProcesses(self):
        p2 = Process(target=self.createMapperOne);
        p3 = Process(target=self.createMapperTwo);
        p4 = Process(target=self.createReducer);

        p2.start();
        p3.start();
        p4.start();

        self.createCLI();
