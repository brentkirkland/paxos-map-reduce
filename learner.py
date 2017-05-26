import socket
import ast

class Learner:
    def __init__(self, port, ip, pid):
        self.port = port;
        self.ip = ip;
        self.pid = pid;
        self.d = {};
        self.my_log = [];
        self.logging_switch = True

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

            if command[0] == "print":
                self.log("received print command")
                self.print_logs()

            else:
                delim = "$$$eth$$$"
                c = data.split(delim)

                if c[0] == "accept":
                    self.learn(c[1], c[2])


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
