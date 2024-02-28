import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simsun']  # 如果要显示中文字体，则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
A = np.array(
    [0.4333, 0.9667, 0.3667, 0.9333, 0.3667, 0.9667, 0.3667, 0.9667, 0.3333, 0.9667, 0.4, 0.9, 0.3667, 0.9667, 0.4333,
     1, 0.5333, 1])
B = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
# C = np.array([0.9657, 0.6688, 0.9855, 0.7881, 0.8667, 0.5952, 0.9361, 0.7848, 0.9244, 0.9221])
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

plt.plot(x, A, marker='o', color="blue", label="原始方案", linewidth=3)
plt.plot(x, B, "*--", color="red", label="改进后的方案", linewidth=3)
# plt.plot(x, C, color="red", label="C algorithm", linewidth=1.5)
# plt.plot(x, D, "r--", label="D algorithm", linewidth=1.5)

group_labels = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=24, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=24, fontweight='bold')
# plt.title("Success Rate", fontsize=26, fontweight='bold')  # 默认字体大小为12
plt.xlabel("需要检测的验证人数量", fontsize=26, fontweight='bold')
plt.ylabel("检测成功率", fontsize=26, fontweight='bold')
plt.xlim(2, 21)  # 设置x轴的范围
plt.ylim(0, 1.1)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=24, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./sucRate.png', format='png')  # 建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
plt.show()
