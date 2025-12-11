# SuperFastPython.com
# example of scheduling an async task
import asyncio

# # coroutine to perform some useful task
# async def task_coro():
# 	# report a message
# 	print('The task is running...')
# 	# suspend and sleep for a moment
# 	await asyncio.sleep(1)
# 	# report a message
# 	print('The task done')
# 	# return a result
# 	return 'The answer is 100'
#
# # main coroutine
# async def main():
# 	# run a task independently
# 	task = asyncio.create_task(task_coro())
# 	# suspend a moment, allow the scheduled task to run
# 	await asyncio.sleep(0)
# 	# wait for the async task to complete
# 	await task
# 	# report the return value
# 	print(f'Got: {task.result()}')
#
# # create the coroutine and run it in the event loop
# asyncio.run(main())

async def water_boiling():
	print("Starting Boiling Water...")
	await asyncio.sleep(2)
	print("Boiled Water!")


async def crawl_data():
	await asyncio.sleep(2)
	return f"Important Data!"


async def main():
	try:
		# task1 = asyncio.create_task(water_boiling())
		# print("Cutting Spring Onions...")
		# await asyncio.sleep(1)
		# await task1

		task = asyncio.create_task(crawl_data())
		result = await task
		print(result)

	except Exception as e:
		raise e


if __name__ == '__main__':
	asyncio.run(main())
