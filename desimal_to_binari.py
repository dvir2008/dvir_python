def desimal_to_binari(x):
    if x == 0:
        return 0
    y = []
    while x > 0:
        y.insert(0,x&1)
        x = x>>1
    z = ''
    for i in range(len(y)):
        z += str(y[-i])
    return z
