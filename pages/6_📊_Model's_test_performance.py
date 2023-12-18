import streamlit as st

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema

def sub_img_index():
    if st.session_state.img_index > 1:
        st.session_state.img_index -= 1

def sum_img_index():
    if st.session_state.img_index < len(paths):
        st.session_state.img_index += 1

def reset_img_index():
    st.session_state.img_index = 1
    

from st_controll import (
    model_names,
    default_model_index,
    test_image_paths,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Model's test performance"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📊")

st.title(TITLE)
st.markdown(
    "#### Displays the performance of a trained model in the test dataset.")

if "img_index" not in st.session_state:
    st.session_state["img_index"] = 1

# ==================================================
# Widget ::: Model name
model_names = model_names()
model_index = default_model_index()
model_name = st.selectbox(label="Model to be analyzed", options=model_names, index=model_index, key="model")

# ==================================================
# Widget ::: Slider to the image to be displayed
if len(model_names) > 0:
    paths = test_image_paths(model_name)
    if len(paths) > 0:
        if st.session_state.img_index > len(paths): # Possible when model_name is changed
            reset_img_index()
        st.slider(label="Index of the test image", label_visibility="hidden", min_value=1, max_value=len(paths), key="img_index")

        # ==================================================
        # Widgets ::: Buttons to help in image selection
        nav_buttons = st.container()
        col_nav_buttons = nav_buttons.columns(20)
        back_button = col_nav_buttons[len(col_nav_buttons)-2].button(label="←", on_click=sub_img_index)
        forw_button = col_nav_buttons[len(col_nav_buttons)-1].button(label="→", on_click=sum_img_index)

        path_detected = (str)(paths[st.session_state.img_index-1])
        path_ground_truth = ((str)(paths[st.session_state.img_index-1])).replace("/detected/" ,"/ground_truth/")
        st.markdown("##### Detected")
        st.image(path_detected)
        st.markdown("##### Ground truth")
        st.image(path_ground_truth)
        
    else:
        st.warning("There are no test images available for this model.")