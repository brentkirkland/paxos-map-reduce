import socket
import os

class CLI:
    def __init__(self, pid):
        self.pid = pid
        self.logging_switch = True

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'CLI:\t' + str(text);

    def defineMapperOne(self, port, ip):
        self.m1_port = port;
        self.m1_ip = ip;

    def defineMapperTwo(self, port, ip):
        self.m2_port = port;
        self.m2_ip = ip;

    def defineReducer(self, port, ip):
        self.r_port = port;
        self.r_ip = ip;

    def definePRM(self, port, ip):
        self.prm_port = port;
        self.prm_ip = ip;

    def connect(self, message, ip, port):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSocket.connect((ip, port))
        sendSocket.send(str(message));
        sendSocket.close();

    def handleCommand(self, command):
        if command[0] == "map":
            if len(command) != 2:
                print 'argument required.'
            else:

                with open(command[1]) as f:
                    content = f.read()
                content = [x.strip() for x in content]

                middle = int(len(content)/2)

                while(content[middle] != ' ' and content[middle] != ''):
                    middle -= 1;

                firstmessage = "map " + command[1] + " 0 " + str(middle)
                secondmessage = "map " + command[1] + " " + str(middle + 1) + " " + str(len(content) - middle - 1)

                self.connect(firstmessage, self.m1_ip, self.m1_port);
                self.connect(secondmessage, self.m2_ip, self.m2_port)

        if command[0] == "reduce":
            if len(command) < 3:
                print 'minimum 2 arguments required'
            else:
                self.log('reducing...')
                self.connect(" ".join(command), self.r_ip, self.r_port)

        if command[0] == "replicate":
            if len(command) != 2:
                print 'argument required'
            else:
                self.log('replicating...')
                self.connect(" ".join(command), self.prm_ip, self.prm_port)

        if command[0] == "total":
            if len(command) < 3:
                print 'minimum 2 arguments required'
            else:
                self.log('totaling...')
                self.connect(" ".join(command), self.prm_ip, self.prm_port + 2)

        if command[0] == "print":
            self.connect(" ".join(command), self.prm_ip, self.prm_port + 2)

        if command[0] == "merge":
            if len(command) != 3:
                print '2 arguments required'
            else:
                self.log('merging...')
                self.connect(" ".join(command), self.prm_ip, self.prm_port + 2)


        if command[0] == "stop":
            self.log('stopping...')

            # TODO: // FIX FOR MULTIPLE NODES / GOOGLE
            self.connect("stop", self.prm_ip, self.prm_port)
            self.connect("stop", self.prm_ip, self.prm_port + 1)
            self.connect("stop", self.prm_ip, self.prm_port + 2)

        if command[0] == "resume":
            self.log('resuming...')

            self.connect("resume", self.prm_ip, self.prm_port)
            self.connect("resume", self.prm_ip, self.prm_port + 1)
            self.connect("resume", self.prm_ip, self.prm_port + 2)
