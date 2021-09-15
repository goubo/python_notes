# matplotlib 画图测试
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([3, 5, 7, 6, 3, 2, 8, 4])
plt.plot(x, y, 'r')  # 折线图
# plt.plot(x, y, 'g', lw=10)  # 折线图
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([13, 15, 17, 16, 13, 12, 18, 14])
plt.bar(x, y, 0.5, alpha=0.5, color='b')
plt.show()
