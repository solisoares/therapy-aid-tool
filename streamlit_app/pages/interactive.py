from therapy_aid_tool.interaction_detector import interaction_detector

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
    # TODO: prevent streamlit reruns of yolo on button click
    # TODO: Add loading bar
    # TODO: Process video and get interactions. Input: video | Output: interactions dict
    # Download user video
    with open("user_video.mp4", "wb") as f:
        f.write(user_video.read())

    # Run detection the first time only
    if 'interactions' not in st.session_state:
        with st.spinner("It may take a while..."):
            interactions = interaction_detector("user_video.mp4")
            st.session_state['interactions'] = interactions
    else:
        interactions = st.session_state['interactions']
    # Buttons
    st.subheader("What kind of interactions would you like to inspect?")
    col1, col2, col3, col4 = st.columns(4)
    button_td_ct = col1.button("Toddler touches Caretaker")
    button_td_pm = col2.button("Toddler touches Plusme")
    button_ct_pm = col3.button("Caretaker touches Plusme")
    button_ct_td = col4.button("Caretaker touches Toddler")

    # Show Video
    st.video(user_video)
    td_ct = np.array(interactions['td_ct'])
    td_pm = np.array(interactions['td_pm'])
    ct_pm = np.array(interactions['ct_pm'])

    # Choose what type of interaction to show
    # TODO: put a title on the interaction bar
    y = td_ct  # default
    if button_td_ct:
        y = td_ct

    elif button_td_pm:
        y = td_pm

    elif button_ct_pm:
        y = ct_pm

    elif button_ct_td:
        # TODO: Add interaction for Caretaker touching Toddler -> y = ct_td
        pass

    x = np.arange(len(y))

    # Plot closeness and interaction bar
    # (8,1) is the perfect size to match streamlit video dimensions on the centered layout
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.stackplot(x, y, alpha=0.8, color='lightsteelblue')
    ax.fill_between(x, y, alpha=0.5, color='red', where=y > 0.6)
    ax.set_ylim(top=1)
    ax.set_xlim(left=0, right=len(y))
    ax.vlines(0, 0, 1)
    ax.vlines(len(x), 0, 1)
    ax.yaxis.set_ticks([])

    st.pyplot(fig)
else:
    if 'interactions' in st.session_state:
        st.session_state.pop('interactions')
