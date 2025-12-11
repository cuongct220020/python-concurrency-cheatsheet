# example of scheduling an async task
import asyncio

# async def coro():
# 	pass

# asyncio.create_task(coro()) biến một hàm async thành một task và ném vào Event Loop để chạy ngầm.
# task = asyncio.create_task(coro())

# await task: khi bạn thực sự cần kết quả của task hoặc cần đảm bảo nó xong, bạn mới dùng lệnh này.

async def water_boiling():
	print("Starting Boiling Water...")
	await asyncio.sleep(2)
	print("Boiled Water!")


async def crawl_data():
	await asyncio.sleep(2)
	return f"Important Data!"


async def long_task():
	print("Starting Long Task...")
	await asyncio.sleep(5)
	print("Completed Long Task!")


async def setup_camera():
	print("--- [Camera] Start ---")
	await asyncio.sleep(3)
	return f"--- [Camera] Ready! ---"


async def main():
	try:
		# task1 = asyncio.create_task(water_boiling())
		# print("Cutting Spring Onions...")
		# await asyncio.sleep(1)
		# await task1

		# task2 = asyncio.create_task(crawl_data())
		# result = await task2
		# print(result)

		# task3 = asyncio.create_task(long_task())
		# await asyncio.sleep(1)
		# print("Main Task Completed!") # 'Completed Long Task!' cannot print on console

		print("Starting Main...")
		task4 = asyncio.create_task(setup_camera())

		# Này Event Loop, tôi (main) tạm dừng 0 giây, anh hãy tranh thủ chạy các task khác đang chờ trong hàng đợi (Queue) đi.
		await asyncio.sleep(0)
		print(await task4)

	except Exception as e:
		raise e


if __name__ == '__main__':
	asyncio.run(main())
