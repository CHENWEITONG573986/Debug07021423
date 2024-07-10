"""人脸特征模型
这个网络使相似的面部特征更加接近。
"""

from .mobilenet_v2 import MobileNetv2

import keras.backend as K
from keras.layers import Input, Lambda
from keras.models import Model
from keras.utils.vis_utils import plot_model


def euclidean_distance(inputs):
    """欧几里得距离
    此函数用于计算两个特征的欧氏距离

    # 参数
        inputs: List, 两个特征
    # 返回
        Output: Double, 欧几里得距离
    """
    assert len(inputs) == 2, \
        '欧几里得距离需要两个输入, %d given' % len(inputs)
    u, v = inputs
    return K.sqrt(K.sum((K.square(u - v)), axis=1, keepdims=True))


def contrastive_loss(y_true, y_pred):
    """对比损失
    此函数用于计算对比损失


    # 参数
        y_true: Integer, 成对标记
        y_pred: Double, 欧氏距离
    # 返回
        Output: Double, 对比损失
    """
    margin = 1.
    """
    l1 = K.mean(y_true) * K.square(y_pred)
    l2 = (1 - y_true) *  K.square(K.maximum(margin - y_pred, 0.))
    loss = l1 + l2
    """
    return K.mean((1. - y_true) * K.square(y_pred) + y_true * K.square(K.maximum(margin - y_pred, 0.)))


def get_model(shape):
    """人脸特征网络
    这个网络使相似的面部特征更加接近。

    # 参数
        shape: 一个整数 或者 三个整数组成的元组/列表, 张量的尺寸
    # 返回
        输出模型
    """
    mn = MobileNetv2(shape)

    im1 = Input(shape=shape)
    im2 = Input(shape=shape)

    feat1 = mn(im1)
    feat2 = mn(im2)

    distance = Lambda(euclidean_distance)([feat1, feat2])

    face_net = Model(inputs=[im1, im2], outputs=distance)
    face_net.compile(optimizer='adam', loss=contrastive_loss)
    # plot_model(face_net, to_file='images/face_net.png', show_shapes=True)

    return face_net
