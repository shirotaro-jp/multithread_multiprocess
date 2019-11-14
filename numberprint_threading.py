# threadingを使って100個の処理を並行化
# rasppy zero でも問題なく動く

import time
import threading
import random
import os

# 毎秒print
def number_print():
    number = 0
    while True:
        number = int(random.random() * 10)
        # print(number)
        if number == 6:
            break
        time.sleep(1)
    numbers.append(number)

# 10秒カウント
def count_10sec():
    print('10count')
    time.sleep(10)
    # print('10sec')


if __name__ == "__main__":
    # print(os.cpu_count())
    # print(len(os.sched_getaffinity(0)))

    threads = []
    for _t in range(99):
        threads.append(threading.Thread(target=number_print, daemon=True))
    time_thread = threading.Thread(target=count_10sec, daemon=True)

    number = None
    numbers = []
    counter = 0
    try:
        for i in range(len(threads)):
            thread = threads[i]
            thread.start()
        time_thread.start()

        while True:
            if len(threads) == 0:
                number = 0
                for n in range(len(numbers)):
                    number += numbers[n]
                break
            for i in range(len(threads)):
                thread = threads[i]
                if not thread.is_alive():
                    threads.pop(i)
                    counter += 1
                    break
            if not time_thread.is_alive():
                number = 'end'
                break
        print(number)
        print(counter)
    except:
        print('Error')
    finally:
        # デーモンでない生存中のスレッドが全てなくなると、 Python プログラム全体が終了します。
        print('fin')


    # thread_a = threading.Thread(target=number_print, daemon=True)
    # thread_b = threading.Thread(target=number_print, daemon=True)
    # time_thread = threading.Thread(target=count_10sec, daemon=True)

    # number = None
    # numbers = []

    # try:
    #     thread_a.start()
    #     thread_b.start()
    #     time_thread.start()
    #     while True:
    #         if not thread_a.is_alive() and not thread_b.is_alive():
    #             number = 1
    #             for num in numbers:
    #                 number *= num
    #             break
    #         if not time_thread.is_alive():
    #             number = 'end'
    #             break
    #     print(number)
    # except:
    #     print('Error')
    # finally:
    #     # デーモンでない生存中のスレッドが全てなくなると、 Python プログラム全体が終了します。
    #     print('fin')

