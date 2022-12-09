import requests
from requests_toolbelt import MultipartEncoder
import time
import threading


avg_time = 0


def send_requests(thread_num, request_times):
    global avg_time
    begin_time = time.time()
    image_data = open(r"cat.png", "rb").read()
    for i in range(request_times):
        data = MultipartEncoder({
            "file": ("image"+str(thread_num)+str(i)+".png", image_data, "application/octet-stream")
        })
        headers = {
            "Content-Type": data.content_type
        }
        res = requests.post(url="http://128.95.190.63:8080/recognize/", headers=headers, data=data)
        print(res.text)
    end_time = time.time()
    avg_time += (end_time - begin_time) / request_times
    print("Average response time:", (end_time - begin_time) / request_times)


def start_threads():
    thread_num = 50
    request_times = 10
    threads = []
    begin_time = time.time()
    for i in range(thread_num):
        t = threading.Thread(target=send_requests, args=(i, request_times))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    end_time = time.time()
    print((end_time-begin_time)/request_times*thread_num, request_times*thread_num)


def main():
    start_threads()


if __name__ == "__main__":
    main()
