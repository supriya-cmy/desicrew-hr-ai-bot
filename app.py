# =========================
# app.py
# Candidate Screening Form
# =========================

import streamlit as st
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, timedelta

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="DesiCrew Recruitment",
    layout="centered"
)

# -------------------------------------------------
# PROFESSIONAL UI
# -------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FC;
}

.main-title {
    color: #0B1F3A;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: #4B5563;
    font-size: 18px;
}

.stButton button {
    background-color: #0B1F3A;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    border: none;
    font-size: 16px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #163A6B;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("HR_AI_DATABASE").sheet1

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.image("logo.png", width=180)

st.markdown(
    '<div class="main-title">DesiCrew Recruitment</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI Powered Interview Screening</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------------------------------------
# FORM
# -------------------------------------------------

with st.form("candidate_form"):

    st.subheader("👤 Basic Information")

    name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1980,1,1),
        max_value=date.today()
    )

    mobile = st.text_input("Mobile Number")

    email = st.text_input("Email ID")

    location = st.text_input("Current Location")

    st.markdown("---")

    st.subheader("🎓 Education & Experience")

    candidate_type = st.selectbox(
        "Candidate Type",
        ["Fresher", "Experienced"]
    )

    arrear = "No"

    experience = ""

    current_salary = ""

    expected_salary = ""

    negotiable = ""

    if candidate_type == "Fresher":

        arrear = st.selectbox(
            "Any Arrears?",
            ["Yes", "No"]
        )

    if candidate_type == "Experienced":

        years = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=20
        )

        months = st.number_input(
            "Months",
            min_value=0,
            max_value=11
        )

        experience = f"{years} Years {months} Months"

        current_salary = st.text_input(
            "Current Salary"
        )

        expected_salary = st.number_input(
            "Expected Salary",
            min_value=0
        )

        if expected_salary > 25000:

            negotiable = st.selectbox(
                "Is salary negotiable?",
                ["Yes", "No"]
            )

    st.markdown("---")

    st.subheader("🛠 Screening Questions")

    availability = st.selectbox(
        "Available for Job Change?",
        ["Yes", "No"]
    )

    night_shift = st.selectbox(
        "Willing to work Night Shift?",
        ["Yes", "No"]
    )

    distance = st.selectbox(
        "Distance from Tidel Neo",
        [
            "Less than 5 kms",
            "5 - 10 kms",
            "10 - 15 kms",
            "15 - 20 kms",
            "20 - 30 kms"
        ]
    )

    relocate = "No"

    if distance == "20 - 30 kms":

        relocate = st.selectbox(
            "Willing to Relocate?",
            ["Yes", "No"]
        )

    notice_period = st.number_input(
        "Notice Period (Days)",
        min_value=0,
        max_value=90
    )

    interview_date = st.date_input(
        "Preferred Interview Date",
        min_value=date.today() + timedelta(days=1)
    )

    submit = st.form_submit_button(
        "Submit Application"
    )

# -------------------------------------------------
# SAVE DATA
# -------------------------------------------------

if submit:

    sheet.append_row([

        name,
        str(dob),
        mobile,
        email,
        location,
        candidate_type,
        arrear,
        experience,
        current_salary,
        expected_salary,
        negotiable,
        availability,
        night_shift,
        distance,
        relocate,
        notice_period,
        str(interview_date),
        "Interview Scheduled",
        "Pending",
        "No",
        "Open",
        "Pending",
        ""

    ])

    st.success(
        "✅ Interview date confirmed successfully."
    )

    st.info(
        "📧 You will receive an email regarding Venue, Interview Date and Time."
    )