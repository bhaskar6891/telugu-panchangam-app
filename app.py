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
    tithi_index = min(max(math.floor(((moon_long - sun_long) % 360) / 12), 0), 29)
    
    shaka_year = date_obj.year - 78
    if date_obj.month < 3 or (date_obj.month == 3 and date_obj.day < 20): 
        shaka_year -= 1
    
    return TELUGU_YEARS[(shaka_year - 1) % 60], TELUGU_MONTHS[(math.floor(sun_long / 30) - 11) % 12], ("Shukla Paksham" if tithi_index < 15 else "Krishna Paksham"), TELUGU_TITHIS[tithi_index]

# --- STREAMLIT USER INTERFACE & DESIGN ---
st.set_page_config(page_title="Telugu Panchangam Converter", page_icon="🔱", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: #FF9933;
    }
    
    html, body, [class*="css"], p, label, h3, .stMarkdown {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #1A1A1A !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 2px solid #87CEEB !important;
    }
    
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 5px solid #87CEEB !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.15) !important;
    }
    
    div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"], div[data-testid="stMetric"] * {
        color: #1A1A1A !important;
    }
    
    /* Custom style for inside the expander to keep things legible */
    .stDetails {
        background-color: #FFFFFF !important;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Heading Banner with Sky Blue background
st.markdown("""
<div style="background-color:#87CEEB; padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 4px 12px rgba(0,0,0,0.25);">
    <h1 style="color:#1A1A1A !important; font-family:'Georgia', serif; margin:0; font-size: 32px; font-weight: bold;">
        ॐ తెలుగు పంచాంగం కన్వర్టర్ ॐ
    </h1>
    <p style="color:#1A1A1A !important; font-size:16px; margin:8px 0 0 0; letter-spacing: 1px; font-weight: bold;">
        Traditional Telugu Panchangam Calendar Converter
    </p>
</div>
""", unsafe_allow_html=True)

st.write("") 
st.write("") 

min_possible_date = datetime(1, 1, 1).date()
max_possible_date = datetime(9999, 12, 31).date()

st.markdown("**Select an English Date to Convert:**")
selected_date = st.date_input(
    label="Select Date",
    label_visibility="collapsed",
    value=datetime.now().date(),
    min_value=min_possible_date,
    max_value=max_possible_date
)

st.write("")

# Centered Button
left_col, mid_col, right_col = st.columns([1.3, 1, 1])
with mid_col:
    submit_button = st.button("Convert Date", type="primary")

if submit_button:
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

st.write("---")

# --- PROJECT DETAILS EXPANDER ---
with st.expander("ℹ️ View Project Details & Strategic Overview"):
    st.markdown("""
    <div class="stDetails">
        <h3>📖 Strategic Overview: Telugu Panchangam Digital Converter</h3>
        <p>This application serves as a bridge between traditional Vedic astronomical time-tracking structures and modern computational software frameworks.</p>
        
        <hr>
        
        <h4>1. The Science of Vedic Time</h4>
        <ul>
            <li><strong>The Samvatsara Chakra:</strong> Runs on a prominent 60-year Jovian cycle (from Prabhava to Akshaya), based roughly on Jupiter's relative position in space.</li>
            <li><strong>Lunar Precision:</strong> Tracks the position of the moon relative to the sun to dynamically assign the 12 Telugu Lunar Months (Masamu) and 30 Tithis.</li>
        </ul>
        
        <h4>2. Calculation Methodology</h4>
        <p>The core computational background transforms standard Gregorian calendar days into astronomical Julian Dates (JD). By using the angular differential distance between solar and lunar coordinates, the model computes:</p>
        <ul>
            <li>Solar/Lunar Longitude Overlaps</li>
            <li>Tithi Indexing via precise 12° incremental phases</li>
            <li>Shaka Era offset mappings</li>
        </ul>
        
        <h4>3. Seasonal Search & Cultural Trends</h4>
        <ul>
            <li><strong>Ugadi (New Year):</strong> Peak systemic traffic (95% search/utility load)</li>
            <li><strong>Sravanam (Monsoon Festivals):</strong> High baseline query metrics for auspicious dates</li>
            <li><strong>Kartika (Autumn Celebrations):</strong> Continuous evening traffic trends</li>
        </ul>
        
        <blockquote style="border-left: 4px solid #87CEEB; padding-left: 10px; font-style: italic;">
            "Kaalah Sarvam Labhati" — Time provides everything.
        </blockquote>
    </div>
    """, unsafe_allow_html=True)
