import asyncio

import MainBot
import Heap
import threading

mainBot = None
heap = None

def main():

    mainBot = MainBot.MainBot()
    heap = Heap.Heap()

    mainBotThread = threading.Thread(target=mainBot.run)
    heapThread = threading.Thread(target=heap.run)

    mainBotThread.start()
    heapThread.start()

    mainBotThread.join()
    heapThread.join()


if __name__ == "__main__":
    main()






if __name__ == "__main__":
    main()