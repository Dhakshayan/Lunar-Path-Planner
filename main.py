import streamlit as st
from PIL import Image
import os
import time
import numpy as np
from image_processing.crater_detector import detect_craters_and_mountains
from path_planning.planner import a_star
from image_processing.utils import draw_path

st.set_page_config(layout="wide")
st.title("Lunar Rover Path Planner using Orbital Imagery and ML")

if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.current_pos = None
    st.session_state.destination = None
    st.session_state.grid = None
    st.session_state.last_path = []

st.sidebar.header("Upload Lunar Surface Image")
img_file = st.sidebar.file_uploader("Upload JPEG image of lunar surface", type=['jpg', 'jpeg'])

if img_file:
    img = Image.open(img_file).convert("RGB")
    img_np = np.array(img)

    st.image(img, caption="Uploaded Lunar Image", use_column_width=True)

    if st.session_state.grid is None:
        st.sidebar.write("Select Start and Destination Coordinates")
        sx = st.sidebar.number_input("Start X", min_value=0, max_value=img_np.shape[1]-1)
        sy = st.sidebar.number_input("Start Y", min_value=0, max_value=img_np.shape[0]-1)
        dx = st.sidebar.number_input("Destination X", min_value=0, max_value=img_np.shape[1]-1)
        dy = st.sidebar.number_input("Destination Y", min_value=0, max_value=img_np.shape[0]-1)

        if st.sidebar.button("Initialize and Compute First Path"):
            grid = detect_craters_and_mountains(img_np)
            path = a_star(grid, (int(sy), int(sx)), (int(dy), int(dx)))

            if path:
                st.session_state.grid = grid
                st.session_state.current_pos = path[0]
                st.session_state.destination = (int(dy), int(dx))
                st.session_state.last_path = path
                st.session_state.history.append((img_np.copy(), path))
                st.success("Initial path computed.")
            else:
                st.error("No path found. Please choose different coordinates.")

    elif st.sidebar.button("Upload New Satellite Image and Update Path"):
        grid = detect_craters_and_mountains(img_np)
        rover_index = min(1, len(st.session_state.last_path) - 1)
        new_pos = st.session_state.last_path[rover_index]

        st.session_state.current_pos = new_pos
        new_path = a_star(grid, new_pos, st.session_state.destination)

        if new_path:
            st.session_state.grid = grid
            st.session_state.last_path = new_path
            st.session_state.history.append((img_np.copy(), new_path))
            st.success("Path updated using new image.")
        else:
            st.error("Unable to find new path from current position.")

    if st.session_state.history:
        img_copy, path = st.session_state.history[-1]
        vis_img = draw_path(img_copy, path, st.session_state.current_pos, st.session_state.destination)
        st.image(vis_img, caption="Rover Path Visualization", use_column_width=True)
