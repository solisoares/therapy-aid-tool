import streamlit as st

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    model_names,
    default_model_index,
    DATABASE,
    MODELS_DIR
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Label information"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📊")

st.title(TITLE)
st.markdown(
    '#### Statistics about labels used in training. See "Train your model" section for further information.')

# ==================================================
# Widget ::: Model name
model_name = st.selectbox(label="Model to be analyzed", options=model_names(), index=default_model_index(), key="model")

# ==================================================
# Widgets ::: Plot images
if len(model_names()) > 0:
    image_labels = ["Labels' summary",
                    "Labels' correlogram"
                    ]

    model_paths = [ MODELS_DIR / model_name / "labels.jpg",
                    MODELS_DIR / model_name / "labels_correlogram.jpg"
                ]

    available = 0
    for image in model_paths:
        if image.exists():
            available += 1
    if available == 0:
        st.warning("There are no graphs available for this model.")
    elif available < len(model_paths):
        st.warning("Some graphs are not available for this model.")

    for i in range(len(model_paths)):
        if model_paths[i].exists():
            st.markdown("### "+image_labels[i])
            st.image((str)(model_paths[i]))