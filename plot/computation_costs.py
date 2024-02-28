import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体，则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
A = np.array(
    [0, 0.019551992, 0.03883791, 0.059290648, 0.078893661, 0.098425865, 0.1179657, 0.13749456, 0.156843424, 0.175904512,
     0.194018364, 0.213230371, 0.233722448, 0.25490952, 0.27437949, 0.29374051, 0.31308341, 0.3325274])
B = np.array([0, 0.038552046, 0.08435535, 0.134988308, 0.183243275, 0.231801272, 0.27928758, 0.32357335, 0.375901461,
              0.423469544, 0.46774292, 0.515706539, 0.560789585, 0.60543942, 0.64968204, 0.6994679, 0.7504828,
              0.80421066])
C = np.array([0, 0.017800808, 0.07026982, 0.108886957, 0.148254156, 0.187499285, 0.22668791, 0.27841592, 0.326951027,
              0.366243839, 0.404932976, 0.444133997, 0.483304977, 0.52215862, 0.56076956, 0.60006976, 0.63907123,
              0.65943146

              ])
# D = np.array([0.9664, 0.6701, 0.9884, 0.7929, 0.8790, 0.6072, 0.9352, 0.7920, 0.9170, 0.9254])

# label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(12, 8))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
# ax.spines['top'].set_visible(False)  # 去掉上边框
# ax.spines['right'].set_visible(False)  # 去掉右边框

plt.plot(x, A, marker='o', color="blue", label="Original sealing", linewidth=3)
plt.plot(x, B, "o--", color="red", label="Our scheme", linewidth=3)
plt.plot(x, C, "o-.", color="green", label="Seal under the cloning attack", linewidth=3)
# plt.plot(x, D, "r--", label="D algorithm", linewidth=1.5)

group_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                '17']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=24, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=24, fontweight='bold')
# plt.title("Computation costs", fontsize=26, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Number of Blocks", fontsize=26, fontweight='bold')
plt.ylabel("Computation costs(s)", fontsize=26, fontweight='bold')
plt.xlim(0, 18)  # 设置x轴的范围
plt.ylim(0, 0.85)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=24, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./Computation Overhead.png', format='png')  # 建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
plt.show()
