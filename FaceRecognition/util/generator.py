"""Data process.
Data process and generation.
"""

import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split


def read_img(path):
    """读取图像
    此函数用于从文件夹中读取不同人的人脸图像。

    # 参数
        path: String, 人脸数据存放文件夹的路径.
    # 返回
        res: List, 不同人的人脸图像.
    """
    res = []

    for (root, dirs, files) in os.walk(path):
        if files:
            tmp = []
            files = np.random.choice(files, 4)
            for f in files:
                img = os.path.join(root, f)
                image = cv2.imread(img)
                image = cv2.resize(image, (64, 64),
                                   interpolation=cv2.INTER_CUBIC)
                image = np.array(image, dtype='float32')
                image /= 255.
                tmp.append(image)

            res.append(tmp)

    return res


def get_paris(path):
    """配对
    此函数用于为相同大的人和不同的人配对

    # 参数
        path: String, 数据路径
    # 返回
        sm1: List, 配对的第一个对象
        sm2: List, 配对的第二个对象
        y1: List, 配对标记 (相同: 0, 不同: 1).
    """
    sm1, sm2, df1, df2 = [], [], [], []
    res = read_img(path)

    persons = len(res)

    for i in range(persons):
        for j in range(i, persons):
            p1 = res[i]
            p2 = res[j]

            if i == j:
                for pi in p1:
                    for pj in p2:
                        sm1.append(pi)
                        sm2.append(pj)
            else:
                df1.append(p1[0])
                df2.append(p2[0])

    df1 = df1[:len(sm1)]
    df2 = df2[:len(sm2)]
    y1 = list(np.zeros(len(sm1)))
    y2 = list(np.ones(len(df1)))

    sm1.extend(df1)
    sm2.extend(df2)
    y1.extend(y2)

    return sm1, sm2, y1


def create_generator(x, y, batch):
    """创建数据生成器
    此函数是一个数据生成器

    # Arguments
        x: List, 输入数据
        y: List, 数据标签
        batch: Integer, 数据生成器的批次大小。
    # Returns
        [x1, x2]: List, 配对数据与批次大小
        yb: List, 数据标签
    """
    while True:
        index = np.random.choice(len(y), batch)
        x1, x2, yb = [], [], []
        for i in index:
            x1.append(x[i][0])
            x2.append(x[i][1])
            yb.append(y[i])
        x1 = np.array(x1)
        x2 = np.array(x2)

        yield [x1, x2], yb


def get_train_test(path):
    """获取训练集和测试集
    此函数用于分割训练和测试数据并将其打乱。

    # 参数
        path: String, 人脸数据存放路径
    # 返回
        X_train: List, 训练集
        X_test: List, 训练集标签
        y_train: List, 测试集
        y_test: List, 测试集标签
    """
    im1, im2, y = get_paris(path)
    im = list(zip(im1, im2))

    X_train, X_test, y_train, y_test = train_test_split(
        im, y, test_size=0.33)

    return X_train, X_test, y_train, y_test
