import streamlit as st

from pathlib import Path

from therapy_aid_tool.DAOs._create_db_squema import create_schema

from st_controll import (
    toddlers_names,
    plot_sessions_progress,
    DATABASE,
)


# ==================================================
# Try to create database and squema if this is the first page openned
create_schema(DATABASE)

# ==================================================
# Page configs
TITLE = "Evaluate Toddler's Progress"

st.set_page_config(
    page_title=TITLE,
    layout="centered",
    page_icon="📈")

st.title(TITLE)
st.markdown(
    "#### Choose a Toddler to see their progress in the sessions")
st.markdown("---")

# ==================================================
# Quick check for empty database
if not toddlers_names():
    st.info("Please, add a therapy session to the database first! :)")
    st.stop()

# ==================================================
# SelectBox ::: Choose the toddler
st.markdown("##### Choose the toddler")
toddler_name = st.selectbox("", toddlers_names())

# ==================================================
# Images ::: Plot Sessions Progress
plot_sessions_progress(toddler_name)
