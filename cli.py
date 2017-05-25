class CLI:
    def __init__(self):
        return

    def log(self, text):
        print 'CLI:\t' + text;

    def handleCommand(self, command):
        if command[0] == "map":
            if len(command) != 3:
                print 'Missing arguments'
            else:
                print "I'm a mapper mofo"
