import matplotlib.pyplot as plt
import numpy as np

size = 6
y1 = [0.75, 0.81, 0.86, 0.91, 0.95, 1.0]
y2 = [1.49, 1.63, 1.74, 1.88, 1.97, 2.11]

plt.grid()
x = np.arange(size)
total_width, n = 0.5, 2  # 有多少个类型，只需更改n即可
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x, y1, width=width, label='Original sealing', color='lightskyblue')
plt.bar(x + width, y2, width=width, label='Sealing with our scheme', color='lightcoral')
# plt.bar(x + 2 * width, y3, width=width, label='label3', color='green')

plt.xticks()
plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体，则在此处设为：SimHei
plt.ylabel('Communication costs (s)')
plt.xlabel('Number of blocks')
plt.rcParams['savefig.dpi'] = 600  # 图片像素
plt.rcParams['figure.dpi'] = 600  # 分辨率
plt.rcParams['figure.figsize'] = (30.0, 16.0)  # 尺寸
# plt.title("title")
plt.savefig('./communication_costs.png', format='png')
plt.show()
