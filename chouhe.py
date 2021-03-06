import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy.misc import imread
import tensorflow as tf

from FlowNet2_src import FlowNet2, LONG_SCHEDULE
from FlowNet2_src import flow_to_image
def process_img(frame_1, frame_2):
    # Feed forward
    im1 = frame_1/255.
    im2 = frame_2/255.
    print('im1', im1.shape)
    im1 = np.array([im1]).astype(np.float32)
    print('npim1',im1.shape)
    #im1 = np.stack([im1,im1,im1], axis=-1)
    print('stim1',im1.shape)
    im2 = np.array([im2]).astype(np.float32)
    #im2 = np.stack([im2,im2,im2], axis=-1)
    return im1,im2

if __name__ == '__main__':
    filename = 'zth_src'
    # 读取视频
    path = 'zth_src/test_4_6.avi'
    cap = cv2.VideoCapture(path)
    print('总帧数', cap.get(7))
    print('图像的尺寸为：', cap.get(3), cap.get(4))

    # 调用flownet
    # Graph construction
    im1_pl = tf.placeholder(tf.float32, [1, 576, 768, 3])  # 图像的维度
    im2_pl = tf.placeholder(tf.float32, [1, 576, 768, 3])
    flownet2 = FlowNet2()
    inputs = {'input_a': im1_pl, 'input_b': im2_pl}
    flow_dict = flownet2.model(inputs, LONG_SCHEDULE, trainable=False)
    pred_flow = flow_dict['flow']
    cpkt_file = 'FlowNet2_src/checkpoints/FlowNet2/flownet-2.ckpt-0'
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, cpkt_file)
        while (1):
            res, frame_1 = cap.read()
            cv2.imshow('image', frame_1)
            res_2, frame_2 = cap.read()
            #print('frame', frame_1.shape)
            im1, im2 = process_img(frame_1, frame_2)
            feed_dict = {im1_pl: im1, im2_pl: im2}
            pred_flow_val = sess.run(pred_flow, feed_dict=feed_dict)
            flow_im = flow_to_image(pred_flow_val[0])
            cv2.imshow('flowImage', flow_im)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


