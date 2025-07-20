def check_polindrom(x):
    str(x)
    t = x
    y =[]
    for i in range(len(x)):
        y.insert(i,x[i])
    y.reverse()    
    t_o_f =   True
    for i in range(len(y)):
        if x[i] != y[i]:
            t_o_f = False
    return t_o_f
def check(x):
  for i in range(len(x)):
    if check_polindrom(x[i]) == False:
        x.pop(i)
  return x

print(check(["noon", 'baab','gajag']))


