import cv2
import streamlit as st
import time
import random
import numpy as np
from Solver import Solver
from PIL import Image

thread_art_solver = Solver()


img_array = None

def GenerateClicked():
	GenerateArt()


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

	st.button("Generate Thread Art", key = None,  on_click = GenerateClicked, use_container_width = True)






my_placeholder = st.empty()


def GenerateArt():
	global img_array, thread_art_solver
	if img_array is not None:
		img = thread_art_solver.CreateThreadArt(img_array)
		my_placeholder.image(img, use_column_width=True)