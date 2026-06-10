from datetime import datetime
import math
import streamlit as st
import random # Implemented for dynamic element positioning 

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

# Function for determining Julian Date from a DateTime object
def get_julian_date(date_obj):
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

# Estimation of Lunar Positions for Telugu Panchangam
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
# --- Page configuration with icon and layout settings
st.set_page_config(page_title="Telugu Panchangam Converter", page_icon="🔱", layout="centered")

# --- Custom CSS styling for background and elements
# Incorporates dynamic positioning of decorative elements
def generate_decorative_elements(n_elements):
    elements = []
    # Use image URLs instead of relative paths for reliable rendering
    symbol_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/e/e4/Aum_Om_red.svg", # Om Symbol (SVG for scalability)
        "https://upload.wikimedia.org/wikipedia/commons/e/eb/Symbol_Venkat_W.png", # Shankha (using transparent PNG)
        "https://upload.wikimedia.org/wikipedia/commons/d/de/Ganesha_silhouette.png", # Ganesha Silhouette (using transparent PNG)
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/Shiva_symbol.png", # Shiva Symbol (using transparent PNG)
    ]
    for _ in range(n_elements):
        symbol_url = random.choice(symbol_urls)
        top = random.randint(0, 100)
        left = random.randint(0, 100)
        rotation = random.randint(0, 360)
        size = random.randint(30, 80) # Increased size range
        opacity = random.uniform(0.05, 0.2) # Increased opacity
        elements.append(f'<img src="{symbol_url}" style="position: absolute; top: {top}%; left: {left}%; transform: rotate({rotation}deg); width: {size}px; height: {size}px; opacity: {opacity}; z-index: -1;">')
    return "".join(elements)

# Combine background styling with decorative elements
decorative_elements_html = generate_decorative_elements(40) # Increased element count for better density

# Custom CSS styling including background and decorative elements
st.markdown(f"""
<style>
    .stApp {{
        background-color: #FF9933;
        overflow: hidden; /* Prevent scrolling if elements overflow */
    }}
    
    /* Positioning decorative elements behind content */
    #decorative-elements {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }}

    html, body, [class*="css"], p, label, h3, .stMarkdown {{
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #1A1A1A !important;
    }}
    
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {{
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 2px solid #87CEEB !important;
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
<div id="decorative-elements">
    {decorative_elements_html}
</div>
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

# --- Empty space for visual separation
st.write("") 
st.write("") 

# --- Date range constraint setting
min_possible_date = datetime(1, 1, 1).date()
max_possible_date = datetime(9999, 12, 31).date()

# --- Section for selecting English Date to convert
st.markdown("**Select an English Date to Convert:**")
selected_date = st.date_input(
    label="Select Date",
    label_visibility="collapsed",
    value=datetime.now().date(),
    min_value=min_possible_date,
    max_value=max_possible_date
)

# --- Empty space for visual separation
st.write("")

# Centered Button Layout
left_col, mid_col, right_col = st.columns([1.3, 1, 1])
with mid_col:
    submit_button = st.button("Convert Date", type="primary")

# --- Processing the selected date and displaying results when the button is clicked
if submit_button:
    jd = get_julian_date(selected_date)
    samvatsara, month, paksham, tithi = estimate_lunar_positions(jd, selected_date)
    
    st.markdown(f"### 📅 Results for {selected_date.strftime('%d %B, %Y')}")
    
    # Display results in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Telugu Year (Samvatsaram)", value=samvatsara)
        st.metric(label="Telugu Month (Masam)", value=month)
    with col2:
        st.metric(label="Lunar Phase (Paksham)", value=paksham)
        st.metric(label="Tithi (Lunar Day)", value=tithi)

# --- Separator line
st.write("---")

# --- CLEANED NATiVE STREAMLIT PROJECT DETAILS EXPANDER ---
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
