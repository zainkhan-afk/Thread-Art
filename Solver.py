import cv2
import random
import numpy as np

class Solver:
	def __init__(self, num_nails = 360, img_size = (800, 800)):
		self.img_size = img_size
		self.num_nails = num_nails
		self.nails_list = list(range(self.num_nails))

		# Calculations for Square images
		self.nails_per_side = self.num_nails // 4
		self.dist_between_nails = self.img_size[0] / self.nails_per_side
		self.solved = False
		self.halt = False

		'''
		0                  		
	  N ------------------------- N/4
		|						|
		|						|
		|						|
    3N/4|_______________________| N/2
		                 
		'''

	def GetImgMSE(self, input_image, constructed_image):
		return ((input_image - constructed_image)**2 ).sum() / (input_image.shape[0]*input_image.shape[1])
	
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


	def GetOptimalLine(self, start_nail, in_img, img_out):
		X1, Y1 = self.GetNailPos(start_nail)
		nails_explored = []

		min_error = 1000000
		min_error_nail = None
		min_error_image = None

		while len(nails_explored) < self.num_nails - 2:
			chosen_nail = None
			while True:
				chosen_nail = random.sample(self.nails_list, 1)[0]
				nails_explored.append(chosen_nail)
				if self.ValidNail(start_nail, chosen_nail):
					break

			X2, Y2 = self.GetNailPos(chosen_nail)
			

			temp = img_out.copy()
			temp = cv2.line(temp, (X1, Y1), (X2, Y2), 0, 1)

			MSE = self.GetImgMSE(in_img, temp)

			if MSE < min_error:
				min_error = MSE
				min_error_nail = chosen_nail
				min_error_image = temp.copy()

		return min_error_image, min_error_nail

	
	def Solve(self, img, mode, frames_list):
		self.solved = False
		thread_trail = [random.randint(0, self.num_nails - 1)]
		out_image = 255 * np.ones(img.shape).astype("uint8")
		frames_list.append(out_image.copy())
		while not self.halt:
			print(f"Lines Completed: {len(thread_trail)}")
			current_nail = thread_trail[-1]
			out_image, chosen_nail = self.GetOptimalLine(current_nail, img, out_image)

			thread_trail.append(chosen_nail)
			frames_list.append(out_image.copy())


			if len(thread_trail) > 500:
				self.halt = True

		self.solved = True






if __name__ == "__main__":
	dum_img = np.zeros((800, 800)).astype("uint8")
	dum_img = cv2.imread("star.jpg", 0)
	solver = Solver(num_nails = 360, img_size = (800, 800))
	out, frames_list = solver.Solve(dum_img, "Square")

	cv2.imwrite("out.jpg", out)

	for frame in frames_list:
		cv2.imshow("out", out)
		cv2.imshow("frame", frame)
		cv2.waitKey(30)