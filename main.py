import Server
import sys


def main():
    if len(sys.argv) != 3:
        print("Parameter error")
        return
    ip = sys.argv[1]
    port = int(sys.argv[2])
    server = Server.Server(ip, port)
    # server = Server.Server("localhost", 35410)
    server.start()


if __name__ == '__main__':
    main()

