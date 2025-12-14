# get the http status of a webpage
import asyncio

"""
Kiến thức bài học: Trước đây bạn có thể dùng các thư viện như requests hay aiohttp để gọi API.
Đó là thư viện cấp cao (High-Level) đã làm bộ bạn mọi thứ. 

Bài này bóc trần lớp vỏ đó ra để bạn thấy máy tính thực sự giao tiếp với nhau: 
1. asyncio.open_connection: Tạo một đường ống (socket TCP) kết nối trực tiếp đến Server.

2. StreamReader & StreamWriter:
    - writer: Dùng để gửi dữ liệu đi (như bạn hét vào đường ống)
    - reader: Dùng để nghe dữ liệu về (như việc bạn ghé tai vào đường ống)

3. Giao thức thủ công: Bạn đang phải tự tay viết đúng cú pháp của giao thức HTTP. 
Nếu bạn viết sai một dấu cách hay thiếu \r\n, Server sẽ không hiểu.


Bài tập thực hành: Hãy viết một chương trình "HTTP Header Inspector". Thay vì chỉ đọc dòng trạng thái (200 OK), 
bạn hãy đọc và in ra toàn bộ Headers mà server trả về (ví dụ: Server loại gì, ngày giờ, loại nội dung...).
"""

async def main():
    host = 'example.com'
    port = 80  # Dùng cổng 80 cho HTTP thường, đỡ phải config SSL

    print(f"Connecting to {host}...")

    # 1. Mở kết nối (open_connection)
    reader, writer = await asyncio.open_connection(host, port)

    # 2. Tạo request string (Lưu ý: HTTP yêu cầu xuống dòng bằng \r\n)
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    # 3. Gửi request (encode -> write -> drain)
    writer.write(request.encode())
    await writer.drain()


    print("--- HEADERS RECEIVED ---")
    # 4. Vòng lặp đọc từng dòng (readline)
    while True:
        line_bytes = await reader.readline()
        if not line_bytes:
            break

        line_str = line_bytes.decode().strip()
        if line_str == "":
            break

        print(line_str)

    # 5. Đóng kết nối
    writer.close()


if __name__ == '__main__':
    asyncio.run(main())