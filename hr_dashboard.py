# =========================
# hr_dashboard.py
# =========================

import streamlit as st
import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="HR Dashboard",
    layout="wide"
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
    font-size: 40px;
    font-weight: bold;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

.metric-number {
    color: #0B1F3A;
    font-size: 32px;
    font-weight: bold;
}

.metric-label {
    color: #6B7280;
    font-size: 14px;
}

.stButton button {
    background-color: #0B1F3A;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    border: none;
    font-size: 15px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOGIN
# -------------------------------------------------

USERNAME = "admin"

PASSWORD = "Desi@123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 HR Dashboard Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Invalid Credentials")

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

else:

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

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

    col1, col2 = st.columns([1,5])

    with col1:
        st.image("logo.png", width=120)

    with col2:

        st.markdown(
            '<div class="main-title">🛠 HR Recruitment Dashboard</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------

    total = len(df)

    selected = len(
        df[df["Final Status"] == "Selected"]
    )

    rejected = len(
        df[df["Final Status"] == "Rejected"]
    )

    pending = len(
        df[df["Follow Up Status"] == "Pending"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{total}</div>
        <div class="metric-label">Total Candidates</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{selected}</div>
        <div class="metric-label">Selected</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{rejected}</div>
        <div class="metric-label">Rejected</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{pending}</div>
        <div class="metric-label">Pending Follow Up</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------
    # DATABASE
    # -------------------------------------------------

    st.subheader("📋 Candidate Database")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    # -------------------------------------------------
    # UPDATE PANEL
    # -------------------------------------------------

    st.subheader("🛠 Update Candidate Status")

    candidate_names = df["Name"].tolist()

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_names
    )

    attendance = st.selectbox(
        "Interview Attendance",
        [
            "Pending",
            "Attended",
            "Did Not Attend"
        ]
    )

    final_status = st.selectbox(
        "Final Status",
        [
            "Open",
            "Selected",
            "Hold",
            "Rejected"
        ]
    )

    followup = st.selectbox(
        "Follow Up Status",
        [
            "Pending",
            "Completed",
            "Interested",
            "No Response",
            "Not Interested"
        ]
    )

    remarks = st.text_area(
        "HR Remarks"
    )

    if st.button("Update Candidate"):

        cell = sheet.find(selected_candidate)

        row_number = cell.row

        sheet.batch_update([

            {
                'range': f'V{row_number}',
                'values': [[attendance]]
            },

            {
                'range': f'U{row_number}',
                'values': [[final_status]]
            },

            {
                'range': f'S{row_number}',
                'values': [[followup]]
            },

            {
                'range': f'W{row_number}',
                'values': [[remarks]]
            }

        ])

        st.success(
            "✅ Candidate updated successfully."
        )

    st.markdown("---")

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()