import numpy as np

# np 矩阵
data1 = np.array([1, 2, 3, 4, 5])
print(data1)
data2 = np.array([[3, 6], [2, 3]])
print(data2)

print(data1.shape, data2.shape)

# 初始化矩阵
print(np.zeros([2, 3]))
print(np.ones([2, 3]))

# 修改矩阵
data2[1, 0] = 5

# 矩阵计算
# 矩阵和常数元素,每个元素都进行计算
data3 = np.ones([2, 3])
data4 = np.array([[2, 2, 2], [2, 2, 2]])
print(data3 + 2)
print(data3 + data4)
print(data3 * data4)
