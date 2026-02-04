import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CSDDS Dashboard",
    page_icon="📡",
    layout="wide"
)

# --- APP TITLE ---
st.title("🔇 Silence & Drift Detection System (CSDDS)")
st.markdown("""
    This system monitors real-time data streams to detect **Signal Silence** 
    and **Timing Drift** before they impact the user experience.
""")

# --- SIDEBAR CONTROLS (Input Simulation Module UI) ---
st.sidebar.header("🛠️ Simulation Controls")
st.sidebar.write("Adjust these sliders to simulate network conditions.")

# Requirement: Packet Rate (0-100)
packet_rate = st.sidebar.slider(
    "Packet Rate (packets/sec)", 
    min_value=0, 
    max_value=100, 
    value=50,
    help="How many data packets are sent per second."
)

# Requirement: Latency (0-500 ms)
simulated_latency = st.sidebar.slider(
    "Simulated Latency (ms)", 
    min_value=0, 
    max_value=500, 
    value=50,
    help="The delay between sender and receiver."
)

# Requirement: Clock Drift (0-100 ms)
clock_drift = st.sidebar.slider(
    "Clock Drift (ms)", 
    min_value=0, 
    max_value=100, 
    value=0,
    help="The gradual accumulation of timing misalignment."
)

st.sidebar.divider()
if st.sidebar.button("Reset Simulation"):
    st.rerun()

# --- MAIN DASHBOARD LAYOUT ---

# Top Row: Three columns for the three key monitoring sections
col1, col2, col3 = st.columns(3)

# 1. Current Network Health Section
with col1:
    st.subheader("🌐 Network Health")
    # Simple logic to determine health status based on inputs
    if packet_rate == 0:
        health_status = "Disconnected"
        color = "red"
    elif simulated_latency > 300 or clock_drift > 50:
        health_status = "Poor"
        color = "orange"
    else:
        health_status = "Excellent"
        color = "green"
    
    st.markdown(f"**Status:** :{color}[{health_status}]")
    st.metric(label="Current Latency", value=f"{simulated_latency} ms")

# 2. Silence Status Section
with col2:
    st.subheader("🔕 Silence Status")
    # If packet rate is 0, we assume silence is detected
    if packet_rate == 0:
        st.error("SILENCE DETECTED")
        st.write("No incoming data packets.")
    else:
        st.success("Signal Active")
        st.write(f"Receiving {packet_rate} packets/sec.")

# 3. Drift Status Section
with col3:
    st.subheader("⏳ Drift Status")
    # Logic to warn about drift
    if clock_drift > 70:
        st.error("CRITICAL DRIFT")
    elif clock_drift > 30:
        st.warning("DRIFT WARNING")
    else:
        st.info("Timing Stable")
    
    st.metric(label="Clock Offset", value=f"{clock_drift} ms", delta=f"{clock_drift} ms")

# --- DATA VISUALIZATION SECTION (Placeholders for next steps) ---
st.divider()
st.subheader("📈 Real-Time Analytics")

# Creating a placeholder for the live graph we will build in the next step
chart_placeholder = st.empty()
with chart_placeholder.container():
    st.info("System is ready. Start the simulation to see packet flow graph.")
    # We will use st.line_chart here in the next module

# --- FOOTER ---
st.caption("CSDDS Project Architecture - Hackathon Prototype")
