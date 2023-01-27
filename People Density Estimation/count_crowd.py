
from pyimagesearch import configuration as config
from pyimagesearch.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import imutils
import cv2
import os


labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])
print("[INFO] loading YOLO from disk...")


net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


if config.USE_GPU:
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#extract layers outputs
# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)
writer = None


while True:
	(grabbed, frame) = vs.read()


	if not grabbed:
		break


	frame = imutils.resize(frame, width=700)
	results = detect_people(frame, net, ln,
		personIdx=LABELS.index("person"))



	for (i, (prob, bbox, centroid)) in enumerate(results):

		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		cv2.circle(frame, (cX, cY), 5, color, 1)


	text = "Crowd Count: {}".format(len(results))
	cv2.putText(frame, text, (10, frame.shape[0] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 0, 0), 3)


	if True:
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

