import socket
import os

class CLI:
    def __init__(self):
        return

    def log(self, text):
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
                self.connect(" ".join(command), self.r_ip, self.r_port)

        if command[0] == "replicate":
            if len(command) != 2:
                print 'argument required'
            else:
                self.log(command);
                self.connect(" ".join(command), self.prm_ip, self.prm_port)
