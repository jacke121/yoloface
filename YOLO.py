# *******************************************************************
#
# Author : Thanh Nguyen, 2018
# Email  : sthanhng@gmail.com
# Github : https://github.com/sthanhng
#
# Face detection using the YOLOv3 algorithm
#
# Description : YOLO.py
# Contains methods of YOLO
#
# *******************************************************************

import os
import colorsys
import numpy as np
import cv2

from query_pic import search_pic
from yolo.model import eval
from yolo.utils import letterbox_image

from keras import backend as K
from keras.models import load_model
from timeit import default_timer as timer
from PIL import ImageDraw, Image
import global_var_model as gl_var

class YOLO(object):
    def __init__(self, args):
        self.args = args
        self.model_path = args.model
        self.classes_path = args.classes
        self.anchors_path = args.anchors
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self._generate()
        self.model_image_size = args.img_size

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        print(class_names)
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def _generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith(
            '.h5'), 'Keras model or weights must be a .h5 file'

        # Load model, or construct model and load weights
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            # make sure model, anchors and classes match
            self.yolo_model.load_weights(self.model_path)
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                   num_anchors / len(self.yolo_model.output) * (
                           num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print(
            '[i] ==> {} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

        # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(102)
        np.random.shuffle(self.colors)
        np.random.seed(None)

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2,))
        boxes, scores, classes = eval(self.yolo_model.output, self.anchors,
                                           len(self.class_names),
                                           self.input_image_shape,
                                           score_threshold=self.args.score,
                                           iou_threshold=self.args.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        start_time = timer()

        if self.model_image_size != (None, None):
            assert self.model_image_size[
                       0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[
                       1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(
                reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        # print(image_data.shape)
        image_data /= 255.
        # Add batch dimension
        image_data = np.expand_dims(image_data, 0)

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })

        # print('[i] ==> Found {} face(s) for this image'.format(len(out_boxes)))
        thickness = (image.size[0] + image.size[1]) // 400

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            text = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

            # print(text, (left, top), (right, bottom))

            for thk in range(thickness):
                draw.rectangle(
                    [left + thk, top + thk, right - thk, bottom - thk],
                    outline=(51, 178, 255))
            del draw

        end_time = timer()
        print('[i] ==> Processing time: {:.2f}ms'.format((end_time -
                                                          start_time) * 1000))

        return image, out_boxes

    def close_session(self):
        self.sess.close()


def detect_img(yolo):
    while True:
        img = input('[i] ==> Input image filename: ')
        try:
            image = Image.open(img)
        except:
            print('[!] ==> Open Error! Try again!')
            continue
        else:
            res_image, _ = yolo.detect_image(image)
            res_image.show()

    yolo.close_session()

def savemat(image, x, y, w, h):  # 保存矩阵

    minY = max(y - 10, 0)
    maxY = min(y + h + 10, image.shape[0])
    minX = max(x - 20, 0)
    maxX = min(x + w + 20, image.shape[1])
    cropImg = image[int(minY): int(maxY), int(minX): int(maxX)]
    return cropImg

def detect_video(model, video_path=None, output=None):
    if video_path == 'stream':
        # vid = cv2.VideoCapture(0)
        vid = cv2.VideoCapture("rtsp://admin:sbdwl123@192.168.25.45:554/h264/ch1/main/av_stream")
    else:
        vid = cv2.VideoCapture(video_path)

    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")

    # The video format and fps
    # video_fourcc = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fourcc = cv2.VideoWriter_fourcc('M', 'G', 'P', 'G')
    video_fps = vid.get(cv2.CAP_PROP_FPS)

    # The size of the frames to write
    video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output != "" else False
    if isOutput:
        output_fn = 'output_video.avi'
        out = cv2.VideoWriter(os.path.join(output, output_fn), video_fourcc, video_fps, video_size)

    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    i=0
    ###################################
    while True:
        ret, frame = vid.read()
        if ret:
            image = Image.fromarray(frame)
            image, faces = model.detect_image(image)
            result = np.asarray(image)
            curr_time = timer()
            exec_time = curr_time - prev_time
            prev_time = curr_time
            accum_time = accum_time + exec_time
            curr_fps = curr_fps + 1
            if accum_time > 1:
                accum_time = accum_time - 1
                fps = curr_fps
                curr_fps = 0
            # Initialize the set of information we'll displaying on the frame
            info = [
                ('FPS', '{}'.format(fps)),
                ('Faces detected', '{}'.format(len(faces)))
            ]
            if len(faces)>0:
                faces=faces[0]
                cropImg = savemat(frame, faces[0], faces[1], faces[2], faces[3])
                if (cropImg.shape[0] > 0 and cropImg.shape[1] > 0):
                    cv2.imwrite('./sht_face/' + str(i) + '.jpg', cropImg)
                    res = search_pic(gl_var.camera_server_ip, dbName="sbd_db02", path='./sht_face/' + str(i) + '.jpg')
                    if res:
                        print(res)
                    i += 1
            cv2.rectangle(result, (5, 5), (120, 50), (0, 0, 0), cv2.FILLED)
            for (i, (txt, val)) in enumerate(info):
                text = '{}: {}'.format(txt, val)
                cv2.putText(result, text, (10, (i * 20) + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (10, 175, 0), 1)

            cv2.namedWindow("face", cv2.WINDOW_NORMAL)
            cv2.imshow("face", result)
            # if isOutput:
            #     out.write(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()

    # Close the session
    model.close_session()