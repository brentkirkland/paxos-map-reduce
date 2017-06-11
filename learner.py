import socket
import ast
from collections import Counter

class Learner:
    def __init__(self, port, ips, ip, pid):
        self.port = port;
        self.ips = ips;
        self.ip = ip;
        self.pid = pid;
        self.d = {};
        self.my_log = [];
        self.logging_switch = True
        self.stopped = False

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'LEARNER (' + str(self.pid) + ')\t(' + str(self.port) + '):\t' + text;

    def connect(self, message, ip, port):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSocket.connect((ip, port))
        sendSocket.send(str(message));
        sendSocket.close();

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


            command = data.split()

            if not self.stopped:
                if command[0] == "print":
                    self.log("received print command")
                    self.print_logs()
                elif command[0] == "total":
                    self.total(command)

                elif command[0] == "merge":
                    self.merge(command)

                elif command[0] == "stop":
                    self.stopped = True

                else:
                    delim = "$$$eth$$$"
                    c = data.split(delim)

                    if c[0] == "accept":
                        self.learn(c[1], c[2])

            if command[0] == "resume":
                #self.stopped = False
                self.catchup()
            if command[0] == "catchup":
                self.respond_to_catchup(command[1], command[2])

            command = data.split("$$$eth$$$")
            if command[0] == "logupdate":
                print "command 1: " + command[1]
                self.finish_catchup(eval(command[1]))
                self.stopped = False




            stream.close();

        sock.close();

    def learn(self, b, value_str):

        shabug = {
            'value_str': value_str,
            'count': 1,
            'has_written': False
        }

        if b in self.d:
            self.d[b]['count'] += 1
        else:
            self.d[b] = shabug

        if b in self.d and self.d[b]['count'] >= 2 and not self.d[b]['has_written']:
            self.writeToLog(value_str)
            self.connect("reset$$$eth$$$", self.ip, self.port - 1)
            self.d[b]['has_written'] = True

    def catchup(self):
        print "in catchup"
        #ping all learners and ask for log
        catchup_msg = "catchup " + self.ip + " " + str(self.port)

        for x in range(0, 3):
            self.connect(catchup_msg, self.ips[x], 5006 + (x)*10)

        ##(learners should be listening for this message, when they get it they respond with their log)
    def respond_to_catchup(self, ip, port):
        print "in respond to catchup"
        catchup_response_msg = "logupdate$$$eth$$$" + str(self.my_log)
        self.connect(catchup_response_msg, ip, int(port))


    def finish_catchup(self, log_arr):
        #once we hear back from a majority of learners
        print "got in finish_catchup"
        print 'some parsing' + str(log_arr[0])
        if len(log_arr) > len(self.my_log):
            print "updated log from: " + str(self.my_log) + " to " + str(log_arr)
            self.my_log = log_arr


    def writeToLog(self, value_str):

        val = ast.literal_eval(value_str)
        self.log('testing')
        self.log(str(val['filename']))

        loggy = {
            'filename': str(val['filename']),
            'contents': val['contents']
        }

        self.my_log.append(loggy)

    def print_logs(self):
        print "printing filenames:"
        for log in self.my_log:
            print log['filename']

    def merge(self, commands):
        str_contents_one = self.my_log[int(commands[1])]['contents']
        str_contents_two = self.my_log[int(commands[2])]['contents']

        c1 = Counter(ast.literal_eval(str_contents_one));
        c2 = Counter(ast.literal_eval(str_contents_two));

        c = c1 + c2;

        print dict(c)


    def total(self, commands):
        b = Counter();
        for x in range(1, len(commands)):
            command = int(commands[x])
            str_contents = self.my_log[command]['contents']
            c = Counter(ast.literal_eval(str_contents));
            b = b + c;

        s = sum(b.values());

        print 'Sum: ' + str(s)
