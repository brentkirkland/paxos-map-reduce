from collections import Counter
import string
import ast
import socket



class Reducer:
    def __init__(self, port, ip):
        self.port = port;
        self.ip = ip
        self.orig_filename = "f"
        self.logging_switch = True

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'REDUCER\t(' + str(self.port) + '):\t' + text;

    def listen(self):
        sock = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(10)
        while 1:
            self.log('waiting to accept')
            stream, addr = sock.accept();
            data = stream.recv(1024);
            self.log('recieved: ' + str(data))

            command = str(data).split()
            #could check 0th element and make sure its "reduce"
            self.reduce(command)

            stream.close();

        sock.close();

    def load_from_file(self, filename):
        self.orig_filename = filename.split('_')[0]

        f = open(filename, "r")
        text = f.read()
        counter = Counter(ast.literal_eval(text));

        return counter

    def reduce(self, command):
        filename_arr = command[1:]
        master_counter = Counter()

        for filename in filename_arr:
            master_counter += self.load_from_file(filename)

        self.output_file(master_counter)

    def output_file(self, counter):
        filename = self.orig_filename + "_reduced.txt"
        outfile = open(filename, "w")
        outfile.write(str(dict(counter)))

        outfile.close()
