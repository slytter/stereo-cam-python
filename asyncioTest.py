import threading
import time
from connections import mayCheckConnection, pingConnections

def loop1_10(cons):
    try:
        while 1:
            if(mayCheckConnection()):
                time.sleep(5)
                pingConnections(cons, 1, False)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print('exit')        
def runIt():
    threading.Thread(target=loop1_10, args=[cons]).start()
