""""
Trong thực tế, việc băm (hash) mật khẩu (như dùng Bcrypt hay Argon2) được thiết kế để chạy chậm (tốn CPU) nhằm chống lại các cuộc tấn công Brute-force.
Nếu hệ thống của bạn phải import 1.000 user cùng lúc, việc chạy tuần tự sẽ rất lâu.

Đề bài: Hệ thống Băm Mật Khẩu (Password Hashing)
Mục tiêu: Sử dụng kỹ thuật Dictionary mapping để xử lý song song và in kết quả chính xác không bị nhầm lẫn.

"""

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import hashlib

def slow_hash(password: str):
    salt = 'random-salt'
    hashed = password

    for _ in range(200000):
        text = f"{hashed}{salt}"
        hashed = hashlib.sha512(text.encode()).hexdigest()

    return hashed

def main():
    passwords = ["password123", "admin", "very_long_password_secure", "123456", "let_me_in"]

    with ProcessPoolExecutor() as executor:
        futures_to_pass = {
            executor.submit(slow_hash, password) : password for password in passwords
        }

        for future in concurrent.futures.as_completed(futures_to_pass):

            original_password = futures_to_pass[future]

            try:
                hash_result = future.result()
                print(f"Password: {original_password} -> Hash: {hash_result}")
            except Exception as exception:
                raise exception


if __name__ == '__main__':
    main()
