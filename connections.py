import os, platform, time

class Connection : # place this in another doc please..
    ip = ''
    port = ''
    ping = 0
    status = False
    
    def __init__ (self, _ip, _port):
        self.ip = _ip
        self.port = _port
    
    def updateConnection(self) :
        connection = True
        newPing = 10
        if(connection) : # psuedo check for ping and return true if connection up.
            self.ping = (self.ping + newPing) / 2 # moving average thing
            self.status = True
            print('Connection up for ' + self.ip + 'with ping: ' + str(self.ping))
            return True
        else : 
            self.status = False
            print('Connection could not be established to ' + self.ip)
            return False




def checkPing(connections) : 
    anyConnectionDown = 1
    while (anyConnectionDown > 0) :
        print('Trying to connect to slaves')
        anyConnectionDown = 0
        for connection in connections :
            if(connection.updateConnection() == False) :
                anyConnectionDown += 1
        if(anyConnectionDown > 0):
            time.sleep(1)
    
    return True






