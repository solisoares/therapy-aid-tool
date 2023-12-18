import streamlit as st

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    model_names,
    default_model_index,
    create_zip_from_model,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Export model"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📥")

st.title(TITLE)

# ==================================================
# Widget ::: Model name
mdl_name = st.selectbox(label="Model to be exported", options=model_names(), index=default_model_index(), key="model")

# ==================================================
# Widget ::: Download button
button_download = st.button(label="Export")

# ==================================================
# Process "Choose" button press
if button_download:
    # Validate the values of the variables
    if len(model_names()) == 0:
        st.warning("Please train or load a model to export one.")
    
    # If all the values inputted are valid, get model
    if len(model_names()) > 0:
        with st.spinner("It may take a while..."):
            save_path = create_zip_from_model(mdl_name)
            st.success("Operation completed succesfully! You can access it in "+(str)(save_path))