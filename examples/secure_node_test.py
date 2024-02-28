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

    def renew(self):
        self.num = random.randint(1, 2 * (100 + 1))
        self.s = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])
        self.r = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])

    def test(self):
        print(' ------Start------ ')

        for i in range(0, self.sealer_num):
            self.node_list[i].start()

        time.sleep(1)

        for i in range(0, self.sealer_num):
            self.node_list[i].key_pair_generate()

        for i in range(0, self.sealer_num):
            for j in range(0, self.sealer_num):
                if i != j:
                    self.node_list[i].connect_with_node("localhost", 10001 + j)

        for i in range(0, self.sealer_num):
            self.node_list[i].print_connections()

        time.sleep(2)

        seal_times = self.sealer_num * 2  # 在这里设置出块数

        for i in range(0, seal_times):
            p = i % self.sealer_num
            self.node_list[p].seal_block({"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
            time.sleep(self.time_limit)
            self.renew()

        time.sleep(3.2)

        for i in range(0, self.sealer_num):
            self.node_list[i].save_data()
            self.node_list[i].stop()
            self.node_list[i].join()

        print(' ------End------ ')


if __name__ == '__main__':
    nt = NodeTest(9)
    nt.test()
