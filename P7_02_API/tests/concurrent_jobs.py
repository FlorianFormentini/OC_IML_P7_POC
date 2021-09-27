import requests
import time


t0 = time.perf_counter()
# for i in range(10):
#     r = requests.post('https://hera-project.herokuapp.com/api/fbapp/test')
#     print(r.elapsed.total_seconds(), r.status_code)

r = requests.post('https://hera-project.herokuapp.com/api/fbapp/test')
t1 = time.perf_counter()
print(r.elapsed.total_seconds())
print('total time :', t1 - t0)