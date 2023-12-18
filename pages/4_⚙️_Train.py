import streamlit as st

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    dataset_names,
    default_dataset_index,
    verify_dataset_folder,
    existing_model,
    finetune_yolo,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Train"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="⚙️")

st.title(TITLE)
st.markdown(
    "#### Train the model to analyze therapy sessions and \
    obtain statistics on the performance of the trained \
    model.")

# ==================================================
# Widget ::: Dataset name
dataset_name = st.selectbox(label="Dataset to be used in training", options=dataset_names(), index=default_dataset_index(), key="dataset")

# ==================================================
# Widget ::: Project name
model_name = st.text_input("Name of this model (it must not contain spaces)", key="model")

# ==================================================
# Widget ::: Expander
with st.expander("Advanced settings"):
    # ==================================================
    # Widget ::: Number input
    image_size = st.number_input(label="Image size", value=256, min_value=1)
    # ==================================================
    # Widget ::: Number input
    num_epochs = st.number_input(label="Number of epochs", value=100, min_value=1)
    # ==================================================
    # Widget ::: Number input
    batch_size = st.number_input(label="Batch size", value=1, min_value=1)
    # ==================================================
    # Widget ::: Selectbox
    base_model_name = st.selectbox(label="Base model to fine-tune", options=("yolov5n","yolov5s","yolov5m","yolov5l","yolov5x"), index=2)+".pt"

# ==================================================
# Widget ::: Button
button_train = st.button(label = "Train")

# ==================================================
# Process "Train" button press
if button_train:
    # Validates input values
    valid_values = True
    if len(dataset_names()) == 0:
        valid_values = False
        st.warning("Please load a dataset to train your model.")
    elif ' ' in dataset_name:
        valid_values = False
        st.warning("Please input name for the dataset without spaces.")
    if model_name == "" or ' ' in model_name:
        valid_values = False
        st.warning("Please input a name for the model without spaces.") 

    # Validate dataset folder and model name
    success, warning_msg1 = verify_dataset_folder(dataset_name)
    existing, warning_msg2 = existing_model(model_name)
    if not success:
        valid_values = False
        st.warning(warning_msg1, icon="⚠️")
    elif existing:
        valid_values = False
        st.warning(warning_msg2, icon="⚠️")
        
    # If input values are valid, train model
    if valid_values:
        with st.spinner("Training..."):
            infobox = st.info("You can check the progress of your training in the terminal used to open Therapy Aid Tool.", icon='ℹ')
            success, warning_msg = finetune_yolo(dataset_name, model_name, image_size, num_epochs, batch_size, base_model_name)    
            infobox.empty()                    
            if success:
                st.success("Training completed successfully!")
            else:    
                st.warning(warning_msg, icon="⚠️")