import streamlit as st
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import tensorflow as tf

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="FinGuard Elite | AI Security", page_icon="🛡️", layout="wide")

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white; border: none; border-radius: 8px;
        padding: 12px; font-weight: bold; width: 100%;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5); }
    .intro-box {
        background: #161b22; padding: 25px; border-radius: 15px; 
        border-left: 5px solid #00d2ff; margin-bottom: 25px;
    }
    .success-card {
        background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc;
        color: #00ffcc; padding: 25px; border-radius: 12px; text-align: center;
    }
    .fraud-alert {
        background: rgba(255, 75, 75, 0.1); border: 2px solid #ff4b4b;
        color: #ff4b4b; padding: 20px; border-radius: 12px; text-align: center;
        font-size: 24px; font-weight: bold; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ASSET LOADING ---
@st.cache_resource
def load_models():
    scaler = joblib.load('Models/scaler.pkl')
    ann_model = tf.keras.models.load_model('Models/finguard_ann.h5')
    xgb_model = xgb.Booster()
    xgb_model.load_model('Models/finguard_xgb.json')
    return scaler, ann_model, xgb_model

scaler, ann_model, xgb_model = load_models()

# --- 4. SIDEBAR: SYSTEM CONTROLS & INTELLIGENCE GUIDE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("System Controls")
    st.markdown("---")
    
    engine_choice = st.radio("Intelligence Engine", ["XGBoost High-Speed", "Neural Network (ANN)"])
    
    st.markdown("---")
    st.subheader("💡 Intelligence Guide")
    if engine_choice == "XGBoost High-Speed":
        st.write("**Strategy:** Customer-First")
        st.caption("Optimized for speed and minimal false alarms. Best for keeping genuine transactions moving quickly.")
    else:
        st.write("**Strategy:** Security-First")
        st.caption("Deep-scan mode. Caught 85% of fraud in testing but may occasionally flag unusual genuine activity for review.")
    
    st.markdown("---")
    st.info("Current Status: System Operational ✅")

# --- 5. INTRODUCTION & MISSION ---
st.title("🛡️ FinGuard: Advanced Fraud Detection")

st.markdown(f"""
<div class="intro-box">
    <h3>The Mission</h3>
    FinGuard serves as a shield against digital theft. By analyzing subtle patterns in massive, 
    imbalanced datasets, we intercept fraud in milliseconds—protecting your business 
    without slowing down your customers.
</div>
""", unsafe_allow_html=True)

# --- 6. PROJECT STATS SECTION ---
st.subheader("📊 Project Highlights")
stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.metric(label="Total Transactions Analyzed", value="284,808")
    st.caption("Massive dataset training")

with stat_col2:
    st.metric(label="Fraud Incidence Rate", value="0.172%", delta="-0.02%", delta_color="inverse")
    st.caption("Highly imbalanced signal detection")

with stat_col3:
    st.metric(label="System Latency", value="< 50ms")
    st.caption("Real-time intercept capability")

st.markdown("---")

# --- 7. TRANSACTION INPUT PANEL ---
t_col1, t_col2 = st.columns(2)
with t_col1:
    st.subheader("💰 Transaction Amount")
    amount = st.number_input("How much is being sent? ($)", min_value=0.01, value=450.00, step=10.0)

with t_col2:
    st.subheader("🕒 Timing")
    time_val = st.number_input("Seconds since customer's last login", min_value=0, max_value=172792, value=1000)

st.markdown("---")
st.subheader("🔍 Hidden Pattern Analysis")
st.write("Adjust the behavioral signals (V1-V28) to simulate specific transaction signatures.")

# Grouping V columns into 4 blocks
v_inputs = {}
v_tabs = st.tabs(["Signal Block A", "Signal Block B", "Signal Block C", "Signal Block D"])

for i, tab in enumerate(v_tabs):
    with tab:
        v_cols = st.columns(7)
        for j in range(7):
            v_num = (i * 7) + j + 1
            v_inputs[f'V{v_num}'] = v_cols[j].number_input(f"V{v_num}", value=0.0, format="%.3f")

# --- 8. PREDICTION LOGIC ---
if st.button("INITIATE SECURITY SCAN"):
    with st.spinner("Analyzing digital signatures..."):
        # Scale inputs
        scaled_time = scaler.transform(np.array([[time_val]]))[0][0]
        scaled_amount = scaler.transform(np.array([[amount]]))[0][0]

        # Build DataFrame for XGBoost
        data_dict = {f'V{i}': [v_inputs[f'V{i}']] for i in range(1, 29)}
        data_dict['Scaled_Amount'] = [scaled_amount]
        data_dict['Scaled_Time'] = [scaled_time]
        features_df = pd.DataFrame(data_dict)

        # Execution
        if engine_choice == "XGBoost High-Speed":
            dmatrix = xgb.DMatrix(features_df)
            prediction = xgb_model.predict(dmatrix)[0]
        else:
            prediction = ann_model.predict(features_df.values, verbose=0)[0][0]

        # --- 9. RESULTS DISPLAY ---
        st.markdown("### Security Verdict")
        risk_score = float(prediction)
        
        if risk_score > 0.5:
            st.markdown(f"""
                <div class="fraud-alert">
                    🚨 SECURITY ALERT: FRAUD DETECTED<br>
                    <span style="font-size: 18px;">Risk Probability: {risk_score:.2%}</span>
                </div>
                """, unsafe_allow_html=True)
            st.error(f"The {engine_choice} engine detected patterns matching known fraud signatures.")
        else:
            st.markdown(f"""
                <div class="success-card">
                    <h2 style="margin:0;">✨ All Clear!</h2>
                    <p style="font-size: 18px; margin: 10px 0;">Verification Score: {(1-risk_score):.2%}</p>
                </div>
                """, unsafe_allow_html=True)
            st.success(f"Verified by {engine_choice}: No high-risk anomalies detected.")

st.markdown("---")
st.caption("FinGuard Elite Intelligence Hub | Developed by Risper Wacu | © 2024 All Rights Reserved")