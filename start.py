import connections
from connections import Connection
from downloadImages import downloadImages 
status = False

# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']

cons = []
cons.append(Connection('https://i1.sndcdn.com/', 'artworks-000319237989-ooxmoa-t500x500.jpg'))
cons.append(Connection('https://i1.sndcdn.com/', 'artworks-000319389714-9u4dgh-t500x500.jpg'))

status = connections.checkPing(cons)

if(downloadImages(cons, 10)):
    print('Succesfully downloaded and compiled')
else: 
    print('Download error. Re-pinging slaves')
    status = False
    status = connections.checkPing(cons)

