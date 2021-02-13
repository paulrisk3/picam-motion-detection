import multiprocessing
import random
import time

def do_work(process_id):
    time.sleep( random.randint(1,10) )
    print('1 from process:', process_id)
    time.sleep( random.randint(1,10) )
    print('2 from process:', process_id)

processes = []

for i in range(3):
   process = multiprocessing.Process(target=do_work, args=[i])
   processes.append(process)
   process.start()

print('3 processes started.')

for process in processes:
    process.join()

print('3 processes finished.')
