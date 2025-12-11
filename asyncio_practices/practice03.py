# example of running many coroutines concurrently
import random
import asyncio

"""
Bài toán: Hệ thống pha chế đồ uống (Barista Simulator)
Kịch bản: 
	- Bạn là một lập trình viên viết phần mềm cho một con robot pha chế. 
	- Cửa hàng nhận được một loạt đơn hàng cùng lúc (Cafe, Trà sữa, Sinh tố, Nước ép). 
	- Mỗi món tốn thời gian pha chế khác nhau. Robot có nhiều tay máy nên có thể pha tất cả cùng một lúc.
"""


async def make_drink(drink_name):
	if drink_name == "Mắm Tôm Latte":
		raise ValueError("Món này kinh quá, robot từ chối pha!")

	time_make = random.uniform(1, 3)
	print(f"Bắt đầu pha {drink_name}...")
	await asyncio.sleep(time_make)
	print(f"{drink_name} đã hoàn thành sau {time_make:.2f}s!")
	return time_make, f"{drink_name} ngon tuyệt"

async def main():

	orders = ["Cafe Đen", "Trà Sữa", "Sinh Tố Bơ", "Bạc Xỉu", "Mắm Tôm Latte"]
	tasks = [make_drink(order) for order in orders]
	results = await asyncio.gather(*tasks, return_exceptions=True)

	success_time = []

	for i, result in enumerate(results):
		if isinstance(result, Exception):
			print(f"{orders[i]} thất bại: {result}")
		else:
			time_make, message = result
			success_time.append(time_make)
			print(f"{orders[i]} thành công: {message}")

	if success_time is not None:
		print(f"Tổng thời gian hoàn thành: {max(success_time)}")
	else:
		print(f"Không có món nào thành công cả!")

if __name__ == '__main__':
	asyncio.run(main())