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

[data-testid="stToolbar"] { display: none; }
.stAppDeployButton { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

if "job_payload" not in st.session_state:
    st.session_state.job_payload = {}

# -------------------------------
# USERS  (replace with DB later)
# -------------------------------

USERS = {
    "admin":  "admin123",
    "dba":    "dba123",
    "viewer": "view123",
}

# -------------------------------
# LOGIN PAGE
# -------------------------------

def login():

    _, col, _ = st.columns([1, 1, 1])

    with col:

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🔐 EBS Clone POC")
        st.markdown("---")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign in", type="primary", use_container_width=True):

            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

# -------------------------------
# HOME
# -------------------------------

def home():

    st.title("Cloning POC Dashboard")

    schedule_col, = st.columns([1])

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
                else:
                    st.error("Job Submission Failed")

            except Exception as e:
                st.error(f"Connection Error: {e}")

# -------------------------------
# PAGE ROUTING
# -------------------------------

if not st.session_state.logged_in:
    login()
    st.stop()

# Logout button (top right via sidebar or inline)
with st.sidebar:
    st.markdown(f"Signed in as **{st.session_state.username}**")
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.session_state.page      = "home"
        st.rerun()

if st.session_state.page == "home":
    home()

elif st.session_state.page == "job_wizard_1":
    job_wizard_1()

elif st.session_state.page == "job_wizard_2":
    job_wizard_2()