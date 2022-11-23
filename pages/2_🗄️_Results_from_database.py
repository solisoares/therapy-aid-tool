from copy import deepcopy
from pathlib import Path
import streamlit as st

import numpy as np
import matplotlib.pyplot as plt

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    get_session,
    toddlers_names,
    dates_from_name,
    dates_from_name,
    DATABASE,
)


# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Results from Database"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="🗄️")

st.title(TITLE)
st.markdown(
    "#### Choose a recorded session in the database \
     and generate interactive and statistical results")
st.markdown("---")

# ==================================================
# Quick check for empty database
if not toddlers_names():
    st.info("Please, add a therapy session to the database first! :)")
    st.stop()

# ==================================================
# Choose session based on toddler and Date
st.markdown("##### Session information")
col1, col2 = st.columns(2)
toddler_name = col1.selectbox("Toddler", toddlers_names())
date = col2.selectbox("Date", dates_from_name(toddler_name))

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
video = get_session(toddler_name, date).video
st.video(video.filepath)

# ==================================================
# Choose what type of closeness to plot
td_ct = np.array(video.closeness['td_ct'])
td_pm = np.array(video.closeness['td_pm'])
ct_pm = np.array(video.closeness['ct_pm'])

y_closeness = td_ct  # default
title = "Toddler-Caretaker"
if button_td_ct:
    y_closeness = td_ct
    title = "Toddler-Caretaker"

elif button_td_pm:
    y_closeness = td_pm
    title = "Toddler-Plusme"

elif button_ct_pm:
    y_closeness = ct_pm
    title = "Caretaker-Plusme"

# ==================================================
# Image ::: Plot Closeness and Interaction bar
# (8,1) is the perfect size to match streamlit video dimensions on the centered layout
CLOSENESS_THRESHOLD = 0.6
x = np.arange(len(y_closeness))
fig, ax = plt.subplots(figsize=(8, 1))
ax.stackplot(x, y_closeness, alpha=0.8, color='lightsteelblue')
# TODO: use interactions to fill_between instead of thresholding the closeness
ax.fill_between(x, y_closeness, alpha=0.5, color='red',
                where=y_closeness > CLOSENESS_THRESHOLD)
ax.set_ylim(top=1)
ax.set_xlim(left=0, right=len(y_closeness))
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
