import sys
import getopt
import requests
import configparser


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:", ["delay="])
    except getopt.GetoptError:
        print('slave.py -d <delay>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('slave.py -d <delay>')
            sys.exit()
        elif opt in ("-d", "--delay"):
            slave = Slave(arg)
            result = slave.postmanEchoRequest()
            if result == 0:
                sys.exit(0)
            elif result == 1:
                sys.exit(1)
            else:
                sys.exit(2)


class Slave:
    def __init__(self, delay): self.delay = delay

    def postmanEchoRequest(self):
        config = configparser.ConfigParser()
        config.read('slave.ini')
        baseUrl = config['DEFAULT']['BaseUrl']

        try:
            result = requests.get(f'{baseUrl}{self.delay}')
        except Exception as e:
            print('Exception is %s', str(e))
            return 2

        if result.status_code == 200:
            return 0

        return 1


if __name__ == "__main__":
    main(sys.argv[1:])
