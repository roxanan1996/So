from Queue import Queue
from threading import Thread

def worker():
        while True:
                    item = q.get()
                    #do_work(item)
                    q.task_done()

if __name__ == "__main__":
    q = Queue()
    for i in range(2):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    q.put(1)
    q.put(2)
    q.put(3)
    
    q.join()       # block until all tasks are done
    if q.empty():
        print "pul;a"
