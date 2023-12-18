import streamlit as st

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    existing_dataset,
    download_dataset_from_labelbox,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Download dataset from Labelbox"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📥")

st.title(TITLE)

# ==================================================
# Widget ::: Text input
ds_name = st.text_input(label="Dataset name")

# ==================================================
# Widget ::: Text input
labelbox_api = st.text_input(label="Labelbox API key")

# ==================================================
# Widget ::: Text input
project_id = st.text_input(label="Project ID")

# ==================================================
# Widget ::: Number input
train_perc = st.number_input(label="Percentage of the dataset destined to training", value=50, min_value=1)

# ==================================================
# Widget ::: Number input
valid_perc = st.number_input(label="Percentage of the dataset destined to validation", value=25, min_value=0)

# ==================================================
# Widget ::: Number input
test_perc = st.number_input(label="Percentage of the dataset destined to testing", value=25, min_value=0)

# ==================================================
# Widget ::: Button
button_download = st.button(label="Download")

# ==================================================
# Process "Choose" button press
if button_download:
    # Validate the values of the variables
    valid_values = True
    # ds_name
    if ds_name == "":
        valid_values = False
        st.warning("Please input the name of the dataset.")
    else:
        dataset_exists, warning_msg = existing_dataset(ds_name)
        if dataset_exists:
            valid_values = False
            st.warning(warning_msg)
    # labelbox_api
    if labelbox_api == "":
        valid_values = False
        st.warning("Please input the Labelbox API key. For a tutorial on how to get it, see 'Train your model' section.")
    # project_id
    if project_id == "":
        valid_values = False
        st.warning("Please input the Labelbox project ID. For a tutorial on how to get it, see 'Train your model' section.")
    # train_perc, valid_perc and test_perc
    if (train_perc+valid_perc+test_perc) != 100:
        valid_values = False
        st.warning("Invalid traininng, validation and testing percentages. The proportion between them must sum up to 100%.")

    # If all the input values are valid, download dataset
    if valid_values:
        st.session_state.dataset = ds_name
        with st.spinner("It may take a while..."):
            success, ds_path = download_dataset_from_labelbox(labelbox_api, project_id, train_perc, valid_perc, test_perc, ds_name)
            if success:
                st.success("Download completed successfully! You can access it at "+(str)(ds_path))