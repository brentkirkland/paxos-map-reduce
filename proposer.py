import socket

class Proposer:
    def __init__(self, port, ip, pid):
        self.port = port;
        self.ip = ip;
        self.pid = pid;
        self.n = 0;
        self.q = []
        self.v = []
        self.logging_switch = True
        self.stopped = False

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'PROPOSER (' + str(self.pid) + ')\t(' + str(self.port) + '):\t' + text;

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

            command = data.split();

            if not self.stopped:
                if command[0] == "stop":
                    self.stopped = True
                elif command[0] == "replicate":
                    fname = command[1];
                    self.v = [];
                    self.q = [];
                    self.sendProposal(fname);
                else:
                    command = data.split("$$$eth$$$");
                    #self.log(str(command))
                    self.handleMajority(command)

            if command[0] == "resume":
                self.stopped = False

            stream.close();

        sock.close();

    def sendProposal(self, fname):
        self.fname = fname

        self.n += 1
        message = "prepare " + str(self.n) + " " + str(self.pid)

        # TODO: FIX THIS FOR GOOGLE. NO HARDCODE
        for x in range(0, 3):
            self.connect(message, self.ip, 5005 + (x)*10)

    def sendAccept(self, message):
        for x in range(0, 3):
            self.connect(message, self.ip, 5005 + (x)*10)

    def handleMajority(self, command):

        self.log(str(command))
        self.q.append(tuple(command[2]));
        self.v.append(command[3]);

        #TODO: figure out what the accept_num is needed for!
        #TODO: this will be some bug
        allNone = True
        if len(self.q) == 2:
            self.log('recieved all three!')
            for x in self.v:
                self.log('X: ' + str(x))
                if x != "None":
                    allNone = False;
            if allNone:
                #json of file

                f = open(self.fname, "r")
                text = f.read()
                value = {
                    'filename': self.fname,
                    'contents': text
                }

                myVal = value;

                self.log(str(value))

            else:
                maxx = max(self.q)
                indi = self.q.index(maxx)
                myVal = self.v[indi]

            delimiter = "$$$eth$$$"
            message = "accept" + delimiter + str(command[1]) + delimiter + str(myVal)

            self.sendAccept(message)

            self.v = [];
            self.q = [];


            # send commands!

        #message = "ack" + delim + str(self.ballot_num) + delim + str(self.accept_num) + delim + str(self.accept_val)
