import collections
import string
import ast
import socket

class Mapper:
    def __init__(self, port, ip, mid):
        self.port = port;
        self.ip = ip;
        self.mid = mid;
        self.logging_switch = True

    def logging(self, switch):
        self.logging_switch = switch

    def log(self, text):
        if self.logging_switch:
            print 'MAPPER\t(' + str(self.port) + '):\t' + text + ' - ' + str(self.mid);

    # these next three functions are borrowed from stackoverflow. It helps parse large messages
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

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
            self.map(command[1], int(command[2]), int(command[3]))

            stream.close();

        sock.close();

    def writeToFile(self, filename, contents):
        fname = filename + '_I_' + str(self.mid) + '.txt';
        file = open(fname, 'w');
        file.write(contents);
        file.close();
        self.log('File ' + fname + ' saved.');

    def map(self, filename, offset, size):
        with open(filename) as f:
            content = f.read();

        bb = '';
        for x in range(offset, offset + size):
            bb += content[x].lower().translate(None, string.punctuation);

        c = collections.Counter(bb.split());
        cd = dict(c);

        self.log('Counting complete');
        self.writeToFile(filename.split('.')[0], str(cd));
