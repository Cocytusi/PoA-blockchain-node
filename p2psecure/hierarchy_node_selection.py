import random


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


class HierarchyNodeSelection:
    def __init__(self, n, coin_set, hiswd, trans, id):
        self.sealer_id = id
        self.sealer_weight = []
        self.coin_weight_set = coin_set
        self.hwd = hiswd
        self.transactions = trans
        self.sealer_num = n
        self.Lt = 1000
        self.C = [0.2, 0.5]
        self.WS = [1, 1.1, 1.2]
        self.layers = 3
        # coin weight sum
        self.coin_weight = {}
        # HWD weight sum
        self.hwd_weight = {}
        # Transaction weight of weight
        self.transactions_weight = {}
        # The sum of the weight
        self.weight_sum_list = {}

        if len(self.coin_weight_set) != n:
            print("Data inconsistency!!!")

        self.weight_sum(0)

    def coin_weight_count(self, sealer):
        self.coin_weight.clear()
        m = 0
        a = 0
        for i in range(0, len(self.coin_weight_set)):
            ac = 0
            for k, v in self.coin_weight_set[i].items():
                ac = ac + (k * v)
            self.coin_weight[i] = ac
            if i == sealer:
                a = ac
            m += ac
        for i in range(0, len(self.coin_weight)):
            self.coin_weight[i] /= m
        return a / m

    def historical_weighted_difficulty(self, sealer):
        self.hwd_weight.clear()
        b = 0
        bi = 0
        for i in range(0, len(self.hwd)):
            w = 0
            for k, v in self.hwd[i].items():
                w += k * v
            b += w
            self.hwd_weight[i] = w

            if i == sealer:
                bi = w
        for i in range(0, len(self.hwd_weight)):
            self.hwd_weight[i] /= b
        return bi / b

    def transaction_weight_sealer(self, sealer):
        self.transactions_weight.clear()
        wt = 0
        wi = 0
        for i in range(0, len(self.transactions)):
            w = 0
            for k, v in self.transactions[i].items():
                w += self.transaction_weight(k) * v
            self.transactions_weight[i] = w
            if i == sealer:
                wi = w
            wt += w
        for i in range(0, len(self.transactions_weight)):
            self.transactions_weight[i] /= wt
        return wi / wt

    def transaction_weight(self, n):
        wt = 0
        if (self.C[1] * self.Lt) <= n <= self.Lt:
            c = 0.01
        elif (self.C[0] * self.Lt) <= n <= (self.C[1] * self.Lt):
            c = 0.5
        elif n <= (self.C[0] * self.Lt):
            c = 1
        else:
            c = 0

        wt += n * c
        return wt

    def weight_sum(self, sealer):
        self.coin_weight_count(sealer)
        self.historical_weighted_difficulty(sealer)
        self.transaction_weight_sealer(sealer)
        for i in range(0, self.sealer_num):
            self.weight_sum_list[i] = self.WS[0] * self.coin_weight[i] + self.WS[1] * self.hwd_weight[i] + self.WS[2] * \
                                      self.transactions_weight[i]
        return self.weight_sum_list

    def select_node_hierarchy(self, n):
        """n means how many node we need"""
        layers = []
        node_list = []

        # print(self.weight_sum_list)

        if n == self.sealer_num:
            for i in range(0, self.sealer_num):
                if self.sealer_id != i:
                    node_list.append(i)
            return node_list

        for i in list(self.weight_sum_list.keys()):
            if i == self.sealer_id:
                del self.weight_sum_list[i]

        wsl = sorted(self.weight_sum_list.items(), key=lambda kv: (kv[1], kv[0]))
        temp = self.dev(wsl, round(self.sealer_num / self.layers))

        for i in temp:
            layers.append(i)

        for x in range(0, n):
            i = x % self.layers
            if layers[i] is not None:
                j = random.randint(0, len(layers[i]) - 1)
                node_list.append(layers[i][j][0])
                del layers[i][j]

        node_list.sort()
        return node_list

    def dev(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


if __name__ == "__main__":
    n = 20
    id = 0
    # cw = [{1: 1, 2: 2}, {1: 2, 2: 4}, {2: 3, 4: 11}, {2: 3, 5: 11}, {2: 9, 4: 3}, {2: 1, 9: 1}, {10: 3, 9: 11}]
    # hwd = [{1: 4}, {1: 4, 2: 1}, {1: 10}, {3: 9}, {5: 6}, {8: 10}, {9: 6}]
    # t = [{100: 1, 400: 2, 900: 1}, {100: 1, 400: 9, 1500: 1}, {100: 10, 1500: 1}, {200: 1, 300: 6, 1200: 1},
    #      {500: 1, 700: 9, 900: 1}, {150: 1, 200: 2, 900: 1}, {100: 1, 300: 8, 500: 1}]
    # cw, hwd, t = creaet_hns_data(n)  # 随机生成测试数据
    # hns = HierarchyNodeSelection(n, cw, hwd, t, id)

    # print(cw)
    # print(hwd)
    # print(t)
    # print(hns.select_node_hierarchy(n))

    for i in range(0, n):
        cw, hwd, t = creaet_hns_data(n)  # 随机生成测试数据
        hns = HierarchyNodeSelection(n, cw, hwd, t, i)
        print(hns.select_node_hierarchy(n))
