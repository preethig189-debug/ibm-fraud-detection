import streamlit as st
import pandas as pd
import hashlib
import re

st.set_page_config(
    page_title="PrivacyGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------- PAGE DESIGN ----------
st.title("🛡️ PrivacyGuard AI")
st.subheader("Privacy-Preserving AI Fraud Detection")
st.write(
    "Detect suspicious payment patterns while keeping "
    "personal identifiers away from the risk detection model."
)

st.info("Demonstration only. Use fictional transaction data.")

# ---------- PRIVACY FUNCTIONS ----------
def mask_name(name):
    if not name.strip():
        return "MASKED"
    return name[0].upper() + "***"

def tokenize_upi(upi):
    # Stable pseudonymous token for demonstration.
    # Do not use this unsalted hash approach in production.
    return "USER_" + hashlib.sha256(
        upi.strip().lower().encode()
    ).hexdigest()[:10]

def mask_phone(phone):
    digits = re.sub(r"\D", "", phone)
    return "******" + digits[-4:] if digits else "MASKED"

# ---------- FRAUD DETECTOR ----------
def detect_fraud(amount, recent_count, new_device):
    score = 0
    reasons = []

    if amount >= 10000:
        score += 35
        reasons.append("Amount exceeds the demo threshold.")

    if recent_count >= 5:
        score += 35
        reasons.append("High transaction frequency.")

    if new_device:
        score += 30
        reasons.append("A new device was detected.")

    score = min(score, 100)

    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, reasons

# ---------- SIDEBAR ----------
st.sidebar.header("About this project")
st.sidebar.write("Privacy layer → Feature analysis → Risk score")
st.sidebar.write("Prototype version 1.0")

# ---------- TRANSACTION INPUT ----------
st.header("1. Enter a sample transaction")

with st.form("payment_form"):
    name = st.text_input("Customer name", "Rahul")
    upi = st.text_input("UPI ID", "rahul@example")
    phone = st.text_input("Phone number", "9876543210")

    amount = st.number_input(
        "Transaction amount (₹)",
        min_value=1,
        max_value=10000000,
        value=25000
    )

    recent_count = st.number_input(
        "Transactions in the recent time window",
        min_value=1,
        max_value=1000,
        value=8
    )

    new_device = st.checkbox("New device detected")

    submitted = st.form_submit_button("🔍 Analyse Transaction")

if submitted:
    # ---------- PRIVACY LAYER ----------
    masked_customer = mask_name(name)
    tokenized_user = tokenize_upi(upi)
    masked_number = mask_phone(phone)

    st.header("2. Privacy protection")

    privacy_data = pd.DataFrame([
        {
            "Field": "Customer name",
            "Original": name if name else "(empty)",
            "Protected": masked_customer
        },
        {
            "Field": "UPI ID",
            "Original": upi if upi else "(empty)",
            "Protected": tokenized_user
        },
        {
            "Field": "Phone",
            "Original": phone if phone else "(empty)",
            "Protected": masked_number
        }
    ])

    st.dataframe(privacy_data, hide_index=True, use_container_width=True)

    st.success(
        "The detector receives transaction features, "
        "not the original name, UPI ID or phone number."
    )

    # ---------- FEATURE-ONLY ANALYSIS ----------
    # Personal identifiers are deliberately not passed here.
    score, level, reasons = detect_fraud(
        amount, recent_count, new_device
    )

    st.header("3. Fraud analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk score", f"{score}/100")
    col2.metric("Risk category", level)
    col3.metric("Transaction amount", f"₹{amount:,.0f}")

    st.progress(score / 100)

    if level == "HIGH":
        st.error("⚠️ High-risk transaction: review recommended.")
    elif level == "MEDIUM":
        st.warning("🟠 Medium-risk transaction: further review recommended.")
    else:
        st.success("🟢 Low-risk under the current demo rules.")

    st.subheader("4. Why was this score assigned?")

    if reasons:
        for reason in reasons:
            st.write("•", reason)
    else:
        st.write("No configured risk rules were triggered.")

    st.subheader("5. Protected transaction summary")

    summary = pd.DataFrame([{
        "User token": tokenized_user,
        "Amount": amount,
        "Recent transaction count": recent_count,
        "New device": "Yes" if new_device else "No",
        "Risk score": score,
        "Risk category": level
    }])

    st.dataframe(summary, hide_index=True, use_container_width=True)

    st.caption(
        "Important: This is a rule-based educational prototype, "
        "not a trained ML model or a calibrated fraud probability. "
        "The thresholds are illustrative and must be validated "
        "before real-world use."
    )

# ---------- SAMPLE TEST CASES ----------
st.divider()
st.header("6. Try sample scenarios")

examples = pd.DataFrame([
    {"Scenario": "Normal example", "Amount": 500,
     "Recent transactions": 1, "New device": "No"},
    {"Scenario": "Large payment", "Amount": 15000,
     "Recent transactions": 2, "New device": "No"},
    {"Scenario": "Rapid transactions", "Amount": 500,
     "Recent transactions": 6, "New device": "No"},
    {"Scenario": "Multiple risk signals", "Amount": 25000,
     "Recent transactions": 8, "New device": "Yes"}
])

st.dataframe(examples, hide_index=True, use_container_width=True)