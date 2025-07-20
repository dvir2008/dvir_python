# תרגיל 1
# def get_value(dictionary, key):
#     if key in dictionary:
#         print(dictionary[key])
#     else:
#         print('ERROR')
# x = {"a": 1,"b": 2, "c": 3}        
# print(get_value(x,"a"))

# תרגיל 2
# def union_sets(s1,s2):
#     return s1.union(s2)
# x= {1,2,3}
# y = {4,5,6}
# print(union_sets(x,y))

# תרגיל 3
def c(l):
    x = {}
    for i in range(len(l)):
        for y in range(len(l[i])):
            if l[i][y] in x:
                x[l[i][y]] += 1
            else:
                x[l[i][y]] = 1
    print(x)
l = [('a', 'b'), ('a', 'c'), ('d', 'b'), ('e', 'f'), ('a', 'b')]
print(c(l))