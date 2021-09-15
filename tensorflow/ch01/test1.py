import tensorflow as tf

data1 = tf.constant(6)
data2 = tf.Variable(10)
dataAdd = tf.add(data1, data2)  # 加
dataSub = tf.subtract(data1, data2)  # 减
dataMul = tf.multiply(data1, data2)  # 乘
dataDiv = tf.divide(data1, data2)  # 除
print(data1)
print(dataAdd, dataSub, dataMul, dataDiv)
