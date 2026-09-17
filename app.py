import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

from config import (
    APP_MODE,
    PAGE_TITLE,
    BIRTHDAY_PLAN,
    BIRTHDAY_MESSAGE,
    PHOTO_FILES,
)

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="♡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# STYLE
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --cream: #F7F2EA;
        --paper: #FFFDF9;
        --charcoal: #262321;
        --muted: #766F69;
        --burgundy: #7A263A;
        --burgundy-dark: #5B1B2B;
        --line: #E7DED4;
    }

    html, body, [class*="css"] {
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(122,38,58,.06), transparent 28%),
            linear-gradient(180deg, #F9F5EF 0%, #F3ECE4 100%);
        color: var(--charcoal);
    }

    .block-container {
        max-width: 720px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: var(--charcoal);
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: clamp(2.15rem, 7vw, 3.35rem) !important;
        line-height: 1.02 !important;
        margin-bottom: .75rem !important;
    }

    .eyebrow {
        text-transform: uppercase;
        letter-spacing: .18em;
        font-size: .72rem;
        font-weight: 700;
        color: var(--burgundy);
        margin-bottom: .7rem;
    }

    .hero-sub {
        font-size: 1.08rem;
        line-height: 1.65;
        color: var(--muted);
        margin-bottom: 1.4rem;
    }

    .card {
        background: rgba(255,253,249,.94);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.35rem 1.35rem 1.15rem 1.35rem;
        box-shadow: 0 10px 30px rgba(70,49,40,.05);
        margin: .65rem 0 1rem 0;
    }

    .small-note {
        color: var(--muted);
        font-size: .91rem;
        line-height: 1.5;
    }

    .mystery {
        background: #F2E7E8;
        border: 1px solid #E5CDD2;
        color: var(--burgundy-dark);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: .8rem 0 1rem 0;
        text-align: center;
        font-weight: 650;
    }

    .summary-row {
        padding: .68rem 0;
        border-bottom: 1px solid var(--line);
    }

    .summary-label {
        color: var(--muted);
        font-size: .8rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin-bottom: .18rem;
    }

    .summary-value {
        font-size: 1rem;
        font-weight: 650;
        color: var(--charcoal);
    }

    .birthday-box {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 26px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 12px 35px rgba(70,49,40,.06);
    }

    .plan-item {
        display: grid;
        grid-template-columns: 72px 1fr;
        gap: 12px;
        padding: .85rem 0;
        border-bottom: 1px solid var(--line);
        align-items: start;
    }

    .plan-time {
        color: var(--burgundy);
        font-weight: 750;
    }

    .plan-text {
        color: var(--charcoal);
        font-weight: 600;
    }

    .closing {
        text-align: center;
        margin-top: 1.5rem;
        color: var(--muted);
        line-height: 1.7;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 999px;
        border: 1px solid var(--burgundy);
        background: var(--burgundy);
        color: white;
        font-weight: 700;
        min-height: 3.2rem;
        transition: all .18s ease;
    }

    div.stButton > button:hover {
        background: var(--burgundy-dark);
        border-color: var(--burgundy-dark);
        color: white;
        transform: translateY(-1px);
    }

    div[data-baseweb="radio"] label,
    div[data-baseweb="checkbox"] label {
        background: rgba(255,253,249,.75);
        border-radius: 14px;
        padding: .25rem .3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"], footer {
        visibility: hidden;
    }

    /* =========================================
       FINAL TEXT COLOR OVERRIDE
       Questions + all option text
       ========================================= */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #262321 !important;
    }

    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label *,
    [data-testid="stRadio"] p,
    [data-testid="stRadio"] span {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label *,
    [data-testid="stCheckbox"] p,
    [data-testid="stCheckbox"] span {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    [data-testid="stMultiSelect"] *,
    [data-baseweb="select"] * {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    [role="listbox"],
    [role="listbox"] *,
    [role="option"],
    [role="option"] * {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    [data-testid="stSelectbox"] *,
    [data-testid="stSelectbox"] p,
    [data-testid="stSelectbox"] span {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }


    /* =========================================
       SELECTS / MULTISELECTS — LIGHT DROPDOWNS
       ========================================= */

    /* Closed activity multiselect + time selectbox */
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #FFFDF9 !important;
        border-color: #E7DED4 !important;
    }

    [data-testid="stMultiSelect"] input,
    [data-testid="stSelectbox"] input,
    [data-testid="stMultiSelect"] [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* White dropdown panel */
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {
        background: #FFFDF9 !important;
        color: #262321 !important;
    }

    /* Activity and time options */
    [role="option"],
    [role="option"] > div,
    [role="option"] p,
    [role="option"] span {
        background-color: #FFFDF9 !important;
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Hover / selected option */
    [role="option"]:hover,
    [role="option"][aria-selected="true"],
    [role="option"]:hover > div,
    [role="option"][aria-selected="true"] > div {
        background-color: #F2E7E8 !important;
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Selected activities */
    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: #F2E7E8 !important;
        color: #262321 !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] * {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Placeholder text */
    [data-testid="stMultiSelect"] input::placeholder,
    [data-testid="stSelectbox"] input::placeholder {
        color: #766F69 !important;
        -webkit-text-fill-color: #766F69 !important;
        opacity: 1 !important;
    }

    /* Dropdown arrows/icons */
    [data-testid="stMultiSelect"] svg,
    [data-testid="stSelectbox"] svg {
        fill: #262321 !important;
        color: #262321 !important;
    }


    /* =========================================
       TEXT AREA — BIRTHDAY REQUEST
       ========================================= */
    [data-testid="stTextArea"] textarea {
        background-color: #FFFDF9 !important;
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
        border: 1px solid #E7DED4 !important;
        caret-color: #7A263A !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #766F69 !important;
        -webkit-text-fill-color: #766F69 !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] div[data-baseweb="textarea"],
    [data-testid="stTextArea"] div[data-baseweb="textarea"] > div {
        background-color: #FFFDF9 !important;
        border-color: #E7DED4 !important;
    }

    /* =========================================
   START TIME — LIGHT SELECTBOX
   ========================================= */

    /* Closed selectbox */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: white !important;
        background-color: white !important;
        border: 1px solid #E7DED4 !important;
    }

    /* Selected value */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div[aria-selected="true"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div[role="option"] {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Text/input inside the closed select */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
        background: white !important;
        background-color: white !important;
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* BaseWeb value container */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
        background: white !important;
        background-color: white !important;
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Every text element inside the select */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] p {
        color: #262321 !important;
        -webkit-text-fill-color: #262321 !important;
    }

    /* Arrow */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
        fill: #262321 !important;
        color: #262321 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# HELPERS
# -----------------------------
def card_open():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

def init_state():
    defaults = {
        "step": 0,
        "birthday_style": None,
        "activities": [],
        "other_activity": "",
        "food": None,
        "request": "",
        "start_time": None,
        "duration": None,
        "submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    st.session_state.step = max(0, st.session_state.step - 1)
    st.rerun()

def google_sheet():
    """
    Returns a gspread worksheet, or None if secrets are not configured.
    """
    try:
        info = dict(st.secrets["gcp_service_account"])
        sheet_id = st.secrets["sheet_id"]
    except Exception:
        return None

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_id)
    return sh.sheet1

def save_response():
    ws = google_sheet()
    if ws is None:
        return False, "Google Sheets is not configured yet."

    headers = [
        "timestamp_toronto",
        "birthday_style",
        "activities",
        "other_activity",
        "food",
        "special_request",
        "start_time_toronto",
        "duration",
    ]

    existing = ws.row_values(1)
    if not existing:
        ws.append_row(headers)

    now = datetime.now(ZoneInfo("America/Toronto")).strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([
        now,
        st.session_state.birthday_style or "",
        ", ".join(st.session_state.activities),
        st.session_state.other_activity,
        st.session_state.food or "",
        st.session_state.request,
        st.session_state.start_time or "",
        st.session_state.duration or "",
    ])
    return True, "Saved"

def photo_exists(filename):
    return Path(filename).exists()

def show_photo_or_placeholder(filename, caption=None):
    if photo_exists(filename):
        st.image(filename, use_container_width=True, caption=caption)
    else:
        st.markdown(
            """
            <div class="card" style="text-align:center; padding:2.2rem 1rem;">
                <div style="font-size:2rem; margin-bottom:.5rem;">♡</div>
                <div style="font-weight:700;">Your photo goes here</div>
                <div class="small-note">Upload the image to the <code>assets</code> folder using the expected filename.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# FRIDAY MODE: CHOOSE
# -----------------------------
def render_choose_mode():
    init_state()

    st.markdown('<div class="eyebrow">Friday · Choose</div>', unsafe_allow_html=True)
    st.title(PAGE_TITLE)

    if st.session_state.submitted:
        st.markdown(
            """
            <div class="birthday-box" style="text-align:center;">
                <div style="font-size:2.4rem; margin-bottom:.6rem;">♡</div>
                <h2 style="margin-bottom:.5rem;">Birthday request received.</h2>
                <p class="hero-sub" style="margin-bottom:.3rem;">
                    Thiare will take it from here.<br>
                    Your only job is to enjoy your birthday.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_photo_or_placeholder(PHOTO_FILES[0])
        st.markdown(
            '<div class="closing">See you tomorrow, birthday boy.</div>',
            unsafe_allow_html=True,
        )
        return

    step = st.session_state.step

    # STEP 0 - INTRO
    if step == 0:
        st.markdown(
            """
            <p class="hero-sub">
                <b>Hi, birthday boy.</b><br>
                Your birthday is almost here.
            </p>
            <div class="card">
                <p style="font-size:1.08rem; line-height:1.65; margin:0;">
                    I planned a little birthday date for us, but there are a few
                    important decisions that only you can make.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ready?  →", key="ready"):
            next_step()

    # STEP 1 - VIBE
    elif step == 1:
        st.subheader("What kind of birthday do you feel like having?")
        choice = st.radio(
            "Birthday mood",
            [
                "Cozy day together",
                "Gaming day",
                "Movie & drama day",
                "A little bit of everything",
                "Surprise me, Thiare",
            ],
            index=None,
            label_visibility="collapsed",
        )
        st.session_state.birthday_style = choice
        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Next →", disabled=choice is None):
                next_step()

    # STEP 2 - ACTIVITIES
    elif step == 2:
        st.subheader("Pick what you want to do with me")
        st.markdown('<p class="small-note">You can choose as many as you want. It’s your birthday.</p>', unsafe_allow_html=True)
        activities = st.multiselect(
            "Activities",
            [
                "Watch anime",
                "Play PUBG",
                "Watch a movie",
                "Watch a Japanese/Korean drama",
                "Cook together",
                "Eat together on call",
                "Just talk",
                "Something else",
            ],
            default=st.session_state.activities,
            label_visibility="collapsed",
        )
        st.session_state.activities = activities

        if "Something else" in activities:
            st.session_state.other_activity = st.text_input(
                "Tell me what you have in mind",
                value=st.session_state.other_activity,
                placeholder="Anything you want…",
            )

        if "Play PUBG" in activities:
            st.markdown('<div class="mystery">I knew you were going to pick this.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Next →", disabled=len(activities) == 0):
                next_step()

    # STEP 3 - FOOD
    elif step == 3:
        st.subheader("What about birthday food?")
        food = st.radio(
            "Food",
            [
                "Let’s cook something together",
                "Let’s order dinner",
                "You choose for me",
                "Surprise me",
            ],
            index=None,
            label_visibility="collapsed",
        )
        st.session_state.food = food

        st.markdown(
            """
            <div class="mystery">
                <div style="font-size:.82rem; text-transform:uppercase; letter-spacing:.12em; margin-bottom:.25rem;">
                    Dessert?
                </div>
                Don’t worry about that.<br>
                <b>I already took care of it.</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Next →", disabled=food is None):
                next_step()

    # STEP 4 - REQUEST
    elif step == 4:
        st.subheader("Choose one thing you REALLY want to do on your birthday.")
        st.markdown('<p class="small-note">Anything. This is your request.</p>', unsafe_allow_html=True)
        request = st.text_area(
            "Birthday request",
            value=st.session_state.request,
            placeholder="Your request goes here…",
            height=130,
            label_visibility="collapsed",
        )
        st.session_state.request = request

        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Next →", disabled=len(request.strip()) == 0):
                next_step()

    # STEP 5 - TIME
    elif step == 5:
        st.subheader("When do you want our birthday date to start?")
        st.markdown('<p class="small-note">Toronto time.</p>', unsafe_allow_html=True)
        start_time = st.radio(
            "Start time",
            [
                "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM",
                "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM",
                "Other / let’s decide together",
            ],
            index=None,
            label_visibility="collapsed",
        )
        st.session_state.start_time = start_time

        st.subheader("And how long can I keep the birthday boy?")
        duration = st.radio(
            "Duration",
            [
                "A few hours",
                "Most of the day",
                "Until very late",
                "Until one of us falls asleep",
            ],
            index=None,
            label_visibility="collapsed",
        )
        st.session_state.duration = duration

        if duration == "Until one of us falls asleep":
            st.markdown('<div class="mystery">Correct answer.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Next →", disabled=(start_time is None or duration is None)):
                next_step()

    # STEP 6 - ENOUGH DECISIONS
    elif step == 6:
        st.markdown(
            """
            <div class="birthday-box" style="text-align:center;">
                <div class="eyebrow">One last thing</div>
                <h2>Okay. Enough decisions.</h2>
                <p class="hero-sub" style="margin-bottom:.2rem;">
                    You don’t have to plan everything.<br>
                    <b>I’ll take care of the rest.</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Back", on_click=prev_step)
        with c2:
            if st.button("Show my choices →"):
                next_step()

    # STEP 7 - SUMMARY / SUBMIT
    elif step == 7:
        st.subheader("Your birthday request")

        summary = [
            ("Mood", st.session_state.birthday_style),
            ("Activities", ", ".join(st.session_state.activities)),
            ("Birthday food", st.session_state.food),
            ("Your request", st.session_state.request),
            ("Start", st.session_state.start_time + " · Toronto"),
            ("How long", st.session_state.duration),
        ]

        if st.session_state.other_activity:
            summary.insert(2, ("Something else", st.session_state.other_activity))

        st.markdown('<div class="card">', unsafe_allow_html=True)
        for label, value in summary:
            st.markdown(
                f"""
                <div class="summary-row">
                    <div class="summary-label">{label}</div>
                    <div class="summary-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.button("← Change", on_click=prev_step)
        with c2:
            if st.button("Confirm my birthday date ♡"):
                ok, msg = save_response()
                if ok:
                    st.session_state.submitted = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error(
                        "Your choices are ready, but the page cannot save them yet. "
                        "Thiare needs to finish the private Google Sheets connection."
                    )

# -----------------------------
# SATURDAY MODE: BIRTHDAY
# -----------------------------
def render_birthday_mode():
    st.markdown('<div class="eyebrow">Saturday · Birthday</div>', unsafe_allow_html=True)
    st.title("Happy Birthday, Mā-kun.")

    st.markdown(
        """
        <p class="hero-sub">
            You made your choices.<br>
            I promised I would take care of the rest.
        </p>
        """,
        unsafe_allow_html=True,
    )

    show_photo_or_placeholder(PHOTO_FILES[0])

    st.markdown('<div class="birthday-box">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Our day</div>', unsafe_allow_html=True)

    for item in BIRTHDAY_PLAN:
        st.markdown(
            f"""
            <div class="plan-item">
                <div class="plan-time">{item["time"]}</div>
                <div class="plan-text">{item["activity"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="birthday-box">
            <div class="eyebrow">For you</div>
            <div style="font-size:1.04rem; line-height:1.8; white-space:pre-line;">
                {BIRTHDAY_MESSAGE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(PHOTO_FILES) > 1:
        for filename in PHOTO_FILES[1:]:
            if photo_exists(filename):
                st.image(filename, use_container_width=True)

    st.markdown(
        """
        <div class="closing">
            Your only job today is to enjoy your birthday.<br>
            I’ll be right here with you from Chile. ♡
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# APP
# -----------------------------
if APP_MODE.lower() == "birthday":
    render_birthday_mode()
else:
    render_choose_mode()
