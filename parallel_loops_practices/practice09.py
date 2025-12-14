"""
Đề bài: Đào Coin (Proof of Work Simulation)
Mục tiêu: Tìm một số bí mật (gọi là nonce) sao cho khi gộp với dữ liệu Block và băm ra,
mã hash bắt đầu bằng một số lượng số 0 nhất định (gọi là độ khó - difficulty).
"""

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import hashlib

def mine_block():
    pass


def mine_block(block_id, difficulty):
    target = "0" * difficulty
    nonce = 0

    while True:
        text = f"{block_id}{nonce}"

        hashed = hashlib.sha512(text.encode()).hexdigest()

        if hashed.startswith(target):
            print(f"Block {block_id} đã đào xong: Nonce: {nonce}, Hash: {hashed}")
            break

        nonce += 1


def main():
    jobs = [(1, 4), (2, 5), (3, 6)]

    with ProcessPoolExecutor() as executor:
        futures = []
        for block_id, difficulty in jobs:
            futures.append(executor.submit(mine_block, block_id, difficulty))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    main()