# example of waiting for a collection of tasks
import random
import asyncio

"""
Bài toán: Hệ thống kiểm tra trạng thái (Ping) Server.
Kịch bản: 
	- Bạn là Admin quản lý 5 server. Bạn muốn kiểm tra xem server nào còn sống (Alive). 
	- Vì mạng chập chờn, thời gian phản hồi của mỗi server là khác nhau. 
	- Yêu cầu: Ngay khi server nào phản hồi, hãy in ra màn hình ngay lập tức để Admin biết, không cần đợi các server khác.
"""

async def ping_server(ip_address):
	response_time = random.uniform(1, 5)
	await asyncio.sleep(response_time)
	return f"{ip_address} is alive (ping: {response_time}s)"


async def main():
	ip_list = ["192.168.1.1", "192.168.1.2", "google.com", "vnexpress.net", "localhost"]
	tasks = [asyncio.create_task(ping_server(ip)) for ip in ip_list]

	for task in asyncio.as_completed(tasks):
		result = await task
		print(result)


if __name__ == '__main__':
	asyncio.run(main())