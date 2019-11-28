import sys
import getopt
import asyncio
import random
import configparser


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print('master.py -d <delay>')
        sys.exit()
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == '-h':
                print('master.py -d <delay>')
                sys.exit()
    else:
        master = Master()
        master.requestFromSlave()


class Slave:
    def __init__(self, delay, repeat_times):
        self.delay = delay
        self.repeat_times = repeat_times
        self.exit_code = -1


class Master:

    def __initSlaveDict(self):
        slave_dict = {}
        for i in range(5):
            slave_dict['slave_' + str(i)] = Slave(random.randint(1, 5), 5)
        return slave_dict

    def __init__(self):
        self.slave_dict = self.__initSlaveDict()

    async def executeComandAsync(self, cmd):
        proc = await asyncio.create_subprocess_shell(cmd)
        await proc.communicate()
        return proc.returncode

    # Restart the slaves for at least 5 times until you get exit code 0
    def requestFromSlave(self):
        config = configparser.ConfigParser()
        config.read('master.ini')
        cmd = config['DEFAULT']['cmd']

        for slave in self.slave_dict:
            for repeat in range(self.slave_dict[slave].repeat_times, 0, -1):
                cmd = f'{cmd} {self.slave_dict[slave].delay}'

                if self.slave_dict[slave].exit_code != 0 and self.slave_dict[slave].repeat_times > 0:
                    result = asyncio.run(self.executeComandAsync(cmd))
                    self.slave_dict[slave].repeat_times = repeat - 1
                    self.slave_dict[slave].exit_code = result

                    print(
                        f'value in slave_dictionary {slave}, delay is {self.slave_dict[slave].delay}, exit code is {self.slave_dict[slave].exit_code} and repeat times is {self.slave_dict[slave].repeat_times}')

                    if result == 0:
                        break


if __name__ == "__main__":
    main(sys.argv[1:])
