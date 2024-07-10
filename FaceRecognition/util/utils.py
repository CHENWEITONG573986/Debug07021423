# coding:utf8
import cv2
import numpy as np
from model.facenet import get_model
from keras.models import Model
from face_lib import align_dlib

# 关键点提取模型路径
PREDICTOR_PATH = './face_lib/shape_predictor_68_face_landmarks.dat'
# 使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = align_dlib.AlignDlib(PREDICTOR_PATH)


def get_feature_model():
    """Get face features extraction model.

    # Returns
        feat_model: Model, face features extraction model.
    """
    model = get_model((64, 64, 3))
    model.load_weights('model/weight.h5')

    feat_model = Model(inputs=model.get_layer('model_1').get_input_at(0),
                       outputs=model.get_layer('model_1').get_output_at(0))

    return feat_model


def process_image(img):
    """Resize, reduce and expand image.

    # Returns
        image: ndarray(64, 64, 3), processed image.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转为RGB图片
    face_align = detector.align(64, img_rgb)
    if face_align is None:
        image = cv2.resize(img, (64, 64),
                       interpolation=cv2.INTER_CUBIC)
    else:
        face_align = cv2.cvtColor(face_align, cv2.COLOR_RGB2BGR)  # 转为BGR图片
        image = cv2.resize(face_align, (64, 64),
                       interpolation=cv2.INTER_CUBIC)
    # image = cv2.resize(img, (64, 64),
    #                    interpolation=cv2.INTER_CUBIC)
    image = np.array(image, dtype='float32')
    image /= 255.
    image = np.expand_dims(image, axis=0)

    return image
