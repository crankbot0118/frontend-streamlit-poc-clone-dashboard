import streamlit as st
import requests

st.set_page_config(
    layout="wide",
    page_title="Home",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# GLOBAL CSS
# -------------------------------

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

/* Card Hover */
.job-card:hover {
    border: 1px solid #3b82f6 !important;
    transform: scale(1.01);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE INIT
# -------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "job_payload" not in st.session_state:
    st.session_state.job_payload = {}

# -------------------------------
# HOME
# -------------------------------

def home():

    st.title("Cloning POC Dashboard")

    schedule_col,=st.columns([1])

    with schedule_col:

        if st.button("Schedule a Job"):

            st.session_state.page = "job_wizard_1"
            st.rerun()

    st.divider()

    st.subheader("Running / Pending / Scheduled Jobs")

# -------------------------------
# JOB WIZARD STEP 1
# -------------------------------

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

    st.session_state.target_instance = select_target_instance

    back_button, next_button = st.columns([1, 1])

    with back_button:

        if st.button("Back"):

            st.session_state.page = "home"
            st.rerun()

    with next_button:

        if st.button("Next"):

            st.session_state.page = "job_wizard_2"
            st.rerun()

# -------------------------------
# JOB WIZARD STEP 2
# -------------------------------

def job_wizard_2():

    st.title("Job Wizard - Summary")

    st.subheader("Selected Target")

    st.info(st.session_state.target_instance)

    back_button, next_button = st.columns([1, 1])

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

            try:

                response = requests.post(
                    "http://54.90.68.252:8000/submit_job",
                    json=payload
                )

                if response.status_code == 200:

                    st.success("Job Submitted Successfully!")
                    # st.session_state.page = "home"

                    # st.rerun()

                else:

                    st.error("Job Submission Failed")

            except Exception as e:

                st.error(f"Connection Error: {e}")

# -------------------------------
# PAGE ROUTING
# -------------------------------

if st.session_state.page == "home":
    home()

elif st.session_state.page == "job_wizard_1":
    job_wizard_1()

elif st.session_state.page == "job_wizard_2":
    job_wizard_2()