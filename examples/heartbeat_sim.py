import sys
import time
import random
import math
from p2psecure.securenode import SecureNode
from p2psecure.hierarchy_node_selection import HierarchyNodeSelection

sys.path.insert(0, '..')


class HeartbeatTest:
    def __init__(self, n):
        self.num = 0
        self.s = 'XiG'
        self.r = 'XiG'
        self.sealer_num = n
        self.time_limit = 25
        self.time_detection = math.floor(self.time_limit / 2)
        self.select_node_num = self.sealer_num
        self.node_list = []
        self.select_node_list = []

        for i in range(1, self.sealer_num + 1):
            self.node_list.append(SecureNode("localhost", 10000 + i, self.sealer_num, self.select_node_num))

        for i in range(0, self.sealer_num):
            self.node_list[i].start()

        time.sleep(1)

        for i in range(0, self.sealer_num):
            self.node_list[i].key_pair_generate()

        for i in range(0, self.sealer_num):
            for j in range(0, self.sealer_num):
                if i != j:
                    self.node_list[i].connect_with_node("localhost", 10001 + j)

        print(' ------Start------ ')

    def test(self):
        self.select_node_num = 5  # 设置检测节点数量
        # for i in range(0, self.sealer_num):
        #     self.node_list[i].print_connections()

        seal_times = self.sealer_num * 1  # 在这里设置出块数量

        for i in range(0, seal_times):
            # self.heartbeat_seal(i)
            self.cloning_attack_seal(i)
        # 克隆攻击模拟



        # self.heartbeat_seal(0)

        self.stop_test()

    def heartbeat_seal(self, sealer_id):
        self.creaet_hns_data(self.sealer_num, sealer_id)
        if self.select_node_list is None:
            self.node_list[sealer_id].heartbeat_detection()  # 进行心跳检测
            time.sleep(self.time_detection)
            self.node_list[sealer_id].seal_block_with_heartbeat(
                {"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
            self.renew()
            time.sleep(self.time_limit - self.time_detection)
        else:
            nodes = []
            for i in self.select_node_list:
                nodes.append(10001 + i)
            self.node_list[sealer_id].heartbeat_detection_ip("localhost", nodes)
            time.sleep(self.time_detection)
            self.node_list[sealer_id].seal_block_with_heartbeat(
                {"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
            self.renew()
            time.sleep(self.time_limit - self.time_detection)

    def cloning_attack_seal(self, sealer_id):
        ports = []

        for i in range(0, self.sealer_num, 2):
            if i != sealer_id:
                ports.append(10001 + i)

        self.node_list[sealer_id].heartbeat_detection_ip("localhost", ports)
        time.sleep(self.time_detection)
        self.node_list[sealer_id].seal_block_with_heartbeat(
            {"data": self.s + ' send ' + str(self.num + 1) + ' coins to ' + self.r}, "block")
        self.renew()
        time.sleep(self.time_limit - self.time_detection)

    def stop_test(self):
        for i in range(0, self.sealer_num):
            self.node_list[i].save_data()
            self.node_list[i].stop()
            self.node_list[i].join()
        print(' ------End------ ')

    def renew(self):
        self.num = random.randint(1, 999)
        self.s = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])
        self.r = random.choice(['Alice', 'Bob', 'Charlie', 'Dave', 'Isaac', 'Justin', 'XiG', 'Leary'])

    def creaet_hns_data(self, n, id):
        """create random HNS data for test"""
        cw = []
        hwd = []
        t = []
        for i in range(0, n):
            cwi = {}
            hwdi = {}
            ti = {}
            data_number = random.randint(1, 5)
            for j in range(0, data_number):
                cwi.update({random.randint(1, 10): random.randint(1, 10)})
            cw.append(cwi)

            data_number = random.randint(1, 5)
            for j in range(0, data_number):
                hwdi.update({random.randint(1, 10): random.randint(1, 10)})
            hwd.append(hwdi)

            data_number = random.randint(1, 5)
            for j in range(0, data_number):
                ti.update({random.randint(10, 2000): random.randint(1, 10)})
            t.append(ti)

        hns = HierarchyNodeSelection(self.sealer_num, cw, hwd, t, id)
        self.select_node_list = hns.select_node_hierarchy(self.select_node_num)


if __name__ == "__main__":
    n = 9
    ht = HeartbeatTest(n)
    ht.test()
