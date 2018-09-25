def zigZag(amount):
    oneWay = list(range(0, amount))
    back = list(reversed(range(1, amount - 1)))
    return oneWay + back

def stride(amount):
    return list(range(0, amount))
