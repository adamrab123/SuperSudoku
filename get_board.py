import cv2         
import numpy as np
from os import listdir

def extract_board(im):
	im_thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
		cv2.THRESH_BINARY, 11, 4)
	cv2.imwrite("thres.jpg", im_thresh)
	contours = cv2.findContours(im_thresh, cv2.CV_RETR_LIST, \
		cv2.CHAIN_APPROX_SIMPLE)



im = cv2.imread("source.jpeg", 0)
assert(im is not None)
extract_board(im)