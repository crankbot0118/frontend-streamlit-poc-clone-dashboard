import streamlit as st
import requests

st.set_page_config(
    layout="wide",
    page_title="Home",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# HELPERS
# -------------------------------

def get_status_color(status):

    status = status.upper()

    if status == "RUNNING":
        return "#f39c12"

    elif status == "FAILED":
        return "#e74c3c"

    elif status == "COMPLETED":
        return "#27ae60"

    elif status == "PENDING":
        return "#3498db"

    return "#95a5a6"


def get_jobs():

    try:

        response = requests.get(
            "http://54.90.68.252:8000/rps_job_list"
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception as e:

        st.error(f"Backend Connection Failed: {e}")

        return []


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

    schedule_col, refresh_col = st.columns([1, 1])

    with schedule_col:

        if st.button("Schedule a Job"):

            st.session_state.page = "job_wizard_1"
            st.rerun()

    with refresh_col:

        if st.button("Refresh Jobs"):
            st.rerun()

    st.divider()

    st.subheader("Running / Pending / Scheduled Jobs")

    jobs = get_jobs()

    if not jobs:

        st.info("No jobs found")

        return

    for job in jobs:

        status_color = get_status_color(job["status"])

        st.markdown(
            f"""
            <div class="job-card"
                style="
                    border:1px solid #1f2937;
                    border-radius:14px;
                    padding:20px;
                    margin-bottom:15px;
                    background-color:#111827;
                "
            >

                <div style="
                    font-size:30px;
                    font-weight:bold;
                    color:white;
                ">
                    {job["job_name"]}
                </div>

                <div style="
                    font-size:16px;
                    color:#9ca3af;
                    margin-top:6px;
                ">
                    {job["target_instance"]}
                </div>

                <div style="
                    margin-top:15px;
                    display:inline-block;
                    padding:6px 14px;
                    border-radius:20px;
                    background-color:{status_color};
                    color:white;
                    font-weight:bold;
                    font-size:14px;
                ">
                    {job["status"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

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

                    st.session_state.page = "home"

                    st.rerun()

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