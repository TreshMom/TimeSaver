import threading
import time
import asyncio

lock = threading.Lock()

shared_list = []
def addMsg(item):
    with lock:
        shared_list.append(item)

def notifyMsgs():
    with lock:
        print(shared_list)
        time.sleep(1)
        for i in shared_list:
            if i.is_empty():
                asyncio.run(i.send())
    

# lock = threading.Lock()


# def add_to_shared_list(item):
#     with lock:
#         shared_list.append(item)

# def print_shared_list():
#     with lock:
#         print(shared_list)

def loop():
    while True:
        notifyMsgs()
        time.sleep(0.1)

# def push():
#     for i in range(1,20):
#         add_to_shared_list(i)
#         time.sleep(0.5)

# thread1 = threading.Thread(target=loop)
# thread1.daemon = True
# thread1.start()

