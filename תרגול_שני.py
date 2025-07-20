words_list = ['banana', 'apple','orenge','kiwi','strawberry','pineapple']
print(words_list)
max_len = 0
y = []
for i in range(len(words_list)):
    if len(words_list[i])>max_len:
        max_len = len(words_list[i])
for x in range(len(words_list)-1):
    if len(words_list[x]) == max_len:
        y.append(words_list[x])
        words_list.pop(x)
max_len= 0
for i in range(len(words_list)):
    if len(words_list[i])>max_len:
        max_len = len(words_list[i])
for x in range(len(words_list)):
    if len(words_list[x]) == max_len:
        y.append(words_list[x])
print(y)        
