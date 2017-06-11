import socket

class Acceptor:
    def __init__(self, port, ips, ip, pid):
        self.port = port;
        self.ips = ips;
        self.ip = ip;
        self.pid = pid;
        self.ballot_num = (0,0);
        self.accept_num = (0,0);
        self.accept_val = None;
        self.logging_switch = True
        self.stopped = False

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'ACCEPTOR (' + str(self.pid) + ')\t(' + str(self.port) + '):\t' + text;

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
                elif command[0] == "prepare":
                    self.accept((int(command[1]), int(command[2])))
                else:
                    c = data.split("$$$eth$$$")
                    if c[0] == "accept":
                        self.log('accepted: ' + data)
                        self.update(c[1], c[2], data)
                    if c[0] == "reset":
                        self.log('reset')
                        self.accept_num = (0,0);
                        self.accept_val = None;

            if command[0] == "resume":
                self.stopped = False

            stream.close();

        sock.close();

    def accept(self, n_pid_tuple):
        if n_pid_tuple >= self.ballot_num:
            self.ballot_num = n_pid_tuple;
            delim = "$$$eth$$$";
            message = "ack" + delim + str(self.ballot_num) + delim + str(self.accept_num) + delim + str(self.accept_val)
            n, p = n_pid_tuple;

            self.connect(message, self.ips[p-1], 5004 + int(p-1)*10)

    def update(self, b, value_str, data):
        tup_b = tuple(b)

        if tup_b >= self.ballot_num:
            self.accept_num = tup_b
            self.accept_val = value_str

            #TODO: FIX for googles
            for x in range(0, 3):
                self.connect(data, self.ips[x], 5006 + (x)*10)
