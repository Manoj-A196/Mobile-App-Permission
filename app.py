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

# --------------------------------------------------
# TEAL / GREENISH-BLUE THEME (CUSTOM CSS)
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #f0fdfa; }
h1, h2, h3 { color: #0f766e; }
.stButton>button {
    background-color: #0f766e;
    color: white;
    border-radius: 8px;
}
.stButton>button:hover { background-color: #115e59; }
.stDataFrame { border: 1px solid #99f6e4; }
div[data-testid="metric-container"] {
    background-color: #ecfeff;
    border: 1px solid #67e8f9;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🔐 Mobile App Permission Analysis System")
st.caption("Advanced Permission Risk Detection for Mobile Applications")

st.divider()

# --------------------------------------------------
# SESSION STATE (HISTORY)
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

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
    ["Camera", "Location", "Contacts", "Microphone", "Storage", "SMS"]
)

# --------------------------------------------------
# PERMISSION WEIGHTS & EXPLANATIONS
# --------------------------------------------------
permission_info = {
    "Camera": (20, "Can capture images and videos without user awareness"),
    "Location": (20, "Tracks real-time physical location"),
    "Contacts": (25, "Accesses personal contact list"),
    "Microphone": (20, "Can record audio in the background"),
    "Storage": (10, "Reads and writes local files"),
    "SMS": (30, "Can read private messages and OTPs")
}

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
if st.button("▶ Analyze Permissions"):

    total_score = 0
    explanations = []

    for p in permissions:
        score, reason = permission_info[p]
        total_score += score
        explanations.append(f"• **{p}** – {reason}")

    # Risk Level & Recommendation
    if total_score >= 60:
        risk = "High 🔴"
        recommendation = "❌ Do NOT allow all permissions. Review and deny unnecessary ones."
    elif total_score >= 30:
        risk = "Medium 🟠"
        recommendation = "⚠️ Allow only essential permissions."
    else:
        risk = "Low 🟢"
        recommendation = "✅ Permissions are mostly safe."

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------
    st.subheader("📊 Analysis Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Privacy Risk Score", f"{total_score}/100")
        st.write(f"**Risk Level:** {risk}")
        st.write(f"**Recommendation:** {recommendation}")

    with col2:
        st.markdown("### 🔍 Permission Explanations")
        if explanations:
            for e in explanations:
                st.write(e)
        else:
            st.write("• No permissions selected.")

    st.divider()

    # --------------------------------------------------
    # GRAPH (NUMERIC, GUARANTEED VISIBLE)
    # --------------------------------------------------
    st.subheader("📈 Permission Risk Distribution")

    graph_df = pd.DataFrame({
        "Risk Score": [
            permission_info[p][0] if p in permissions else 0
            for p in permission_info.keys()
        ]
    }, index=list(permission_info.keys()))

    st.bar_chart(graph_df)

    st.caption("Higher bars indicate higher privacy impact of permissions.")

    st.divider()

    # --------------------------------------------------
    # SAVE TO HISTORY
    # --------------------------------------------------
    st.session_state.history.append({
        "App": app_name,
        "Permissions": ", ".join(permissions) if permissions else "None",
        "Risk Score": total_score,
        "Risk Level": risk
    })

# --------------------------------------------------
# HISTORY TABLE
# --------------------------------------------------
if st.session_state.history:
    st.subheader("🕘 Analysis History")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption("Academic Project – Mobile App Permission Analysis System")
