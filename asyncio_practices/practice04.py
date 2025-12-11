# example of waiting for a collection of tasks
import random
import asyncio

"""
Bài tập: Cuộc đua của các Server
Kịch bản: 
	- Bạn cần lấy dữ liệu user. Bạn gửi request đến 3 server: "Server US", "Server Singapore", "Server Japan".
	- Mỗi server phản hồi mất thời gian ngẫu nhiên (dùng random.uniform(1, 5)).
	- Server nào xong trước thì in ra kết quả và kết thúc chương trình chính.
"""

async def fetch_data(server_name):
	response_time = random.uniform(1, 5)
	await asyncio.sleep(response_time)
	return f"Data from {server_name} sau: {response_time}!"

async def main():
	servers = ["Server US", "Server Singapore", "Server Japan"]
	tasks = [asyncio.create_task(fetch_data(server)) for server in servers]
	done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

	finished_task = done.pop()
	print(f"Winner: {finished_task.result()}")

	print(f"Đang huỷ {len(pending)} server chậm hơn...")
	for task in pending:
		task.cancel()

	await asyncio.sleep(0.1)
	print("Đã dọn dẹp xong!")


if __name__ == '__main__':
	asyncio.run(main())
