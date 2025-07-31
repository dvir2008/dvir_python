from threading import Thread,Lock
a = 0
l = Lock()
def thread_plos():
    global a
    for i in range(100000):
        with l:
            a+=1
def thread_minos():
    global a
    for i in range(100000):
        with l:    
         a-=1

thread1 = Thread(target=thread_plos)
thread2 = Thread(target=thread_minos)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(a)

