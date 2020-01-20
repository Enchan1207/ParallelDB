#
# マルチスレッドDB処理
#
from lib.DBQueue import DBQueue
import threading

#--デキュースレッドを立てる
def dequeueThread():
    queue4Dequeue = DBQueue()
    queue4Dequeue.connect("db/main.db")
    queue4Dequeue.deQueue(120)

dqthread = threading.Thread(target=dequeueThread)
dqthread.setDaemon(True) #デーモンスレッド化しないとタイムアウトするまで終わらなくなる
dqthread.start()

#--こっちはサンプルスレッド
def fc1():
    event = threading.Event()
    queue = DBQueue()
    queue.initClient("Client-1")
    queue.enQueue("Client-1", event, "SELECT * FROM testTable")
    event.wait()
    event.clear()
    print(queue.fetchrst("Client-1"))

def fc2():
    event = threading.Event()
    queue = DBQueue()
    queue.initClient("Client-2")
    queue.enQueue("Client-2", event, "INSERT INTO testTable VALUES(0, ?)", ("Bob", ))
    event.wait()
    event.clear()
    print(queue.fetchrst("Client-2"))

thr1 = threading.Thread(target=fc1)
thr2 = threading.Thread(target=fc2)

thr1.start()
thr2.start()
