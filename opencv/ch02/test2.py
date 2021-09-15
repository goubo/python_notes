import matplotlib.pyplot as plt
import numpy as np

data = np.linspace(1, 15)  # 线性增长的数据
beginPrice = np.array(
    [2438.71, 2500.88, 2534.95, 2512.52, 2594.04, 2743.26, 2697.47, 2695.24, 2678.23, 2722.13, 2674.93, 2744.13,
     2717.46, 2832.73, 2877.40])
endPrice = np.array(
    [2511.90, 2538.26, 2510.68, 2591.66, 2732.98, 2701.69, 2701.29, 2678.67, 2726.50, 2681.50, 2739.17, 2715.07,
     2823.58, 2864.90, 2919.08])

plt.figure()

for i in range(0, 15):
    dataOne = np.zeros([2])
    dataOne[0] = i
    dataOne[1] = i
    priceData = np.zeros([2])
    priceData[0] = beginPrice[i]
    priceData[1] = endPrice[i]
    if priceData[1] > priceData[0]:
        plt.plot(dataOne, priceData, 'r', lw=10)
    else:
        plt.plot(dataOne, priceData, 'g', lw=10)
plt.show()
