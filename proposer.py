import socket

class Proposer:
    def __init__(self, port, ips, ip, pid):
        self.port = port;
        self.ips = ips;
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


    # these next three functions are borrowed from stackoverflow. It helps parse large messages
    def send_msg(sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(sock):
        # Read message length and unpack it into an integer
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return recvall(sock, msglen)

    def recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def connect(self, message, ip, port):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSocket.connect((ip, port))
        # sendSocket.send(str(message));
        self.send_msg(sendSocket, message)
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
            # data = stream.recv(1024);
            data = self.recv_msg(stream)
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
            self.connect(message, self.ips[x], 5005 + (x)*10)

    def sendAccept(self, message):
        for x in range(0, 3):
            self.connect(message, self.ips[x], 5005 + (x)*10)

    def handleMajority(self, command):

        self.log(str(command))
        self.q.append(tuple(command[2]));
        self.v.append(command[3]);

        #TODO: figure out what the accept_num is needed for!
        #TODO: this will be some bug
        allNone = True
        if len(self.q) == 2:
            self.log('recieved majority!')
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
