import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- DATABASE INTEGRATION ---
def init_db():
    conn = sqlite3.connect('cync_event_leads.db')
    c = conn.cursor()
    # Table for capturing partner leads (Real-time tracking)
    c.execute('''CREATE TABLE IF NOT EXISTS leads 
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, 
                  source_partner TEXT, zone TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

def log_lead(name, email, partner, zone):
    conn = sqlite3.connect('cync_event_leads.db')
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, email, source_partner, zone, timestamp) VALUES (?, ?, ?, ?, ?)",
              (name, email, partner, zone, datetime.now()))
    conn.commit()
    conn.close()

init_db()

# --- APP STYLING ---
st.set_page_config(page_title="CYNC IN THE CITY | Pulse App", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .stButton>button { border-radius: 12px; background: linear-gradient(90deg, #00F2FF, #00FF87); color: black; border: none; font-weight: bold; }
    .metric-box { padding: 20px; border-radius: 15px; background: #111; border: 1px solid #222; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- APP CONTENT ---
st.title("⚡ CYNC IN THE CITY")
st.caption("Gallagher Convention Centre | Johannesburg 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Programme", "🛡️ Scan & Heatmap", "💰 Wallet", "👤 Profile"])

# TAB 1: CYNC PROGRAMME
with tab1:
    st.subheader("The Weekend Rhythm")
    itinerary = pd.DataFrame([
        {"Time": "08:00", "Activity": "CYNC 10K Run", "Venue": "Midrand Circuit"},
        {"Time": "11:00", "Activity": "Step-Nation (Amapiano)", "Venue": "Hall 2"},
        {"Time": "14:00", "Activity": "The Grid Qualifiers", "Venue": "Hall 1"},
        {"Time": "16:30", "Activity": "Yoga & Live DJ Set", "Venue": "Sunset Deck"}
    ])
    st.table(itinerary)

# TAB 2: SCANNER & LEAD CAPTURE
with tab2:
    st.subheader("Station Check-In")
    st.write("Scan at stations to unlock rewards and track your burn.")
    
    with st.expander("👉 Open Check-In Scanner (Demo Mode)"):
        u_name = st.text_input("Name")
        u_email = st.text_input("Email")
        u_partner = st.selectbox("Partner Station", ["Vitality", "Vodacom", "Under Armour", "Biogen"])
        u_zone = st.selectbox("Current Zone", ["The Gauntlet", "Step-Up Stage", "Sneaker Lab", "Refuel Zone"])
        
        if st.button("Check-In & Unlock Reward"):
            if u_name and u_email:
                log_lead(u_name, u_email, u_partner, u_zone)
                st.success(f"Verified! 550 Calories logged. Your {u_partner} reward is ready at the desk!")
            else:
                st.error("Please enter your details to sync.")

    # Real-time Capacity Simulation
    st.divider()
    st.subheader("Live Zone Capacity")
    col1, col2 = st.columns(2)
    col1.metric("The Gauntlet", "42/50", "High Traffic", delta_color="inverse")
    col2.metric("Sneaker Lab", "12/30", "Space Available")

# TAB 3: THE CYNC WALLET
with tab3:
    st.subheader("Your Pulse Wallet")
    st.markdown("<div class='metric-box'><h3>Balance: R 850.00</h3><p>Includes Grid Challenge Cash Prize</p></div>", unsafe_allow_html=True)
    
    st.write("### Recent Activity")
    st.write("✅ +R500.00 | Grid Challenge Win")
    st.write("🛒 -R120.00 | Healthy Mzansi Food Court")
    st.write("✅ +R50.00 | Vitality Early-Bird Bonus")

# TAB 4: PROFILE & ANALYTICS
with tab4:
    st.subheader("Lebo M. | Urban Athlete")
    st.write("🏆 **Total Burn Today:** 1,450 kcal")
    st.write("👟 **Cync Perk:** 1-Month Partner Gym Trial (Active)")
    
    # Internal Lead Export for Organizers
    if st.checkbox("Show Lead Tracking Data (Admin)"):
        conn = sqlite3.connect('cync_event_leads.db')
        df = pd.read_sql_query("SELECT * FROM leads", conn)
        st.dataframe(df)
        st.download_button("Export Leads to CSV", df.to_csv(), "cync_leads_export.csv")

