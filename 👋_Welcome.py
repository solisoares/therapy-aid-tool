# This is the entrypoint for Streamlit
# Run with `streamlit run 👋_Welcome.py`
import streamlit as st

from pathlib import Path

from therapy_aid_tool.DAOs._create_db_squema import create_schema

ROOT = Path(__file__).parent
DATABASE = ROOT/"database"/"sessions.db"

# Page configs
st.set_page_config(
    page_title="Welcome!",
    layout="centered",
    page_icon="👋")

st.title("A Tool to aid in ASD therapy sessions!")

st.markdown("""
##### What is Autism?
Autism Spectrum Disorder (ASD) is a complex developmental disorder affecting \
people of all ages, their families and the society, limiting their social and \
cognitive skills.


##### Treatment
Autism is not a disease, there is no need for a cure. What was thought as a \
disease is now interpreted as a different way of thinking, feeling and living.
We shouldn't force people to "properly" function, but we can and should assist  \
in their achievement of gols and acceptance.

The number of children diagnosed is rising worldwide everyday, making early \
treatment a key to social development.
""")

st.markdown("""
---
##### The problem with manually extraction of data

There are many types of accompaniment and treatment, physical, nutritional and medical, \
but observational techniques (therapy sessions) are often used to measure success. \
That's where the therapist can watch the progress closely, take notes and intervene.

These therapy sessions generate qualitative and quantitative data that a a lot \
of times go unnoticed. Data that come from questions like:
* Did the patient respond to a certain stimulus?	
* How many responses happened?
* Did they engage in person to person interaction?
* Did they progress?

A possible and simple solution is to just video record these sessions and manually \
extract data from them. But this lacks standardization for a concise and structured \
record. That's because there are many different ways that ASD professionals take \
notes about a patient's progress and where they store this information.
""")

st.markdown("""
---
##### How our app can help in treatment?

With the use of Artificial Inteligence and Computer Vision our app is capable of:

* Handle large amounts of therapy session videos, storing and retrieving them as needed.
* Filter relevant scenes according to ASD professionals. 
    * Point exactly in time where is happening an event of interest in the video.
    * Reduce time for analysis of a whole video.
* Assistance in clinical and therapeutic decisions throughout interactive search and statistical reports.
    * Summary of interactions in each session.
    * Progress of interactions for all sessions.
""")

create_schema(DATABASE)