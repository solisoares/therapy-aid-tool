from therapy_aid_tool.models.video import VideoBuilder

from copy import deepcopy

import streamlit as st
import json

import numpy as np
import matplotlib.pyplot as plt

# Page configs
TITLE = "Interactive Event Detection"

st.set_page_config(
    page_title=TITLE,
    layout="centered")

st.title(TITLE)
st.subheader(
    "Upload a video of an ASD therapy session \
     and generate interactive and statistical \
     results.")

# st.write(st.session_state)
# Upload video
user_video = st.file_uploader(
    label="",
    accept_multiple_files=False,
    key=None,
    on_change=None)

if user_video:
    # Download user video
    with open("user_video.mp4", "wb") as f:
        f.write(user_video.read())

    # Run detection the first time only
    if 'video' not in st.session_state:
        with st.spinner("It may take a while..."):
            # parser = VideoParser("user_video.mp4")
            # closeness = parser.closeness()
            # st.session_state['closeness'] = closeness
            # st.session_state['parser'] = parser
            # WIP
            video = VideoBuilder("user_video.mp4").build()
            st.session_state['video'] = video

    else:
        # closeness = st.session_state['closeness']
        # parser = st.session_state['parser']
        # WIP
        video = st.session_state['video']

    # Buttons
    st.subheader("What kind of interactions would you like to inspect?")
    # The output will be actually a bar of closeness with regions of interaction in red
    col1, col2, col3 = st.columns(3)
    button_td_ct = col1.button("Toddler-Caretaker")
    button_td_pm = col2.button("Toddler-Plusme")
    button_ct_pm = col3.button("Caretaker-Plusme")

    # Show Video
    st.video(user_video)
    # td_ct = np.array(closeness['td_ct'])
    # td_pm = np.array(closeness['td_pm'])
    # ct_pm = np.array(closeness['ct_pm'])
    # WIP
    td_ct = np.array(video.closeness['td_ct'])
    td_pm = np.array(video.closeness['td_pm'])
    ct_pm = np.array(video.closeness['ct_pm'])

    # Choose what type of closeness to plot
    # TODO: put a title on the closeness bar
    y_closeness = td_ct  # default
    title = None
    if button_td_ct:
        y_closeness = td_ct
        title = "Toddler-Caretaker"

    elif button_td_pm:
        y_closeness = td_pm
        title = "Toddler-Plusme"

    elif button_ct_pm:
        y_closeness = ct_pm
        title = "Caretaker-Plusme"

    # Plot Closeness and Interaction bar
    # (8,1) is the perfect size to match streamlit video dimensions on the centered layout
    CLOSENESS_THRESHOLD = 0.6
    x = np.arange(len(y_closeness))
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.stackplot(x, y_closeness, alpha=0.8, color='lightsteelblue')
    ax.fill_between(x, y_closeness, alpha=0.5, color='red',
                    where=y_closeness > CLOSENESS_THRESHOLD)
    ax.set_ylim(top=1)
    ax.set_xlim(left=0, right=len(y_closeness))
    ax.vlines(0, 0, 1)
    ax.vlines(len(x), 0, 1)
    ax.yaxis.set_ticks([])
    ax.set_title(title, {'fontsize': 10})
    st.pyplot(fig)

    # Dataframe of Interactions Statistics
    # The interactions based on 0.6 threshold of closeness

    # interactions = deepcopy(closeness)
    # WIP
    interactions = deepcopy(video.closeness)
    for k, lst in interactions.items():
        for idx, value in enumerate(lst):
            interactions[k][idx] = value > CLOSENESS_THRESHOLD
    st.subheader("Interactions Statistics")
    # st.dataframe(parser.interactions_statistics(
    #     interactions), use_container_width=True)
    # WIP
    st.dataframe(video.interactions_statistics, use_container_width=True)

else:
    if 'video' in st.session_state:
        st.session_state.pop('video')
