import threading
import time
from connections import mayCheckConnection, pingConnections

def loop1_10(cons):
    while 1:
        if(mayCheckConnection()):
            time.sleep(5)
            pingConnections(cons, 1, False)

def runIt():
    threading.Thread(target=loop1_10, args=[cons]).start()
