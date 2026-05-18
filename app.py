import streamlit as st
import json
import time
import requests

st.set_page_config(
    layout="wide",
    page_title="Home",
    initial_sidebar_state="collapsed"
)

#GLOBAL CSS
st.markdown("""
<style>

/* Hide top-right toolbar */
[data-testid="stToolbar"] {
    display: none;
}

/* Hide Deploy button */
.stAppDeployButton {
    display: none;
}

/* Hide hamburger menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# SESSION STATE INIT

if "page" not in st.session_state:
    st.session_state.page = "home"

if "job_payload" not in st.session_state:
    st.session_state.job_payload = {}

#HOME
def home():

    st.title("Cloning POC Dashboard")
    sch_job_col, = st.columns(
        [1],
        border=True,
        vertical_alignment="center"
    )

    list_job_col, = st.columns(
        [1],
        border=True,
        vertical_alignment="center"
    )

    with sch_job_col:
        if st.button("Schedule a Job"):
            st.session_state.page = "job_wizard_1"
            st.rerun()
    
    with list_job_col:
        st.subheader("Running/Pending/Scheduled Job List:")

def job_wizard_1():
    st.title("Job Wizard - Set Target")
    select_target_instance = st.selectbox(
        "Select Target Instance",
        [
            "EBSDEVDB01",
            "EBSTESTAPP01",
            "EBSPRODDB01",
            "VISDB01",
            "VISAPP01",
            "FINDB01",
            "FINAPP01",
            "ERPDB01",
            "ERPAPP01",
        ]
    )
    st.session_state.target_instance=select_target_instance

    #FOOTER BUTTONS
    back_button,next_button = st.columns([1,1])

    with back_button:
        if st.button("Back"):
            st.session_state.page = "home"
            st.rerun()
    
    with next_button:
        if st.button("Next"):
            st.session_state.page = "job_wizard_2"
            st.rerun()

def job_wizard_2():
    st.title("Job Wizard - Summary")

    #FOOTER BUTTONS
    back_button,next_button = st.columns([1,1])

    with back_button:
        if st.button("Back"):
            st.session_state.page = "job_wizard_1"
            st.rerun()
    
    with next_button:
        if st.button("Submit"):
            payload = {
                "job_name": "CLONE",
                "target_instance": st.session_state.target_instance
            }

            response = requests.post(
                "http://54.90.68.252:8000/submit_job",
                json=payload
            )

            if response.status_code == 200:
                st.success("Job Submitted Successfully!")

            else:
                st.error("Job Submission Failed")           

#SESSION STATE FLOW
if st.session_state.page == "home":
    home()

elif st.session_state.page == "job_wizard_1":
    job_wizard_1()

elif st.session_state.page == "job_wizard_2":
    job_wizard_2()