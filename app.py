import streamlit as st
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CSDDS Dashboard",
    page_icon="📡",
    layout="wide"
)

# --- INITIALIZE INCIDENT HISTORY ---
if 'incident_history' not in st.session_state:
    st.session_state.incident_history = []

# --- APP TITLE ---
st.title("🔇 Silence & Drift Detection System (CSDDS)")

# --- SIDEBAR: MODE SELECTOR (Requirement 1) ---
st.sidebar.header("🌍 Environment Settings")
mode = st.sidebar.selectbox(
    "Select Operation Mode",
    ["College Network", "Data Center", "Disaster Communication"],
    help="Each mode has different tolerance levels for latency and drift."
)

# --- THRESHOLD CONFIGURATION (Requirement 2 & 4) ---
# We define thresholds based on the selected mode.
# College: High tolerance for laggy Wi-Fi.
# Data Center: Zero tolerance, high-speed fiber requirements.
# Disaster: High latency expected (Satellite/Radio), but needs to stay connected.

if mode == "College Network":
    LATENCY_THRESHOLD = 350  # ms
    DRIFT_THRESHOLD = 70     # ms
    SILENCE_THRESHOLD = 15   # pkt/s (Higher threshold = more sensitive)
    mode_desc = "Standard Wi-Fi Profile: High tolerance for jitter."

elif mode == "Data Center":
    LATENCY_THRESHOLD = 50   # ms (Strict)
    DRIFT_THRESHOLD = 15     # ms (Strict)
    SILENCE_THRESHOLD = 40   # pkt/s (Extremely sensitive)
    mode_desc = "Enterprise Profile: Critical low-latency monitoring."

else: # Disaster Communication
    LATENCY_THRESHOLD = 600  # ms (Satellite delay allowed)
    DRIFT_THRESHOLD = 120    # ms
    SILENCE_THRESHOLD = 5    # pkt/s (Tolerates very thin data streams)
    mode_desc = "Survival Profile: Prioritizes connection over speed."

# --- SIDEBAR: SIMULATION CONTROLS ---
st.sidebar.divider()
st.sidebar.header("🛠️ Simulation Controls")
packet_rate = st.sidebar.slider("Packet Rate (packets/sec)", 0, 100, 100)
simulated_latency = st.sidebar.slider("Simulated Latency (ms)", 0, 700, 20)
clock_drift = st.sidebar.slider("Clock Drift (ms)", 0, 150, 0)

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.incident_history = []
    st.rerun()

# --- DETECTION LOGIC (Requirement 5) ---
# Severity score is now relative to the Mode Thresholds
latency_severity = (simulated_latency / LATENCY_THRESHOLD) * 33
drift_severity = (clock_drift / DRIFT_THRESHOLD) * 33
silence_severity = ((100 - packet_rate) / 100) * 34

severity_score = min(100, int(latency_severity + drift_severity + silence_severity))

# --- DISPLAY ACTIVE MODE (Requirement 3) ---
st.info(f"**Active Mode:** {mode} | {mode_desc}")

# --- SEVERITY & SUGGESTIONS ---
col_score, col_alert = st.columns([1, 2])

with col_score:
    st.subheader("⚠️ Severity")
    s_color = "green" if severity_score < 30 else "orange" if severity_score < 70 else "red"
    st.markdown(f"Score: **:{s_color}[{severity_score}/100]**")
    st.progress(severity_score / 100)

with col_alert:
    st.subheader("💡 Recommended Action")
    current_issue = None
    
    # Check against dynamic thresholds
    if packet_rate < SILENCE_THRESHOLD:
        st.warning(f"🚨 **Silence:** Packet rate below {SILENCE_THRESHOLD} for {mode}.")
        current_issue = "Silence"
    elif simulated_latency > LATENCY_THRESHOLD:
        st.warning(f"🌐 **Latency:** Exceeded {LATENCY_THRESHOLD}ms limit for {mode}.")
        current_issue = "High Latency"
    elif clock_drift > DRIFT_THRESHOLD:
        st.warning(f"⏳ **Drift:** Exceeded {DRIFT_THRESHOLD}ms limit for {mode}.")
        current_issue = "High Drift"
    else:
        st.success("✅ System stable for current environment.")

# --- INCIDENT LOGGING ---
if current_issue:
    timestamp = datetime.now().strftime("%H:%M:%S")
    if (not st.session_state.incident_history or 
        st.session_state.incident_history[-1]["Issue Type"] != current_issue):
        st.session_state.incident_history.append({
            "Time": timestamp, 
            "Issue Type": current_issue, 
            "Mode": mode,
            "Severity": f"{severity_score}/100"
        })
        if len(st.session_state.incident_history) > 5: st.session_state.incident_history.pop(0)

# --- HISTORY & METRICS ---
st.divider()
st.subheader("📜 Incident History")
st.table(st.session_state.incident_history)

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Packet Rate", f"{packet_rate}/s", delta_color="inverse")
c2.metric("Latency", f"{simulated_latency}ms", delta=f"{simulated_latency - LATENCY_THRESHOLD}ms", delta_color="inverse")
c3.metric("Clock Offset", f"{clock_drift}ms", delta=f"{clock_drift - DRIFT_THRESHOLD}ms", delta_color="inverse")

st.caption(f"CSDDS Dashboard | Mode-Specific Thresholding Active")
