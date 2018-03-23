import os, platform, time
import shlex  
from latencyTester.latencyTester import averagePing
from subprocess import Popen, PIPE, STDOUT

class Connection : # place this in another doc please..
    ip = ''
    port = ''
    ping = 0
    status = False
    reversedPing = 0
    
    def __init__ (self, _ip, _port):
        self.ip = _ip
        self.port = _port
    
    def updateConnection(self, accuracy) :
        con = averagePing(self.ip, accuracy)
        print('connection: ' + str(con))
        if(con != False) : # psuedo check for ping and return true if connection up.
            self.ping = con
            self.status = True
            print('Connection up for ' + self.ip + ' with ping: ' + str(self.ping))
            return True
        else : 
            self.status = False
            print('Connection could not be established to ' + self.ip)
            return False




def checkPing(connections, accuracy) : 
    anyConnectionDown = 1
    while (anyConnectionDown > 0) :
        print('Trying to connect to slaves')
        anyConnectionDown = 0

        for connection in connections :
            if(connection.updateConnection(accuracy) == False):
                anyConnectionDown += 1
        
        if(anyConnectionDown > 0):
            print(str(anyConnectionDown) + ' connection down. Re-pinging in 1 second')
            time.sleep(1)
        else:
            #calculate reverse ping (largest_ping - ping for each ping in pings)
            return True
    
    return True




