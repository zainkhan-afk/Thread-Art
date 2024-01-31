import cv2
import random
import numpy as np

class Solver:
	def __init__(self, num_nails = 360, img_size = (800, 800)):
		self.img_size = img_size
		self.num_nails = num_nails
		self.thread_trail = []
		self.nails_list = list(range(self.num_nails))

		# Calculations for Square images
		self.nails_per_side = self.num_nails // 4
		self.dist_between_nails = self.img_size[0] / self.nails_per_side

		'''
		0                  		
	  N ------------------------- N/4
		|						|
		|						|
		|						|
    3N/4|_______________________| N/2
		                 
		'''
	def ValidNail(self, nail1, nail2):
		side1 = nail1//self.nails_per_side
		side2 = nail2//self.nails_per_side

		if side1 ==  side2:
			return False
		return True

	def GetNailPos(self, nail):
		side = nail//self.nails_per_side
		rem = nail % self.nails_per_side

		if side == 0:
			X = rem / self.nails_per_side * self.img_size[0]
			Y = 0

		if side == 1:
			X = self.img_size[0]
			Y = rem / self.nails_per_side * self.img_size[1]

		if side == 2:
			X = (1 - (rem / self.nails_per_side)) * self.img_size[0]
			Y = self.img_size[1]

		if side == 3:
			X = 0
			Y = (1 - (rem / self.nails_per_side)) * self.img_size[1]

		return int(X), int(Y)


	def GetOptimalLine(self, start_nail, in_img, temp_out):
		X1, Y1 = self.GetNailPos(start_nail)

		chosen_nail = None
		while True:
			chosen_nail = random.sample(self.nails_list, 1)[0]
			if self.ValidNail(start_nail, chosen_nail):
				break

		X2, Y2 = self.GetNailPos(chosen_nail)

		temp_out = cv2.line(temp_out, (X1, Y1), (X2, Y2), 0, 1)

		return temp_out, chosen_nail

	
	def Solve(self, img, mode):
		self.thread_trail.append(random.randint(0, self.num_nails - 1))
		out_image = 255 * np.ones(img.shape).astype("uint8")
		frames_list = [out_image.copy()]
		while True:
			current_nail = self.thread_trail[-1]
			out_image, chosen_nail = self.GetOptimalLine(current_nail, img, out_image)

			self.thread_trail.append(chosen_nail)
			frames_list.append(out_image.copy())


			if len(self.thread_trail) > 100:
				break

		return out_image, frames_list





if __name__ == "__main__":
	dum_img = np.zeros((800, 800)).astype("uint8")
	solver = Solver(num_nails = 360, img_size = (800, 800))
	out, frames_list = solver.Solve(dum_img, "Square")

	for frame in frames_list:
		cv2.imshow("out", out)
		cv2.imshow("frame", frame)
		cv2.waitKey(30)