import streamlit as st
import pandas as pd

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema
from therapy_aid_tool.models.yolo_finetuning import MODELS_DIR

from st_controll import (
    model_names,
    default_model_index,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Model's overall performance"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📊")

st.title(TITLE)
st.markdown(
    '#### Statistics about training process for a model. See "Train your model" section for further information.')

# ==================================================
# Widget ::: Model name
model_name = st.selectbox(label="Model to be analyzed", options=model_names(), index=default_model_index(), key="model")

# ==================================================
# Widgets ::: Plot images
if len(model_names()) > 0:
    image_labels = ["Confusion matrix",
                    "Precision-Confidence curve",
                    "Recall-Confidence curve",
                    "F1 Score-Confidence curve",
                    "Precision-Recall curve",
                    "Training summary"
                    ]

    image_paths = [ MODELS_DIR / model_name / "confusion_matrix.png",
                    MODELS_DIR / model_name / "P_curve.png",
                    MODELS_DIR / model_name / "R_curve.png",
                    MODELS_DIR / model_name / "F1_curve.png",
                    MODELS_DIR / model_name / "PR_curve.png",
                    MODELS_DIR / model_name / "results.png"
                ]

    available = 0
    for image in image_paths:
        if image.exists():
            available += 1
    if available == 0:
        st.warning("There are no graphs available for this model.")
    elif available < len(image_paths):
        st.warning("Some graphs are not available for this model.")

    for i in range(len(image_paths)):
        if image_paths[i].exists():
            st.markdown("### "+image_labels[i])
            st.image(image=(str)(image_paths[i]))
            if i == len(image_paths)-1:
                # Displays the metrics for the best and the last models generated
                container = st.container()
                columns_container = container.columns(2)
                columns_container[0].markdown("#### Best model")
                columns_container[0].dataframe(pd.read_csv(MODELS_DIR / model_name / "best_metrics.csv"), column_config={1: "Metric", 2: "Value"})
                columns_container[1].markdown("#### Last model")
                columns_container[1].dataframe(pd.read_csv(MODELS_DIR / model_name / "last_metrics.csv"), column_config={1: "Metric", 2: "Value"})