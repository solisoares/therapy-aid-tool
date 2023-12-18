import streamlit as st
from pathlib import Path

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    DATABASE,
)

PATH_TUT_IMGS = Path(__file__).parents[1] / "tutorial_images"

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Analyze therapy session"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="🎥")

st.title(TITLE)
st.markdown(
    """
    This module provides an easy way to analyze your videos of therapy sessions and keep track of toddlers' \
    progress. Learn more about how to use it in the following subsections.
    """)

st.markdown(
    """
    #### Importing an existing model

    To import an existing model, exported from the app, simply drag and drop the ZIP file of the model and \
    you are ready to go on with the analysis of your therapy sessions.
    """)

st.image((str)(PATH_TUT_IMGS / "60.png"))

st.markdown(
    """
    #### Results from upload

    In this section of the app you can analyze your videos of therapy sessions. To do so, first choose the model \
    you want to use for the task. You can use a default model or one of your own by using the switch button on the \
    top of the page.

    After that, drag and drop your video in the indicated region and click on "Process video". Then, wait for the \
    analysis to be performed.
    """)

st.image((str)(PATH_TUT_IMGS / "65.png"))

st.markdown(
    """
    When the analysis is completed, some information about it will be available. First, the video with a bar indicating \
    its regions of interest (i.e. the regions in which there are potentially interactions between two of the characters). \
    The regions in red indicate high probability of interaction.

    Additionally, you can choose the type of interaction you want to analyze, by clicking in one of the buttons above the \
    video, "Toddler-Caretaker", "Toddler-Plusme" or "Caretaker-Plusme".
    """)

st.image((str)(PATH_TUT_IMGS / "70.png"))

st.markdown(
    """
    Next to it, some statistics about the interactions in the video are displayed. "td_ct" indicates interactions between \
    toddler and caretaker, "td_pm" between toddler and PlusMe, and "ct_pm" between caretaker and PlusMe.

    The statistics are the total number of interactions, the total time interacting during a session, minimum and maximum \
    durations of a single interaction, and the mean duration of the interactions.
    """)

st.image((str)(PATH_TUT_IMGS / "75.png"))

st.markdown(
    """
    Lastly, you can save the session analysis to have access to toddlers' progress, in the "Evaluate progress" section, \
    and return to a session already analyzed in the future, in the "Results from database" section.
    """)

st.markdown(
    """
    #### Evaluate progress

    In this section, you can check the toddlers' progress in terms of statistics collected during video analysis. Here, \
    three graphs are displayed, one for each type of interaction, as in the image below.
    """)

st.image((str)(PATH_TUT_IMGS / "80.png"))

st.markdown(
    """
    #### Results from database

    In this section, an already analyzed video of a therapy session can be accessed. The information displayed here is \
    the same as that available in the "Results from upload" section. 
    """)