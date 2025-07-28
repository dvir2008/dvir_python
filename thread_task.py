import threading
a = 0
def thread_plos():
    global a
    for i in range(100):
        a+=1
def thread_minos():
    global a
    for i in range(100):
        a-=1

thread1 = threading.Thread(target=thread_plos)
thread2 = threading.Thread(target=thread_minos)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(a)

