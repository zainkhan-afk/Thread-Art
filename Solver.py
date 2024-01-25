import numpy as np
import cv2

class Solver:
	def __init__(self, num_nails = 360, img_size = (800, 800)):
		self.img_size = img_size
		self.num_nails = num_nails
	
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
		# img = cv2.imread(path, 0)
		if len(img.shape) > 2:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
		img = self.SquarePad(img)
		img = self.Resize(img)

		return img

	def CreateThreadArt(self, path):
		img = self.LoadImage(path)


if __name__ == "__main__":
	solver = Solver()
	solver.LoadImage("star.jpg")