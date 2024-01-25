import cv2
import streamlit as st
import time
import random
import numpy as np
from Solver import Solver
from PIL import Image

thread_art_solver = Solver()

def GenerateClicked():
	print("Pressed Generate")


with st.sidebar:
	uploaded_img = st.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg', 'PNG', 'JPG'], accept_multiple_files=False, key=None)
	if uploaded_img is not None:
		image = Image.open(uploaded_img)
		img_array = np.array(image)
		img_array = thread_art_solver.LoadImage(img_array)


		st.image(
			img_array,
			use_column_width=True,
		)
	else:
		st.image(
			np.zeros((100, 100)).astype("uint8"),
			use_column_width=True,
		)


	image_type = st.radio(
    "Image Type",
    ["Square", "Round"])

	st.button("Generate Thread Art", key=None,  on_click=GenerateClicked, use_container_width = True)






my_placeholder = st.empty()



while True:
	img = np.zeros((500, 500, 3)).astype("uint8")
	for i in range(3):
		img[:, :, i] = random.randint(0, 255)
	my_placeholder.image(img, use_column_width=True)
	time.sleep(0.5)