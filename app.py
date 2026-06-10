from datetime import datetime
import math
import streamlit as st

# 1. The 60-Year Telugu Samvatsara (Year) Cycle Names
TELUGU_YEARS = [
    "Prabhava", "Vibhava", "Shukla", "Pramodoota", "Prajotpatti", "Angirasa", "Shreemukha", "Bhava", "Yuva", "Dhatu",
    "Eeshvara", "Bahudhanya", "Pramathi", "Vikrama", "Vrusha", "Chitrabhanu", "Subhanu", "Tarana", "Parthiva", "Vyaya",
    "Sarvajittu", "Sarvadhari", "Virodhi", "Vikruti", "Khara", "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi",
    "Hevalambi", "Vilambi", "Vikari", "Sharvari", "Plava", "Shubhakrutu", "Shobhakrutu", "Krodhi", "Visvavasu", "Parabhava",
    "Plavanga", "Keelaka", "Saumya", "Sadharana", "Virodhikrutu", "Paridhavi", "Pramadicha", "Ananda", "Rakshasa", "Nala",
    "Pingala", "Kalayukti", "Siddharthi", "Raudri", "Durmati", "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Akshaya"
]

# 2. Telugu Lunar Months
TELUGU_MONTHS = [
    "Chaitramu", "Vaishakhamu", "Jyeshthamu", "Ashadhamu", "Shravanamu", "Bhadrapadamu",
    "Ashvayujamu", "Kartikamu", "Margashirshamu", "Pushyamu", "Maghamu", "Phalgunamu"
]

# 3. Telugu Tithis (Lunar Days)
TELUGU_TITHIS = [
    "Padyami", "Vidiya", "Tadiya", "Chavithi", "Panchami", "Shashti", "Saptami", "Ashtami", 
    "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Pournami (Full Moon)",
    "Padyami", "Vidiya", "Tadiya", "Chavithi", "Panchami", "Shashti", "Saptami", "Ashtami", 
    "Navami", "Dashami", "Ekadashi", "Dvadashi", "Trayodashi", "Chaturdashi", "Amavasya (New Moon)"
]

def get_julian_date(date_obj):
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

def estimate_lunar_positions(jd, date_obj):
    d = jd - 2451545.0
    sun_long = (280.466 + 0.9856474 * d) % 360
    moon_long = (218.316 + 13.176396 * d) % 360
    tithi_index = min(math.floor(((moon_long - sun_long) % 360) / 12), 29)
    
    shaka_year = date_obj.year - 78
    if date_obj.month < 3 or (date_obj.month == 3 and date_obj.day < 20): 
        shaka_year -= 1
    
    return TELUGU_YEARS[(shaka_year - 1) % 60], TELUGU_MONTHS[(math.floor(sun_long / 30) - 11) % 12], ("Shukla Paksham" if tithi_index < 15 else "Krishna Paksham"), TELUGU_TITHIS[tithi_index]

# --- STREAMLIT USER INTERFACE & DESIGN ---
st.set_page_config(page_title="Telugu Panchangam Converter", page_icon="🔱", layout="centered")

# Custom CSS styling to set Orange background and customize fonts/cards
st.markdown("""
    <style>
        /* 1. Sets main background to a vibrant orange color */
        .stApp {
            background-color: #FF9933;
        }
        
        /* 2. Forces elegant Serif typography across the application */
        html, body, [class*="css"], p, label, h3 {
            font-family: 'Georgia', 'Times New Roman', serif !important;
            color: #1A1A1A !important;
        }
        
        /* 3. Custom design for output boxes / input labels */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 2px solid #002060 !important;
        }
        
        /* 4. Styles metric blocks to contrast nicely against the orange backdrop */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #002060;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.15);
        }
        
        /* Ensures metric text remains dark and readable */
        div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"] {
            color: #002060 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 5. Decorative Heading Banner with Navy Blue background and "Om" symbols
st.markdown("""
    <div style="background-color:#002060; padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 4px 12px rgba(0,0,0,0.25);">
        <h1 style="color:#FFFFFF; font-family:'Georgia', serif; margin:0; font-size: 32px; font-weight: bold;">
            ॐ తెలుగు పంచాంగం కన్వర్టర్ ॐ
        </h1>
        <p style="color:#FF9933; font-size:16px; margin:8px 0 0 0; letter-spacing: 1px; font-weight: bold;">
            Traditional Telugu Panchangam Calendar Converter
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("") 
st.write("") 

# --- Input Configuration (No Date Restrictions) ---
min_possible_date = datetime(1, 1, 1)
max_possible_date = datetime(9999, 12, 31)

st.markdown("**Select an English Date to Convert:**")
selected_date = st.date_input(
    label="Select Date",
    label_visibility="collapsed",
    value=datetime.today(),
    min_value=min_possible_date,
    max_value=max_possible_date
)

st.write("")
left_col, mid_col, right_col = st.columns([1.3, 1, 1])

# --- Execution & Layout Logic ---
if st.button("Convert Date", type="primary"):
    jd = get_julian_date(selected_date)
    samvatsara, month, paksham, tithi = estimate_lunar_positions(jd, selected_date)
    
    st.markdown(f"### 📅 Results for {selected_date.strftime('%d %B, %Y')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Telugu Year (Samvatsaram)", value=samvatsara)
        st.metric(label="Telugu Month (Masam)", value=month)
    with col2:
        st.metric(label="Lunar Phase (Paksham)", value=paksham)
        st.metric(label="Tithi (Lunar Day)", value=tithi)
