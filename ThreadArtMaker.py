import cv2
import random
import numpy as np
from Solver import Solver
import threading

class ThreadArtMaker:
	def __init__(self, num_nails = 360, img_size = (800, 800)):
		self.img_size = img_size
		self.num_nails = num_nails
		self.num_imgs_converted = 0
		self.input_image = None
		self.solver = Solver(num_nails = 360, img_size = (800, 800))
		self.frame_number = 0
		self.frames_list = []
		self.frames_exhausted = False
	
	def SquareCrop(self, img):
		H, W = img.shape

		if W != H:
			if W > H:
				diff = W - H
				img = img[:, diff//2 : diff//2 + H]

			if H > W:
				diff = H - W
				img = img[diff//2 : diff//2 + W, :]

		return img

	def SquarePad(self, img):
		H, W = img.shape

		padded_image = img.copy()
		if W != H:
			if W > H:
				diff = W - H
				padded_image = np.zeros((W, W)).astype("uint8")
				padded_image[diff//2 : diff//2 + H, :] = img


			if H > W:
				diff = H - W
				padded_image = np.zeros((H, H)).astype("uint8")
				img = img[diff//2 + W, :]
				padded_image[:, diff//2 : diff//2 + W] = img

		return padded_image

	def Resize(self, img):
		return cv2.resize(img, self.img_size)

	def LoadImage(self, img):
		if len(img.shape) > 2:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

		img = self.SquarePad(img)
		img = self.Resize(img)

		return img

	def Solve(self, img, mode):
		self.frames_list = []
		self.frame_number = 0
		self.frames_exhausted = False

		self.input_image = img
		
		proc = threading.Thread(target=self.solver.Solve, args=(img, mode, self.frames_list))
		proc.start()
		
		# self.out_image, self.frames_list = self.solver.Solve(img, mode)

		self.num_imgs_converted += 1

	def GetFrame(self):
		if len(self.frames_list) == 0:
			return 255*np.ones(self.img_size).astype("uint8")

		if not self.solver.solved:
			img = self.frames_list[self.frame_number]
			self.frame_number += 1
			if self.frame_number >= len(self.frames_list):
				self.frame_number = len(self.frames_list)-1
		else:
			img = self.frames_list[-1]


		return img


if __name__ == "__main__":
	solver = Solver()
	solver.LoadImage("star.jpg")