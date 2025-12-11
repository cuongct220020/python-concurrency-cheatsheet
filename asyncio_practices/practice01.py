# example of running a coroutine
import asyncio


async def test_async():
	print('Executing Code')

async def square(num: int):
	return num * num


if __name__ == '__main__':
	try:
		# print(test_async()) # <coroutine object test_async at 0x106619c00>
		asyncio.run(test_async()) # create the coroutine and run it in the event loop
		result = asyncio.run(square(10))
		print(result)
	except Exception as e:
		# sys:1: RuntimeWarning: coroutine 'test_async' was never awaited if not specify asyncio.run()
		raise e