import MainBot
import Heap
import threading


def main():

    mainBot = MainBot.MainBot()
    heap = Heap.Heap()

    task1 = mainBot.run
    task2 = heap.run

    threadMainBot = threading.Thread()
    threaHeap = threading.Thread()

    threadMainBot.join()
    threaHeap.join()











if __name__ == "__main__":
    main()