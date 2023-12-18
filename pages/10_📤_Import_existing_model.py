import streamlit as st

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    existing_model,
    create_model_from_zip,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Import existing model"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📤")

st.title(TITLE)

# ==================================================
# Widget ::: Upload dataset
model = st.file_uploader(label="Model to be imported", type=["zip"])

# ==================================================
# Process "Choose" button press
if model:
    # Validate the values of the variables
    dataset_exists, warning_msg = existing_model(model.name[:-4])
    if dataset_exists:
        st.warning(warning_msg)
    else:
        st.session_state.model = model.name[:-4]
        # If values are valid, import model
        with st.spinner("It may take a while..."):
            create_model_from_zip(model)
            st.success("Model imported successfully!")