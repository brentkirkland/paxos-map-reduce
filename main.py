from cli import CLI
from mapper import Mapper
from reducer import Reducer

if __name__ == "__main__":
    cli = CLI(5001);
    mapper = Mapper(5002);
    reducer = Reducer(5003);

    print cli.port;
    print mapper.port;
    print reducer.port
