# example of a parallel for loop with the ProcessPoolExecutor class
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import time

def fibo(n: int):
    if n <= 1:
        return n

    return fibo(n - 1) + fibo(n - 2)


if __name__ == '__main__':
    arr = [30, 32, 34, 35, 36, 34]
    start = time.time()

    with ProcessPoolExecutor() as executor:
        future_to_num = {executor.submit(fibo, val): val for val in arr}

        for future in concurrent.futures.as_completed(future_to_num):
            original_num = future_to_num[future]
            try:
                result = future.result()
                print(f"Fibo: {original_num} = {result}")
            except Exception as exc:
                print(f"Fibo: {original_num} bị lỗi {exc}")

    end = time.time()
    print(f"Hoan thanh trong: {end - start} seconds")