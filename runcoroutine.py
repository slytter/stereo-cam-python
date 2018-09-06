import asyncio

def runCoroutine(corou):
    try:
#        print('exacuting couroutine')
        corou.send(None)
    except StopIteration as e:
#        print('couroutine exacuted')
        return e.value
