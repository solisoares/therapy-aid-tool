import streamlit as st

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    existing_dataset,
    create_dataset_from_zip,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Import existing dataset"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📤")

st.title(TITLE)

# ==================================================
# Widget ::: Upload dataset
dataset = st.file_uploader(label="Dataset to be imported", type=["zip"])

# ==================================================
# Process "Choose" button press
if dataset:
    # Validate the values of the inputs
    dataset_exists, warning_msg = existing_dataset(dataset.name[:-4])
    if dataset_exists:
        st.warning(warning_msg)
    else:
        st.session_state.dataset = dataset.name[:-4]
        # If the input is valid, load dataset from ZIP file uploaded
        with st.spinner("It may take a while..."):
            create_dataset_from_zip(dataset)
            st.success("Dataset imported successfully!")