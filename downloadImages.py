import imageio
import datetime, time, os
import grequests


def downloadImages(cons, _fps) :
    paths = []

    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    basePath = 'images/' + str(timeStamp)
    os.makedirs(basePath)

    print('Requesting')
    ips = map(lambda con: con.ip + con.port + '?delay=' + str(con.reversedPing), cons) # reversed pings instead of pings
    requests = (grequests.get(ip) for ip in ips)
    responses = grequests.map(requests)

    i = 0
    for response in responses:
        if 199 < response.status_code < 400:
            name = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
            paths.append(name)
            with open(name, 'wb') as f:    # or save to S3 or something like that
                f.write(response.content)
        else:
            return False
        i += 1

    #images = (imageio.imread(filename) for filename in paths)
    images = []
    for filename in paths:
        images.append(imageio.imread(filename))

    imageio.mimsave(basePath + '/compiled.gif', images,fps=_fps)
    return True



