import numpy as np
import matplotlib.pyplot as plt
import cv2
import requests
from requests_toolbelt import MultipartEncoder
import time


def send_request(name, data):
    data = MultipartEncoder({
        "file": (name, data, "application/octet-stream")
    })
    headers = {
        "Content-Type": data.content_type
    }
    res = requests.post(url="http://128.95.190.63:8080/recognize/", headers=headers, data=data)
    print(res.text)


# 为线程定义一个函数
def test_image_size(image_names):
    record = []
    for name in image_names:
        request_times = 10
        total_time = 0
        image_data = open(name, "rb").read()
        for i in range(request_times):
            begin_time = time.time()
            send_request(name, image_data)
            end_time = time.time()
            total_time += end_time - begin_time
            time.sleep(1)
        record.append(total_time/request_times)
    end_time = time.time()
    return np.array(record)


def test_difference_location(image_name):
    pass


def test_concurrency():
    rtt = np.array([2.7809300422668457, 5.328959941864014, 6.47007372379303, 7.278146815299988])
    num = np.array([10, 20, 30, 40])
    # image 1
    plt.title("RTT and concurrent request")
    plt.plot(num, rtt*1000)
    plt.xlabel('concurrent request')
    plt.ylabel('RTT(ms)')
    plt.savefig('RTT and concurrent request.pdf')


def generate_image_names():
    image_sizes = [64, 128, 256, 512, 1024, 2048, 4096]
    names = []
    for s in image_sizes:
        names.append(str(s) + "cat.png")
    return names


def generate_plot():
    images_names = generate_image_names()
    image_sizes = np.array([64, 128, 256, 512, 1024, 2048, 4096])
    image_sizes = image_sizes * image_sizes * 3 / 1000 / 1000
    avg_response_time = test_image_size(images_names)
    throughput = image_sizes * 8 / avg_response_time
    # image 1
    plt.title("RTT and image size")
    plt.plot(image_sizes, avg_response_time*1000)
    plt.xlabel('image size(MB)')
    plt.ylabel('RTT(ms)')
    plt.savefig('RTT of size.pdf')
    # image 2
    plt.figure()
    plt.title("Throughput and image size")
    plt.plot(image_sizes, throughput)
    plt.xlabel('image size(MB)')
    plt.ylabel('Throughput(Mbps)')
    plt.savefig('Throughput of size.pdf')


def generate_images():
    image_sizes = [64, 128, 256, 512, 1024, 2048, 4096]

    image = cv2.imread("cat.png")

    for s in image_sizes:
        image = cv2.resize(image, [s, s])
        cv2.imwrite(str(s) + "cat.png", image)


def main():
    # generate_plot()
    test_concurrency()


if __name__ == "__main__":
    main()



