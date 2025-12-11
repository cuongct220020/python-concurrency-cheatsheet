# example of sharing data between coroutines using a queue

"""
Kiến thức của bài học này:
1. Giao tiếp an toàn giữa các Coroutine:
    - Bình thường các coroutine chạy độc lập. Để truyền dữ liệu từ coroutine A sang B một cách an toàn (tránh tranh chấp tài nguyên), ta dùng asyncio.Queue. 
    - Đây là hàng đợi FIFO (First In, First Out)
2. Cơ chế Blocking tự động
    - await queue.get(): nếu hàng đợi rỗng, Consumer tự động ngủ, chờ đến khi có dữ liệu mới. Bạn không cần viết vòng lặp while kiểm tra liên tục (gây tốn CPU). 
    - await queue.put(): Nếu hàng đợi đầy (nếu bạn set maxsize), Producer sẽ tạm dừng chờ Consumer lấy bớt ra. 
3. Sentinel Value (Tín hiệu kết thúc)
    - Làm sao Consumer biết khi nào Producer đã làm xong việc?
    - Kỹ thuật chuẩn là Producer gửi một giá trị đặc biệt (trong bài là None) vào cuối hàng đợi. Khi Consumer gặp None, nó hiểu là "hết hàng rồi" và thoát vòng lặp. 

Bài tập thực hành: Hệ thống xử lý giá Crypto
Kịch bản:
    - Producer (Market Data Feeder): Giả lập việc lấy giá Bitcoin từ sàn giao dịch cứ mỗi 1 giây.
    - Consumer (Price Analyzer): Nhận giá từ hàng đợi và kiểm tra xem giá có cao bất thường không để báo động.
"""

import random
import asyncio

# Producer
async def generate_market_data(queue):
    for i in range(1, 5):
        price = random.randint(30000, 35000)
        await queue.put(price)
        print(f"[[Producer] Đẩy giá {price} vào hàng đợi]")
        await asyncio.sleep(1)

    await queue.put(None)

# Consumer
async def process_data(queue):
    while True:
        price = await queue.get()
        if price is None:
            print("[Consumer] Đã xử lý xong dữ liệu!")
            break
        elif price > 34000:
            print(f"[Consumer] Giá cao quá ({price})! Bán ngay")
        else:
            print(f"[Consumer] Giá {price} bình thường.")


async def main():
    queue = asyncio.Queue()

    # Create Producer Task
    producer_task = asyncio.create_task(generate_market_data(queue))

    # Create Consumer Task
    consumer_task = asyncio.create_task(process_data(queue))

    # Gather task
    await asyncio.gather(producer_task, consumer_task)

if __name__ == '__main__':
    asyncio.run(main())