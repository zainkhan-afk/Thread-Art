import cv2
import streamlit as st
import time
import random
import numpy as np

my_placeholder = st.empty()

while True:
	img = np.zeros((500, 500, 3)).astype("uint8")
	for i in range(3):
		img[:, :, i] = random.randint(0, 255)
	my_placeholder.image(img, use_column_width=True)
	time.sleep(0.5)