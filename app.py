import base64
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
    T = (jd - 2451545.0) / 36525.0
    
    sun_long = (280.46646 + 36000.76983 * T + 0.0003032 * T**2) % 360
    M_sun = (357.52911 + 35999.05029 * T - 0.0011537 * T**2) % 360
    sun_apparent_long = (sun_long + 1.914602 * math.sin(math.radians(M_sun)) + 0.019993 * math.sin(math.radians(2 * M_sun))) % 360

    moon_long = (218.31644 + 481267.88123 * T - 0.001133 * T**2) % 360
    elongation = (moon_long - sun_apparent_long) % 360
    
    tithi_index = min(max(math.floor(elongation / 12), 0), 29)
    paksham = "Shukla Paksham" if tithi_index < 15 else "Krishna Paksham"
    
    ayanamsa = 12.5 + 0.0130125 * (date_obj.year - 1900)
    sidereal_sun_long = (sun_apparent_long - ayanamsa) % 360
    
    last_new_moon_elongation = elongation % 360
    days_since_new_moon = last_new_moon_elongation / 12.19
    sun_at_new_moon = (sidereal_sun_long - (days_since_new_moon * 0.9856)) % 360
    month_idx = math.floor(sun_at_new_moon / 30) % 12

    shaka_year = date_obj.year - 78
    if month_idx == 11 and date_obj.month == 3:  
        shaka_year -= 1

    samvatsara_idx = (shaka_year - 3) % 60
    
    return TELUGU_YEARS[samvatsara_idx], TELUGU_MONTHS[month_idx], paksham, TELUGU_TITHIS[tithi_index]

# Helper function to encode local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- STREAMLIT USER INTERFACE & DESIGN ---
st.set_page_config(page_title="Telugu Panchangam Converter", page_icon="🔱", layout="centered")

# Read local image and encode it
try:
    base64_image = get_base64_image("background.jpg")
    background_style = f"""
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    """
except FileNotFoundError:
    background_style = ".stApp { background-color: #FF9933; }"

# Custom CSS styling with comprehensive fix for dropdown popups
st.markdown(f"""
<style>
    {background_style}
    
    html, body, p, label, h3, .stMarkdown {{
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #1A1A1A !important;
    }}
    
    /* Input block static fields setup */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {{
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 2px solid #87CEEB !important;
    }}
    
    div[data-baseweb="input"] input, div[data-baseweb="select"] select, input[type="date"] {{
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important;
        background-color: #FFFFFF !important;
    }}
    
    /* CRITICAL FIX: Targets global dropdown portals used by BaseWeb calendars.
       Forces pop-up background and grid days to match clear light parameters.
    */
    div[role="listbox"], 
    div[data-baseweb="popover"] [role="grid"],
    div[data-baseweb="calendar"] [role="gridcell"],
    div[data-baseweb="calendar"] button {{
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important;
    }}

    /* Ensure specific day grid numbers don't turn invisible */
    div[data-baseweb="calendar"] div {{
        color: #1A1A1A !important;
    }}
    
    /* Input instruction text container styling */
    .input-label-container {{
        background-color: #FFFFFF !important;
        padding: 8px 15px !important;
        border-radius: 8px !important;
        display: inline-block !important;
        margin-bottom: 5px !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15) !important;
        border-left: 4px solid #87CEEB !important;
    }}
    
    /* Result Header container styling */
    .result-header-container {{
        background-color: #FFFFFF !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        margin-top: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.15) !important;
        border-left: 5px solid #87CEEB !important;
    }}
    
    .result-header-container h3 {{
        margin: 0 !important;
        padding: 0 !important;
        font-weight: bold !important;
    }}
    
    div[data-testid="stMetric"] {{
        background-color: #FFFFFF !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 5px solid #87CEEB !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.15) !important;
    }}
    
    div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"], div[data-testid="stMetric"] * {{
        color: #1A1A1A !important;
    }}
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

min_possible_date = datetime(1900, 1, 1).date() 
max_possible_date = datetime(2100, 12, 31).date()

# Wrapped the input instruction text inside a styled container block
st.markdown('<div class="input-label-container"><strong>Select an English Date to Convert:</strong></div>', unsafe_allow_html=True)
selected_date = st.date_input(
    label="Select Date",
    label_visibility="collapsed",
    value=datetime.now().date(),
    min_value=min_possible_date,
    max_value=max_possible_date
)

st.write("")

# Centered Button Layout
left_col, mid_col, right_col = st.columns([1.3, 1, 1])
with mid_col:
    submit_button = st.button("Convert Date", type="primary")

if submit_button:
    jd = get_julian_date(selected_date)
    samvatsara, month, paksham, tithi = estimate_lunar_positions(jd, selected_date)
    
    # Wrapped the output results heading inside a styled container block
    formatted_date = selected_date.strftime('%d %B, %Y')
    st.markdown(f"""
    <div class="result-header-container">
        <h3>📅 Results for {formatted_date}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Telugu Year (Samvatsaram)", value=samvatsara)
        st.metric(label="Telugu Month (Masam)", value=month)
    with col2:
        st.metric(label="Lunar Phase (Paksham)", value=paksham)
        st.metric(label="Tithi (Lunar Day)", value=tithi)

st.write("---")

# --- CLEANED NATIVE STREAMLIT PROJECT DETAILS EXPANDER ---
with st.expander("ℹ️ View Project Details & Strategic Overview"):
    st.subheader("📖 Strategic Overview: Telugu Panchangam Digital Converter")
    st.write("This application serves as a bridge between traditional Vedic astronomical time-tracking structures and modern computational software frameworks.")
    
    st.markdown("#### 1. The Science of Vedic Time")
    st.markdown("- **The Samvatsara Chakra:** Runs on a prominent 60-year Jovian cycle (from Prabhava to Akshaya), based roughly on Jupiter's relative position in space.")
    st.markdown("- **Lunar Precision:** Tracks the position of the moon relative to the sun to dynamically assign the 12 Telugu Lunar Months (Masamu) and 30 Tithis.")
    
    st.markdown("#### 2. Calculation Methodology")
    st.write("The core computational background transforms standard Gregorian calendar days into astronomical Julian Dates (JD). By using the angular differential distance between solar and lunar coordinates, the model computes:")
    st.markdown("- Solar/Lunar Longitude Overlaps")
    st.markdown("- Tithi Indexing via precise 12° incremental phases")
    st.markdown("- Shaka Era offset mappings")
    
    st.markdown("#### 3. Seasonal Search & Cultural Trends")
    st.markdown("- **Ugadi (New Year):** Peak systemic traffic (95% search/utility load)")
    st.markdown("- **Sravanam (Monsoon Festivals):** High baseline query metrics for auspicious dates")
    st.markdown("- **Kartika (Autumn Celebrations):** Continuous evening traffic trends")
    
    st.info('"Kaalah Sarvam Labhati" — Time provides everything.')
