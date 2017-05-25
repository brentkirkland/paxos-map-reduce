from cli import CLI
from mapper import Mapper
from reducer import Reducer
from multiprocessing import Process
import time

def createCLI():
    cli = CLI();
    cli.log('Starting Up');
    # execution code goes here

    # this maps the CLI looks pretty
    time.sleep(1)
    cli.log('Loading 5...')
    time.sleep(1)
    cli.log('Loading 4...')
    time.sleep(1)
    cli.log('Loading 3...')
    time.sleep(1)
    cli.log('Loading 2...')
    time.sleep(1)
    cli.log('Loading 1...')
    time.sleep(1)

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

def createMapperOne():
    mapperOne = Mapper(5001);
    mapperOne.log('Starting Up - (1)');
    # execution code goes here

    # exiting
    mapperOne.log('Exiting - (1)');

def createMapperTwo():
    mapperTwo = Mapper(5002);
    mapperTwo.log('Starting Up - (2)');
    # execution code goes here

    # exiting
    mapperTwo.log('Exiting - (2)');

def createReducer():
    reducer = Reducer(5003);
    reducer.log('Starting Up');
    # execution code goes here

    # exiting
    reducer.log('Exiting');


def createProcesses():
    # p1 = Process(target=createCLI);
    p2 = Process(target=createMapperOne);
    p3 = Process(target=createMapperTwo);
    p4 = Process(target=createReducer);

    # p1.start()
    p2.start()
    p3.start()
    p4.start()

    createCLI();


if __name__ == "__main__":
    createProcesses();
