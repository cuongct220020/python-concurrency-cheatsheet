# SuperFastPython.com
# example of killing a process
from time import sleep
from multiprocessing import Process

# custom task function
def task():
    # execute a task in a loop
    while True:
        # block for a moment
        sleep(1)
        # report a message
        print('Worker process running...', flush=True)

# entry point
if __name__ == '__main__':
    # create a process
    process = Process(target=task)
    # run the process
    process.start()
    # wait for a moment
    sleep(5)
    # kill the process
    process.kill()
    # continue on...
    print('Parent is continuing on...')
