import cv2
import streamlit as st
import time
import random
import numpy as np
from Solver import Solver
from PIL import Image

if 'art_started' not in st.session_state:
	st.session_state['art_started'] = False

if 'thread_art_solver' not in st.session_state:
	st.session_state['thread_art_solver'] = Solver()

if 'input_image' not in st.session_state:
	st.session_state['input_image'] = None

thread_art_solver = st.session_state['thread_art_solver']

def GenerateArtClicked():
	st.session_state['art_started'] = True

	if st.session_state['input_image'] is not None:
		thread_art_solver.Solve(st.session_state['input_image'])
				

def StopArtClicked():
	st.session_state['art_started'] = False

def DrawSideBar():
	with st.sidebar:
		uploaded_img = st.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg', 'PNG', 'JPG'], accept_multiple_files=False, key=None)
		if uploaded_img is not None:
			image = Image.open(uploaded_img)
			image = np.array(image)
			st.session_state['input_image'] = thread_art_solver.LoadImage(image)


			st.image(
				st.session_state['input_image'],
				use_column_width=True,
			)
		else:
			st.image(
				np.zeros((100, 100)).astype("uint8"),
				use_column_width=True,
			)

			st.session_state['art_started'] = False



		image_type = st.radio(
	    "Image Type",
	    ["Square", "Round"])

		if not st.session_state['art_started']:
			st.button("Generate Thread Art", on_click = GenerateArtClicked, use_container_width = True)
		else:
			st.button("Stop", on_click = StopArtClicked, use_container_width = True)

def DrawDisplayImage():
	my_placeholder = st.empty()
	if st.session_state['art_started']:
		img = thread_art_solver.GetFrame()
		my_placeholder.image(img, use_column_width=True)


# def GenerateArt():
# 	if img_array is not None:
# 		print("img array is not None")
# 		out_img = thread_art_solver.CreateThreadArt(img_array)
# 		print(out_img)
# 		my_placeholder.image(out_img, use_column_width=True)
# 		print(my_placeholder)

DrawSideBar()
DrawDisplayImage()