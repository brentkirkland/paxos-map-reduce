from main import Main
import sys

if __name__ == "__main__":

    num = 1;
    if len(sys.argv) == 2:
        num = sys.argv[1]

    main = Main(num)
    main.createProcesses();
