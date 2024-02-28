from p2psecure.hierarchy_node_selection import HierarchyNodeSelection
import random
import math


def creaet_hns_data(n):
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

    return cw, hwd, t


class CAWH:
    def __init__(self, n):
        self.n = n
        self.sealers = list(range(1, n))
        random.shuffle(self.sealers)
        self.len = len(self.sealers)

    def start(self):
        suc = 0
        # 需要检测sealer数量
        select = self.n - 11
        re = math.floor(select / 2) + 2
        # re = math.floor(select/2) + 1 当sealer偶数情况下检测
        print("所需签名回执数量：{0}".format(re))

        if self.len % 2 != 0:
            print("list have ODD number of elements")
            exit()

        l_part = self.sealers[0: int(self.len / 2)]
        r_part = self.sealers[int(self.len / 2): self.len]
        l_part.append(0)
        r_part.append(0)
        l_part.sort()
        r_part.sort()
        print(l_part)
        print(r_part)

        for i in range(1, self.n):
            count = 0
            cw, hwd, t = creaet_hns_data(self.n)  # 随机生成测试数据
            hns = HierarchyNodeSelection(self.n, cw, hwd, t, i)
            print(i)
            sl = hns.select_node_hierarchy(select)
            print(sl)
            res = i in l_part

            if res:
                partition = l_part
            else:
                partition = r_part

            print(partition)
            for j in range(0, len(sl)):
                # print(sl[j])
                if sl[j] in partition:
                    count += 1
            print("有效re: {0} ".format(count))
            if count < re:
                print("检测成功")
                suc += 1
            else:
                print("检测失败")

        return suc


if __name__ == "__main__":
    cawh = CAWH(21)
    print("检测成功sealer数量：{0}".format(cawh.start()))
