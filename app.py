import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Mobile App Permission Analysis System",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Mobile App Permission Analysis System")
st.caption("Permission Analysis → Risk Detection → Visualization")

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
st.subheader("📱 Application Permission Input")

app_name = st.selectbox(
    "Select Mobile Application",
    ["Instagram", "WhatsApp", "Facebook", "Google Maps", "Snapchat"]
)

permissions = st.multiselect(
    "Select Permissions Requested by App",
    [
        "Camera",
        "Location",
        "Contacts",
        "Microphone",
        "Storage",
        "SMS"
    ]
)

st.divider()

# --------------------------------------------------
# PERMISSION CATEGORIES
# --------------------------------------------------
normal_permissions = ["Storage"]
sensitive_permissions = ["Camera", "Location", "Microphone"]
critical_permissions = ["Contacts", "SMS"]

# --------------------------------------------------
# ANALYSIS LOGIC
# --------------------------------------------------
def analyze_permissions(selected):
    normal = len([p for p in selected if p in normal_permissions])
    sensitive = len([p for p in selected if p in sensitive_permissions])
    critical = len([p for p in selected if p in critical_permissions])

    if critical > 0:
        risk = "High 🔴"
    elif sensitive > 0:
        risk = "Medium 🟠"
    else:
        risk = "Low 🟢"

    return normal, sensitive, critical, risk

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
if st.button("▶ Analyze Permissions"):

    normal_count, sensitive_count, critical_count, risk_level = analyze_permissions(permissions)

    st.subheader("📊 Analysis Result")

    st.write(f"**Application Name:** {app_name}")
    st.write(f"**Permissions Requested:** {', '.join(permissions) if permissions else 'None'}")
    st.write(f"**Risk Level:** {risk_level}")

    st.divider()

    # --------------------------------------------------
    # GRAPH SECTION
    # --------------------------------------------------
    st.subheader("📈 Permission Risk Visualization")

    graph_df = pd.DataFrame({
        "Permission Type": ["Normal", "Sensitive", "Critical"],
        "Count": [normal_count, sensitive_count, critical_count]
    }).set_index("Permission Type")

    st.bar_chart(graph_df)

    st.caption("Higher critical permissions indicate higher privacy risk")

    st.divider()

    # --------------------------------------------------
    # SECURITY MESSAGE
    # --------------------------------------------------
    if "High" in risk_level:
        st.error("⚠️ This application requests critical permissions. User privacy may be at risk.")
    elif "Medium" in risk_level:
        st.warning("⚠️ This application requests sensitive permissions. Review carefully.")
    else:
        st.success("✅ This application requests minimal permissions and is relatively safe.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption("Academic Project – Mobile App Permission Analysis System")
