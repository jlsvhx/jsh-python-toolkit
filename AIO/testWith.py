import concurrent.futures

def task(num):
    import time
    time.sleep(num)
    print('Task %d is running.' % num)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(5):
            executor.submit(task, i)
    print("threadpoolexecutor fin")