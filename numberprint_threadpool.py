# ThreadPoolを使って100個の処理を並列化
# rasppy zero でも問題なく動く　スタートまで多少時間がかかる

import time
from multiprocessing.pool import ThreadPool
import random
# import os

# 毎秒print
def number_print():
    number = 0
    while True:
        number = int(random.random() * 10)
        # print(number)
        if number == 6:
            break
        time.sleep(1)
    return number

# 10秒カウント
def count_10sec():
    print('10count')
    time.sleep(10)
    # print('10sec')


if __name__ == "__main__":
    # print(os.cpu_count())
    # print(len(os.sched_getaffinity(0)))

    pool = ThreadPool(processes=100)
    async_results = []
    for _p in range(99):
        async_results.append(pool.apply_async(number_print))
    time_result = pool.apply_async(count_10sec)
    # count_10sec()
    # async_result.get()
    number = None
    counter = 0
    while True:
        if len(async_results) == 0:
            number = 'all done'
            break
        for i in range(len(async_results)):
            async_result = async_results[i]
            if async_result.ready():
                async_results.pop(i)
                counter += 1
                break
        if time_result.ready():
            number = 'end'
            break
    print(number)
    print(counter)

    # pool = ThreadPool(processes=3)
    # async_result_a = pool.apply_async(number_print)
    # async_result_b = pool.apply_async(number_print)
    # time_result = pool.apply_async(count_10sec)
    # # count_10sec()
    # # async_result.get()
    # number = None
    # while True:
    #     print(str(async_result_a.ready()) + str(async_result_b.ready()))
    #     if time_result.ready():
    #         number = 'end'
    #         break
    #     time.sleep(1)
    # print(number)