import os

import cv2
import numpy as np

model_path = '/Users/bo/my/git/openpose/models'


class GeneralPoseModel(object):
    mode = ''

    def __init__(self, mode="BODY25"):
        # 指定采用的模型
        #   Body25: 25 points
        #   COCO:   18 points
        #   MPI:    15 points
        self.mode = mode
        self.inWidth = 240
        self.inHeight = 240
        self.threshold = 0.1
        if self.mode == "BODY25":
            self.points_name = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, "LShoulder": 5,
                                "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9, "RAnkle": 10, "LHip": 11, "LKnee": 12,
                                "LAnkle": 13, "Chest": 14, "Background": 15}
            self.num_points = 15
            self.point_pairs = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9],
                                [9, 10], [14, 11], [11, 12], [12, 13]]
            proto_txt = os.path.join(model_path, "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt")
            caffe_model = os.path.join(model_path, "pose/mpi/pose_iter_160000.caffemodel")
            self.pose_net = cv2.dnn.readNetFromCaffe(proto_txt, caffe_model)
        elif self.mode == "COCO":
            self.points_name = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, "LShoulder": 5,
                                "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9, "RAnkle": 10, "LHip": 11, "LKnee": 12,
                                "LAnkle": 13, "REye": 14, "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}
            self.num_points = 18
            self.point_pairs = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10],
                                [1, 11], [11, 12], [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]
            proto_txt = os.path.join(model_path, "pose/coco/pose_deploy_linevec.prototxt")
            caffe_model = os.path.join(model_path, "pose/coco/pose_iter_440000.caffemodel")
            self.pose_net = cv2.dnn.readNetFromCaffe(proto_txt, caffe_model)
        elif self.mode == "MPI":
            self.points_name = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, "LShoulder": 5,
                                "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9, "RAnkle": 10, "LHip": 11, "LKnee": 12,
                                "LAnkle": 13, "Chest": 14, "Background": 15}
            self.num_points = 15
            self.point_pairs = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9],
                                [9, 10], [14, 11], [11, 12], [12, 13]]
            proto_txt = os.path.join(model_path, "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt")
            caffe_model = os.path.join(model_path, "pose/mpi/pose_iter_160000.caffemodel")
            self.pose_net = cv2.dnn.readNetFromCaffe(proto_txt, caffe_model)

    def predict(self, frame):
        img_height, img_width, _ = frame.shape
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (self.inWidth, self.inHeight), (0, 0, 0), swapRB=False,
                                        crop=False)
        self.pose_net.setInput(inpBlob)
        self.pose_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.pose_net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

        output = self.pose_net.forward()

        H = output.shape[2]
        W = output.shape[3]
        print(output.shape)

        #
        points = []
        for idx in range(self.num_points):
            probMap = output[0, idx, :, :]  # confidence map.
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            # Scale the point to fit on the original image
            x = (img_width * point[0]) / W
            y = (img_height * point[1]) / H
            if prob > self.threshold:
                points.append((int(x), int(y)))
            else:
                points.append(None)

        return points

    def put_line(self, frame, points):
        frame_copy = np.copy(frame)
        for pair in self.point_pairs:
            partA = pair[0]
            partB = pair[1]

            if points[partA] and points[partB]:
                cv2.line(frame_copy,
                         points[partA],
                         points[partB],
                         (0, 255, 255), 3)
                cv2.circle(frame_copy,
                           points[partA],
                           8,
                           (0, 0, 255),
                           thickness=-1,
                           lineType=cv2.FILLED)
        return frame_copy


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # 摄像头
    model = GeneralPoseModel(mode='BODY25')
    while cv2.waitKey(1) & 0xFF != ord('q'):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, 1)
        # display the resulting frame
        res_points = model.predict(gray)
        gray = model.put_line(gray, res_points)
        cv2.imshow('frame', gray)
    # when everything done , release the capture
    cap.release()
    cv2.destroyAllWindows()
