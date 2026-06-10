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

# Custom CSS styling to set Orange background and customize fonts/cards
st.markdown("""
    <style>
        /* 1. Sets main background to a vibrant orange color */
        .stApp {
            background-color: #FF9933;
        }
        
        /* 2. Forces elegant Serif typography across the application */
        html, body, [class*="css"], p, label, h3, .stMarkdown {
            font-family: 'Georgia', 'Times New Roman', serif !important;
            color: #1A1A1A !important;
        }
