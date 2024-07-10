"""基于keras的MobileNet v2 模型.

# 参考
- [Inverted Residuals and Linear Bottlenecks Mobile Networks for
   Classification, Detection and Segmentation]
   (https://arxiv.org/abs/1801.04381)
"""


from keras.models import Model
from keras.layers import Input, Conv2D, GlobalAveragePooling2D
from keras.layers import Activation, BatchNormalization, add, Reshape
from keras.regularizers import l2
from keras.layers.advanced_activations import LeakyReLU
from keras.applications.mobilenet import relu6, DepthwiseConv2D
from keras import backend as K


def _conv_block(inputs, filters, kernel, strides):
    """卷积块
    这个函数用 BN 和 relu6 定义了一个二维图像卷积

    # 参数
        inputs: Tensor, conv层的输入张量
        filters: Integer, 输出空间的维数
        kernel: 一个整数或2个整数组成的元组/列表，指定
            二维卷积窗口的宽度和高度
        strides: 一个整数或者2个整数组成的元组/列表,
            指定卷积沿宽和高的步长, 可以用单个整数来
            指定所有空间维度的值

    # 输出
        输出张量
    """

    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1

    x = Conv2D(filters, kernel, padding='same', strides=strides)(inputs)
    x = BatchNormalization(axis=channel_axis)(x)
    return Activation(relu6)(x)


def _bottleneck(inputs, filters, kernel, t, s, r=False):
    """bottleneck
    此函数定义了一个基本的瓶颈结构。

    # 参数
        inputs: Tensor, conv层的输入张量
        filters: Integer, 输出空间的维数
        kernel: 可以是一个integer 或者 两个整数组成的tuple/list, 指定
            二维卷积窗口的宽度和高度
        t: Integer, 展开因子
            t 始终应用于输入的尺寸
        s: 可以是一个integer 或者 两个整数组成的tuple/list,
            指定卷积沿宽和高的步长, 可以用单个整数来
            指定所有空间维度的值

    # 返回
        输出张量
    """

    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    tchannel = K.int_shape(inputs)[channel_axis] * t

    x = _conv_block(inputs, tchannel, (1, 1), (1, 1))

    x = DepthwiseConv2D(kernel, strides=(s, s),
                        depth_multiplier=1, padding='same')(x)
    x = BatchNormalization(axis=channel_axis)(x)
    x = Activation(relu6)(x)

    x = Conv2D(filters, (1, 1), strides=(1, 1), padding='same')(x)
    x = BatchNormalization(axis=channel_axis)(x)

    if r:
        x = add([x, inputs])
    return x


def _inverted_residual_block(inputs, filters, kernel, t, strides, n):
    """Inverted Residual Block
    此函数定义一个由1个或多个相同层组成的序列

    # 参数
        inputs: Tensor, conv 层的输入张量
        filters: Integer, 输出空间的维数
        kernel: 一个整数或2个整数组成的元组/列表，指定
            二维卷积窗口的宽度和高度
        t: Integer, 展开因子
            t 始终应用于输入的尺寸
        s: 一个整数或者2个整数组成的元组/列表,
            指定卷积沿宽和高的步长, 可以用单个整数来
            指定所有空间维度的值
        n: Integer, 层重复次数.
    # 返回
        输出张量.
    """

    x = _bottleneck(inputs, filters, kernel, t, strides)

    for i in range(1, n):
        x = _bottleneck(x, filters, kernel, t, 1, True)

    return x


def MobileNetv2(input_shape):
    """MobileNetv2
    此函数定义了一个MobileNetv2体系结构

    # 参数
        input_shape: 一个整数或3个整数组成的元组/列表, 输入张量的尺寸
    # 返回
        MobileNetv2 模型
    """

    inputs = Input(shape=input_shape, name='single_input')
    x = _conv_block(inputs, 32, (3, 3), strides=(2, 2))

    # x = _inverted_residual_block(x, 16, (3, 3),  1, 1, 1)
    # x = _inverted_residual_block(x, 24, (3, 3),  6, 2, 2)
    # x = _inverted_residual_block(x, 32, (3, 3),  6, 2, 3)
    # x = _inverted_residual_block(x, 64, (3, 3),  6, 2, 4)
    # x = _inverted_residual_block(x, 96, (3, 3),  6, 1, 3)
    # x = _inverted_residual_block(x, 160, (3, 3), 6, 2, 3)
    # x = _inverted_residual_block(x, 320, (3, 3), 6, 1, 1)

    x = _inverted_residual_block(x, 64, (3, 3), t=5, strides=2, n=2)
    x = _inverted_residual_block(x, 128, (3, 3), t=5, strides=2, n=2)
    x = _inverted_residual_block(x, 256, (3, 3), t=5, strides=1, n=1)

    x = _conv_block(x, 1280, (1, 1), strides=(1, 1))
    x = GlobalAveragePooling2D()(x)
    x = Reshape((1, 1, 1280))(x)
    x = Conv2D(512, (1, 1), padding='same', kernel_regularizer=l2(5e-4))(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = Conv2D(128, (1, 1), padding='same', kernel_regularizer=l2(5e-4))(x)

    output = Reshape((128,), name='feat_out')(x)

    model = Model(inputs, output)

    return model
