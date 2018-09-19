import socket, os

print('starting')
HOST_UP = True if os.system("timeout 0.4 ping -c 1 -W 1 " + 'mastejr.local') is 0 else False
print(HOST_UP)