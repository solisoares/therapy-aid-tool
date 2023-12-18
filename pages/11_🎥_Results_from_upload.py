import streamlit as st

import numpy as np
import matplotlib.pyplot as plt

# TODO: avoid using any Model or DAO in the View
from therapy_aid_tool.models.toddler import Toddler
from therapy_aid_tool.models.video import VideoBuilder
from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    VIDEOS_DIR,
    model_names,
    default_model_index,
    save_user_file,
    video_fp_from_toddler_date,
    add_session,
    toddlers_names,
    DATABASE
)

# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Results from upload"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="🎥")

st.title(TITLE)
st.markdown(
    "#### Upload a video of an ASD therapy session \
     and generate interactive and statistical \
     results.")

# ==================================================
# Widget ::: Select custom or default weights
custom = st.toggle("Custom weights")

if custom:
    # ==================================================
    # Widget ::: Upload model
    user_model = st.selectbox(label="Model to be used", options=model_names(), index=default_model_index(), key="model")

# ==================================================
# Widget ::: Upload video
user_video = st.file_uploader(
    label="Video to be analyzed",
    accept_multiple_files=False,
    key=None,
    on_change=None)
st.markdown("---")

# ==================================================
# Widget ::: Button "Process video"
button_process = st.button(label="Process video")

# ==================================================
# Process video
if user_video:
    # ==================================================
    # On "Process video" button press
    if button_process:
        # If there is already a video processed, discards it
        if 'video' in st.session_state:
            st.session_state.pop('video')

        if not user_video:
            st.warning("Please upload a video to be analysed.")
        else:
            build_video = True
            # Validate the values of the variables
            if custom and len(model_names()) == 0:
                    st.warning("Please train or load a model to use custom weights.")
                    build_video = False

            # Saves video uploaded and builds it
            if build_video:
                save_user_file(user_video, "user_video.mp4")
                with st.spinner("It may take a while..."):
                    if custom and user_model:
                        video = VideoBuilder("user_video.mp4", user_model).build()
                    else:
                        video = VideoBuilder("user_video.mp4").build()
                    st.session_state['video'] = video

    # If there is a video processed, display its analysis information
    if 'video' in st.session_state:
        video = st.session_state['video']

        # ==================================================
        # Buttons ::: Choose type of interactions
        st.markdown("### What kind of interactions would you like to inspect?")
        # The output will be actually a bar of closeness with regions of interaction in red
        col1, col2, col3 = st.columns(3)
        button_td_ct = col1.button("Toddler-Caretaker")
        button_td_pm = col2.button("Toddler-Plusme")
        button_ct_pm = col3.button("Caretaker-Plusme")

        # ==================================================
        # Widget ::: Show Video
        st.video(user_video)

        # ==================================================
        # Choose what type of closeness to plot
        type = "td_ct"  # default
        title = "Toddler-Caretaker"
        if button_td_ct:
            type = "td_ct"
            title = "Toddler-Caretaker"

        elif button_td_pm:
            type = "td_pm"
            title = "Toddler-Plusme"

        elif button_ct_pm:
            type = "ct_pm"
            title = "Caretaker-Plusme"

        # ==================================================
        # Image ::: Plot Closeness and Interaction bar
        # (8,1) is the perfect size to match streamlit video dimensions on the centered layout
        CLOSENESS_THRESHOLD = 0.6
        x = np.arange(len(video.closeness[type]))
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.stackplot(x, video.closeness[type], alpha=0.8, color='lightsteelblue')
        ax.fill_between(x, video.closeness[type], alpha=0.5, color='red',
                        where=video.interactions[type])
        ax.set_ylim(top=1)
        ax.set_xlim(left=0, right=len(video.closeness[type]))
        ax.vlines(0, 0, 1)
        ax.vlines(len(x), 0, 1)
        ax.yaxis.set_ticks([])
        ax.xaxis.set_ticks([])
        ax.set_title(title, {'fontsize': 10})
        st.pyplot(fig)
        st.markdown("#")
        st.markdown("---")

        # ==================================================
        # Widget ::: Interactions Statistics
        st.markdown("### Interactions Statistics")
        st.dataframe(video.interactions_statistics, use_container_width=True)
        st.markdown("#")
        st.markdown("---")

        # ==================================================
        # Expanders ::: Forms ::: Add Session to database
        st.markdown("### Add Recorded Session to the database?")
        st.markdown("#### ")

        col_1, col_2 = st.columns(2)
        add_new = col_1.expander("Add with new toddler")
        add_existing = col_2.expander("Add with existing toddler")

        with add_new:
            with st.form(key="add_session_1"):
                toddler = Toddler(st.text_input("What is the toddler's name?"))
                date = str(st.date_input("What is this session date?", key="1"))
                if st.form_submit_button("submit") and all([toddler, date]):
                    video.filepath = video_fp_from_toddler_date(toddler, date)
                    save_user_file(user_video, VIDEOS_DIR/video.filepath)
                    add_session(toddler, video, date)

        with add_existing:
            with st.form(key="add_session_2"):
                toddler = Toddler(st.selectbox(
                    "What is the toddler's name?", toddlers_names()))
                date = str(st.date_input("What is this session date?", key="2"))
                if st.form_submit_button("submit") and all([toddler, date]):
                    video.filepath = video_fp_from_toddler_date(toddler, date)
                    save_user_file(user_video, VIDEOS_DIR/video.filepath)
                    add_session(toddler, video, date)

else:
    if 'video' in st.session_state:
        st.session_state.pop('video')