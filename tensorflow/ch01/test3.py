# 矩阵
import tensorflow as tf

data1 = tf.constant([[6, 7]])
data2 = tf.constant([[2], [2]])
data3 = tf.constant([[3, 3]])
data4 = tf.constant([[1, 2], [3, 4], [5, 6]])
print(data4[0])  # 第0行
print(data4[:, 1])  # 所有行第1列
print(data4[1, 1])  # 第1行第1列

# 运算

# 矩阵加法必须行列相等
# 矩阵乘法 第一个矩阵的列必须等于第二个矩阵的行
data5 = tf.constant([[6, 7], [8, 9]])
data6 = tf.constant([[1, 1], [2, 2]])
matAdd = tf.add(data5, data6)
print('matAdd', matAdd)

data7 = tf.constant([[6, 7], [8, 9], [1, 3]])
data8 = tf.constant([[1, 1, 3], [2, 2, 3]])
matMul = tf.matmul(data7, data8)
print('matMul', matMul)

print(tf.matmul(data1, data2))

# 空矩阵
mat1 = tf.zeros([2, 3])
print(mat1)
# 初始填充
mat2 = tf.fill([2, 3], 15)
print(mat2)

# 复制矩阵结构
mat3 = tf.zeros_like(mat2)
print(mat3)

# 随机矩阵
mat4 = tf.random_uniform_initializer([2, 3], -1, 2)
print(mat4)
