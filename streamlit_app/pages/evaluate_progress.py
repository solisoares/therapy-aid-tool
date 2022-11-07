import streamlit as st

from streamlit_app.st_controll import (
    toddlers_names,
    plot_sessions_progress
)

# ==================================================
# Page configs
TITLE = "Evaluate Toddler's Progress"

st.set_page_config(
    page_title=TITLE,
    layout="centered")

st.title(TITLE)
st.markdown(
    "#### Choose a Toddler to see their progress in the sessions")
st.markdown("---")

# ==================================================
# SelectBox ::: Choose the toddler
st.markdown("##### Choose the toddler")
toddler_name = st.selectbox("", toddlers_names())

# ==================================================
# Images ::: Plot Sessions Progress
plot_sessions_progress(toddler_name)