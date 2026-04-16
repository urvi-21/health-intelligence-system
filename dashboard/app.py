import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(layout="wide")

# -------- DB CONNECTION --------
engine = create_engine(
    "postgresql://postgres:postgres123@127.0.0.1:5434/health_db"
)

# -------- LOAD DATA --------
df = pd.read_sql("SELECT * FROM predictions", engine)

if df.empty:
    st.warning("No data available. Run Airflow pipeline first.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# -------- USER SELECTION --------
user_id = st.selectbox("Select User", df["user_id"].unique())

df_user_raw = df[df["user_id"] == user_id].copy()

df_user = (
    df_user_raw.groupby("date")
    .mean(numeric_only=True)
    .reset_index()
)

latest = df_user.iloc[-1]

# -------- SMOOTH TREND --------
df_user["smooth_health"] = (
    df_user["health_score"]
    .rolling(5, min_periods=1)
    .mean()
)

# -------- UI STYLE --------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}
.block-container { padding: 2rem 3rem; }
</style>
""", unsafe_allow_html=True)

st.title("Health Intelligence System")
st.caption("Understand your health. Act before risk rises.")

#========================================================

score = latest["health_score"]

if score < 40:
    status = "High Risk"
    message = "Your health condition needs immediate attention."
    bg_color = "rgba(255,0,0,0.15)"
elif score < 70:
    status = "Moderate Risk"
    message = "Your health is slightly unstable today."
    bg_color = "rgba(255,165,0,0.15)"
else:
    status = "Healthy"
    message = "You are in a stable condition."
    bg_color = "rgba(0,255,150,0.15)"

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {bg_color}, rgba(255,255,255,0.03));
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.08);
">
""", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(f"## {message}")
    st.markdown(f"### {status}")

    if len(df_user) > 1:
        prev = df_user.iloc[-2]
        delta = score - prev["health_score"]

        if delta > 0:
            st.markdown(f"🟢 Improved by {round(delta,1)} since yesterday")
        else:
            st.markdown(f"🔴 Dropped by {round(abs(delta),1)} since yesterday")

with col2:
    st.markdown(f"""
        <div style='font-size:42px; font-weight:700'>
            {round(score,1)}
        </div>
        <div style='opacity:0.7'>Health Score</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================

st.markdown("### Recommended Actions")

actions = []

if latest["avg_sleep"] < 6:
    actions.append("🔴 Improve sleep to at least 7–8 hours")

if latest["avg_stress"] > 60:
    actions.append("🟠 Reduce stress through relaxation")

if latest["avg_steps"] < 4000:
    actions.append("🟢 Increase daily activity")

if not actions:
    actions.append("🟢 Maintain current healthy routine")

for a in actions:
    st.write(f"• {a}")

st.markdown("---")

# =========================================================

st.markdown("### Tomorrow Risk Prediction")

if len(df_user) > 3:
    recent = df_user.tail(3)
    trend = recent["health_score"].iloc[-1] - recent["health_score"].iloc[0]

    if trend < -2:
        st.error("⚠️ Risk likely to increase tomorrow if this trend continues")
    elif trend > 2:
        st.success("📈 Health improving — risk may decrease tomorrow")
    else:
        st.info("➖ Stable trend — no major change expected")
else:
    st.info("Not enough data for prediction.")

st.markdown("---")

# =========================================================

st.markdown("### Weekly Summary")

recent_week = df_user.tail(7)

avg_score = recent_week["health_score"].mean()
min_score = recent_week["health_score"].min()
max_score = recent_week["health_score"].max()

colW1, colW2, colW3 = st.columns(3)

colW1.metric("Avg Score", round(avg_score,1))
colW2.metric("Best Day", round(max_score,1))
colW3.metric("Lowest Day", round(min_score,1))

st.markdown("---")

# =========================================================

st.markdown("### Health Trend (Last Few Days)")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_user["date"],
    y=df_user["smooth_health"],
    fill='tozeroy',
    mode='lines',
    line=dict(width=4, color="#60a5fa")
))

fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# 🧠 WHY (CLEANED)
# =========================================================

st.markdown("### Key Factors Affecting Your Health")

reasons = []

if latest["avg_stress"] > 60:
    reasons.append("Stress levels are high")

if latest["avg_sleep"] < 6:
    reasons.append("Sleep duration is insufficient")

if latest["avg_hr"] > 90:
    reasons.append("Heart rate is elevated")

if latest["avg_steps"] < 4000:
    reasons.append("Physical activity is low")

if len(df_user) > 3:
    recent = df_user.tail(3)

    if recent["avg_sleep"].iloc[-1] < recent["avg_sleep"].iloc[0]:
        reasons.append("Sleep has decreased recently")

    if recent["health_score"].iloc[-1] < recent["health_score"].iloc[0]:
        reasons.append("Health trend is declining")

# show only top 3
for r in reasons[:3] or ["All vitals are stable"]:
    st.write(f"• {r}")