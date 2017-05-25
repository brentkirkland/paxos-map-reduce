from cli import CLI
from mapper import Mapper
from reducer import Reducer
from multiprocessing import Process
import time

def createCLI():
    cli = CLI(5001);
    cli.log('Starting Up');
    # execution code goes here

    # exiting
    cli.log('Exiting');

def createMapperOne():
    mapperOne = Mapper(5002);
    mapperOne.log('Starting Up - (1)');
    # execution code goes here

    # exiting
    mapperOne.log('Exiting - (1)');

def createMapperTwo():
    mapperTwo = Mapper(5003);
    mapperTwo.log('Starting Up - (2)');
    # execution code goes here

    # exiting
    mapperTwo.log('Exiting - (2)');

def createReducer():
    reducer = Reducer(5004);
    reducer.log('Starting Up');
    # execution code goes here

    # exiting
    reducer.log('Exiting');


def createProcesses():
    p1 = Process(target=createCLI);
    p2 = Process(target=createMapperOne);
    p3 = Process(target=createMapperTwo);
    p4 = Process(target=createReducer);

    p1.start()
    p2.start()
    p3.start()
    p4.start()


if __name__ == "__main__":
    createProcesses();
