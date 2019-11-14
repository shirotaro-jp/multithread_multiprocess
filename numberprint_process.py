# Processを使って100個の処理を並列化
# 参考 https://www.yoheim.net/blog.php?q=20170601
# プロセス間でデータを共有するには、Queue、Pipe、Value、Array、Managerなどの方法がある
# rasppy zero でも問題なく動く　スタートまで時間がかかる

import time
import multiprocessing
from multiprocessing import Queue
import random
import os

# 毎秒print
def number_print(q):
    number = 0
    while True:
        number = int(random.random() * 10)
        # print(number)
        if number == 6:
            break
        time.sleep(1)
    q.put(number)

# 10秒カウント
def count_10sec():
    print('10count')
    time.sleep(10)
    # print('10sec')


if __name__ == "__main__":
    # print(os.cpu_count())
    # print(len(os.sched_getaffinity(0)))

    prosesses = []
    queues = []
    for _p in range(99):
        q = Queue()
        queues.append(q)
        prosesses.append(multiprocessing.Process(target=number_print, args=(q,)))
    time_process = multiprocessing.Process(target=count_10sec)
    # count_10sec()
    # async_result.get()
    number = None
    counter = 0
    try:
        for i in range(len(prosesses)):
            prosesse = prosesses[i]
            prosesse.start()
        time_process.start()

        while True:
            if len(prosesses) == 0:
                number = 0
                for n in range(len(queues)):
                    number += queues[n].get()
                break
            for i in range(len(prosesses)):
                prosesse = prosesses[i]
                if not prosesse.is_alive():
                    prosesses.pop(i)
                    counter += 1
                    break
            if not time_process.is_alive():
                number = 'end'
                break
        print(number)
        print(counter)
    except:
        print('Error')
    finally:
        for i in range(len(prosesses)):
            prosesse = prosesses[i]
            prosesse.terminate()
        time_process.terminate()
        print('fin')

    # q_a = Queue()
    # q_b = Queue()

    # process_a = multiprocessing.Process(target=number_print, args=(q_a,))
    # process_b = multiprocessing.Process(target=number_print, args=(q_b,))
    # time_process = multiprocessing.Process(target=count_10sec)
    # # count_10sec()
    # # async_result.get()
    # number = None

    # try:
    #     process_a.start()
    #     process_b.start()
    #     time_process.start()
    #     while True:
    #         if not process_a.is_alive() and not process_b.is_alive():
    #             number = q_a.get() * q_b.get()
    #             break
    #         if not time_process.is_alive():
    #             number = 'end'
    #             break
    #     print(number)
    # except:
    #     print('Error')
    # finally:
    #     process_a.terminate()
    #     process_b.terminate()
    #     time_process.terminate()
    #     print('fin')

