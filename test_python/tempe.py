# 温度预测训练
import warnings

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing
from tensorflow.keras import layers

warnings.filterwarnings("ignore")

# 读取数据
features = pd.read_csv("temp.csv")
features.head()

print('维度', features.shape)
# 实际温度指标
labels = np.array(features['最高温度'])  # x
features = features.drop('最高温度', axis=1)  # y
features_list = list(features.columns)
features = np.array(features)

# 预处理
input_features = preprocessing.StandardScaler().fit_transform(features)
print(input_features[0])
# 创建模型
model = tf.keras.Sequential()

model.add(layers.Dense(16))  # 添加第一个16个神经元的隐藏层  dense 全连接
model.add(layers.Dense(32))  # 32 个神经元的第二个隐藏层
model.add(layers.Dense(1))  # 输出层,只有1个值

# model.add(layers.Dense(16, kernel_initializer='random_normal'))  # 添加第一个16个神经元的隐藏层  dense 全连接
# # kernel_initializer 初始化方式,随机高斯分布
# model.add(layers.Dense(32, kernel_initializer='random_normal'))  # 32 个神经元的第二个隐藏层
# model.add(layers.Dense(1, kernel_initializer='random_normal'))  # 输出层,只有1个值


# model.add(layers.Dense(16, kernel_initializer='random_normal',
#                        kernel_regularizer=tf.keras.regularizers.l2(0.02)))  # 添加第一个16个神经元的隐藏层  dense 全连接
# # kernel_initializer 初始化方式,随机高斯分布
# model.add(layers.Dense(32, kernel_initializer='random_normal',
#                        kernel_regularizer=tf.keras.regularizers.l2(0.02)))  # 32 个神经元的第二个隐藏层
# model.add(
#     layers.Dense(1, kernel_initializer='random_normal', kernel_regularizer=tf.keras.regularizers.l2(0.02)))  # 输出层,只有1个值

# 优化器和损失函数
model.compile(optimizer=tf.keras.optimizers.SGD(0.001), loss='mean_squared_error')
# x,y
# validation_split 验证集,占数据的0.25
# epochs 迭代次数
# batch_size 每一次迭代样本数量
model.fit(input_features, labels, validation_split=0.25, epochs=20, batch_size=256)

# 测试
predict = model.predict(input_features)
print(predict)
