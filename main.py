#
# マルチスレッドDB処理
#
from lib.DBQueue import DBQueue
import threading

#--デキュースレッド
def dequeueThread():
    queue4Dequeue = DBQueue()
    queue4Dequeue.connect("db/main.db")
    queue4Dequeue.deQueue(120)

dqthread = threading.Thread(target=dequeueThread)
dqthread.setDaemon(True) #デーモンスレッド化しないとタイムアウトするまで終わらなくなる
dqthread.start()

def fc1():
    event = threading.Event()
    queue = DBQueue()
    queue.initClient("Client-1")
    queue.enQueue("Client-1", event, "SELECT * FROM testTable")
    event.wait()
    event.clear()
    print(queue.fetchrst("Client-1"))

thr1 = threading.Thread(target=fc1)
thr1.start()

