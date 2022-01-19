# 自动求导 y = x ^ 2 ,当x = 一个变量的导

import tensorflow as tf

x = tf.Variable(initial_value=3.)  # 定义一个变量, 自动求导器需要使用变量 tf.Variable
with tf.GradientTape() as tape:
    y = tf.square(x)  # 录制函数
y_grad = tape.gradient(y, x)  # 求 y关于x的导数
print(y, y_grad)

 