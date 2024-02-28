import sys
import time
import random
from p2psecure.securenode import SecureNode

sys.path.insert(0, '..')


class NodeTest:
    def __init__(self, n):
        self.num = 0
        self.s = 'XiG'
        self.r = 'XiG'
        self.sealer_num = n
        self.time_limit = 25
        self.node_list = []
        for i in range(1, self.sealer_num + 1):
            self.node_list.append(SecureNode("localhost", 10000 + i, self.sealer_num, self.sealer_num))

        for i in range(0, self.sealer_num):
            self.node_list[i].start()

        time.sleep(1)

        for i in range(0, self.sealer_num):
            self.node_list[i].key_pair_generate()

    def renew(self):
        self.num = random.randint(1, 999)
        self.s = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])
        self.r = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])

    def test(self):
        print(' ------Start------ ')

        for i in range(0, self.sealer_num):
            for j in range(0, self.sealer_num):
                if i != j:
                    self.node_list[i].connect_with_node("localhost", 10001 + j)

        for i in range(0, self.sealer_num):
            self.node_list[i].print_connections()

        time.sleep(self.time_limit)
        self.start_attack()  # 开始进行克隆攻击模拟

        time.sleep(3.2)

        for i in range(0, self.sealer_num):
            self.node_list[i].save_data()
            self.node_list[i].stop()
            self.node_list[i].join()

        print(' ------End------ ')

    def disc(self):
        for i in range(1, self.sealer_num):
            if i % 2 == 0:
                for j in range(1, self.sealer_num, 2):
                    print("S{0}与下面的节点断开链接".format(i + 1))
                    self.node_list[i].disconnect_with_ip("localhost", 10001 + j)

            else:
                for j in range(1, self.sealer_num, 2):
                    print("S{0}与下面的节点断开链接".format(i + 1))
                    self.node_list[i].disconnect_with_ip("localhost", 10002 + j)

    def start_attack(self):
        self.node_list[8].seal_block({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
        self.renew()
        time.sleep(self.time_limit)
        self.node_list[0].seal_block({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
        self.renew()
        time.sleep(self.time_limit)

        ports = []
        for i in range(1, self.sealer_num):
            if i % 2 == 0:
                ports.clear()
                for j in range(2, self.sealer_num, 2):
                    if self.node_list[i].port == 10001 + j:
                        continue
                    ports.append(10001 + j)
                ports.append(10001)
                self.node_list[i].seal_block_ip({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r},
                                                "block", "localhost", ports)
                self.renew()
                time.sleep(self.time_limit)

            else:
                ports.clear()
                for j in range(1, self.sealer_num, 2):
                    if self.node_list[i].port == 10001 + j:
                        continue
                    ports.append(10001 + j)
                ports.append(10001)
                self.node_list[i].seal_block_ip({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r},
                                                "block", "localhost", ports)
                self.renew()
                time.sleep(self.time_limit)

        ports.clear()
        ports.append(10002)
        ports.append(10004)
        ports.append(10006)
        ports.append(10008)
        self.node_list[0].seal_block_ip({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r},
                                        "block", "localhost", ports)


if __name__ == '__main__':
    nt = NodeTest(9)
    nt.test()
