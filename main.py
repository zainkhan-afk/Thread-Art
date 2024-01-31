import cv2
import streamlit as st
import time
import random
import numpy as np
from ThreadArtMaker import ThreadArtMaker
from PIL import Image

if 'art_started' not in st.session_state:
	st.session_state['art_started'] = False

if 'out_type' not in st.session_state:
	st.session_state['out_type'] = None

if 'thread_art_maker' not in st.session_state:
	st.session_state['thread_art_maker'] = ThreadArtMaker()

if 'input_image' not in st.session_state:
	st.session_state['input_image'] = None

thread_art_maker = st.session_state['thread_art_maker']

def GenerateArtClicked():
	st.session_state['art_started'] = True

	if st.session_state['input_image'] is not None:
		thread_art_maker.Solve(st.session_state['input_image'], st.session_state['out_type'])
				

def StopArtClicked():
	st.session_state['art_started'] = False
	thread_art_maker.Stop()

def DrawSideBar():
	with st.sidebar:
		uploaded_img = st.file_uploader("Choose Image", type=['png', 'jpg', 'jpeg', 'PNG', 'JPG'], accept_multiple_files=False, key=None)
		if uploaded_img is not None:
			image = Image.open(uploaded_img)
			image = np.array(image)
			st.session_state['input_image'] = thread_art_maker.LoadImage(image)


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

		st.session_state['out_type'] = image_type

		if not st.session_state['art_started']:
			st.button("Generate Thread Art", on_click = GenerateArtClicked, use_container_width = True)
		else:
			st.button("Stop", on_click = StopArtClicked, use_container_width = True)

def DrawDisplayImage():
	my_placeholder = st.empty()
	if st.session_state['art_started']:
		while not thread_art_maker.frames_exhausted:
			img = thread_art_maker.GetFrame()
			my_placeholder.image(img, use_column_width=True)
			time.sleep(0.5)

		my_placeholder.image(thread_art_maker.out_image, use_column_width=True)
		st.session_state['art_started'] = False



# def GenerateArt():
# 	if img_array is not None:
# 		print("img array is not None")
# 		out_img = thread_art_maker.CreateThreadArt(img_array)
# 		print(out_img)
# 		my_placeholder.image(out_img, use_column_width=True)
# 		print(my_placeholder)

DrawSideBar()
DrawDisplayImage()