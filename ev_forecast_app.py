import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EV Demand Planner — Malaysia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, header, footer, [data-testid="collapsedControl"] { visibility: hidden; height: 0; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] { background: #f4feea; }

.block-container {
    padding-top: 0.3rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 1200px !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
}

h1, h2, h3 { font-family: 'Georgia', serif; color: #1a2e0a; }
p, li { font-size: 12px; line-height: 1.5; color: #1e293b; }

.bento-card {
    background: white;
    border: none;
    border-radius: 10px;
    padding: 8px 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,.05);
    margin-bottom: 6px;
    text-align: center;
}
.metric-label {
    font-size: 9px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #64748b;
    margin-bottom: 2px !important;
    margin-top: 0 !important;
    text-align: center;
    line-height: 1.2;
}
.metric-value {
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #236708 !important;
    line-height: 1.1 !important;
    text-align: center;
    margin: 1px 0 2px 0 !important;
    display: block;
}

.badge-high { background:#236708; color:white; padding:2px 8px; border-radius:5px; font-weight:700; font-size:10px; display:inline-block; }
.badge-med  { background:#f59e0b; color:white; padding:2px 8px; border-radius:5px; font-weight:700; font-size:10px; display:inline-block; }
.badge-low  { background:#ef4444; color:white; padding:2px 8px; border-radius:5px; font-weight:700; font-size:10px; display:inline-block; }

[data-testid="stTabs"] button { font-size: 12px !important; font-weight: 700 !important; font-family: Georgia, serif !important; }
[data-testid="stTabs"] { margin-top: -6px !important; }

[data-testid="stCheckbox"] label {
    font-size: 11.5px !important;
    color: #1e293b !important;
    line-height: 1.4 !important;
    font-weight: 500 !important;
}
[data-testid="stCheckbox"] { margin-bottom: -4px !important; }

[data-testid="stSlider"] label { font-size: 11.5px !important; color: #374151 !important; font-weight: 500 !important; }
div[data-testid="stSlider"] label, div[data-testid="stSlider"] label p {
    font-size: 11.5px !important; font-weight: 500 !important; color: #374151 !important;
}
[data-testid="stSlider"] { margin-top: 2px !important; }

div[data-testid="stCheckbox"] label p, div[data-testid="stCheckbox"] label {
    font-size: 11.5px !important; font-weight: 500 !important;
    color: #1e293b !important; line-height: 1.4 !important;
}

.stDataFrame th, .stDataFrame td { font-size: 11px !important; }

.stSelectbox label { font-size: 12px !important; font-weight: 900 !important; color: #1a2e0a !important; }
[data-testid="stSelectbox"] > div > div { background: white !important; border-radius: 8px !important; font-weight: 700 !important; }
[data-testid="stSelectbox"] > div > div > div { background: white !important; color: #1a2e0a !important; font-weight: 700 !important; }

[data-testid="stHorizontalBlock"] { gap: 6px !important; }

/* ── RED BUTTON ── */
.stButton > button,
.stButton > button:focus,
.stButton > button:active,
.stButton > button:focus:not(:active) {
    background-color: #dc2626 !important;
    background-image: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #b91c1c !important;
    background-image: none !important;
    color: #ffffff !important;
    border: none !important;
}
.stButton > button p, .stButton > button span {
    color: #ffffff !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("final_ev_demand_forecast.csv")
    df["month_start"] = pd.to_datetime(df["month_start"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Cannot find final_ev_demand_forecast.csv — place it in the same folder.")
    st.stop()

STATES = sorted(df["state"].unique().tolist())
HIST   = df[df["period"] == "Historical"]
FCAST  = df[(df["period"] == "XGBoost Forecast") & (df["month_start"] >= "2025-10-01")]

EVCS_LINKS = {
    "Johor":             "https://www.google.com/maps/search/EV+charging+station+Johor+Malaysia",
    "Kedah":             "https://www.google.com/maps/search/EV+charging+station+Kedah+Malaysia",
    "Kelantan":          "https://www.google.com/maps/search/EV+charging+station+Kelantan+Malaysia",
    "Melaka":            "https://www.google.com/maps/search/EV+charging+station+Melaka+Malaysia",
    "Negeri Sembilan":   "https://www.google.com/maps/search/EV+charging+station+Negeri+Sembilan+Malaysia",
    "Pahang":            "https://www.google.com/maps/search/EV+charging+station+Pahang+Malaysia",
    "Perak":             "https://www.google.com/maps/search/EV+charging+station+Perak+Malaysia",
    "Perlis":            "https://www.google.com/maps/search/EV+charging+station+Perlis+Malaysia",
    "Pulau Pinang":      "https://www.google.com/maps/search/EV+charging+station+Pulau+Pinang+Malaysia",
    "Sabah":             "https://www.google.com/maps/search/EV+charging+station+Sabah+Malaysia",
    "Sarawak":           "https://www.google.com/maps/search/EV+charging+station+Sarawak+Malaysia",
    "Selangor":          "https://www.google.com/maps/search/EV+charging+station+Selangor+Malaysia",
    "Terengganu":        "https://www.google.com/maps/search/EV+charging+station+Terengganu+Malaysia",
    "W.P. Kuala Lumpur": "https://www.google.com/maps/search/EV+charging+station+Kuala+Lumpur+Malaysia",
    "W.P. Labuan":       "https://www.google.com/maps/search/EV+charging+station+Labuan+Malaysia",
    "W.P. Putrajaya":    "https://www.google.com/maps/search/EV+charging+station+Putrajaya+Malaysia",
}

INFRA = {
    "W.P. Kuala Lumpur":  ("High",       "1,192 ports · dense network · good coverage"),
    "Selangor":           ("High",       "1,276 ports · highest total · good coverage"),
    "Pulau Pinang":       ("Medium",     "Moderate coverage · growing network"),
    "Johor":              ("Medium",     "Good coverage in JB · expanding"),
    "Perak":              ("Medium",     "Moderate · improving"),
    "Melaka":             ("Medium",     "Compact state · reasonable coverage"),
    "Negeri Sembilan":    ("Medium",     "Moderate · near KL corridor"),
    "Kedah":              ("Low-Medium", "Limited · mainly highway corridors"),
    "Sabah":              ("Low-Medium", "Limited · concentrated in Kota Kinabalu"),
    "Sarawak":            ("Low-Medium", "Limited · mainly Kuching area"),
    "Pahang":             ("Low",        "Very limited · mainly highway rest areas"),
    "Terengganu":         ("Low",        "Limited but 84% DC ratio"),
    "Kelantan":           ("Low",        "Sparse · slowest EV adoption state"),
    "Perlis":             ("Low",        "Very limited · smallest state"),
    "W.P. Putrajaya":     ("Low-Medium", "Government area · some workplace chargers"),
    "W.P. Labuan":        ("Low",        "Very limited · island territory"),
}

import base64 as _b64, os as _os
def _logo_tag():
    for _p in ["logo.png", "static/logo.png"]:
        if _os.path.exists(_p):
            with open(_p, "rb") as _f:
                _b = _b64.b64encode(_f.read()).decode()
            return f'<img src="data:image/png;base64,{_b}" style="width:40px;height:40px;object-fit:contain;" />'
    return '<span style="font-size:20px;">⚡</span>'

# ── Header ─────────────────────────────────────────────
h1, h2 = st.columns([2, 1])
with h1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
        <div style="display:flex;align-items:center;justify-content:center;width:60px;height:60px;">{_logo_tag()}</div>
        <div>
            <div style="font-size:20px;font-weight:900;color:#1a2e0a;font-family:Georgia,serif;">Malaysia EV Demand Planner</div>
            <div style="text-transform:uppercase;font-weight:700;color:#5C9545;font-size:10px;letter-spacing:.1em;">XGBoost Machine Learning Forecast</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown('<p style="font-size:12px;font-weight:900;color:#1a2e0a;margin:0 0 2px 0;">📍 Select Your State</p>', unsafe_allow_html=True)
    selected_state = st.selectbox("", STATES, index=STATES.index("Selangor"), label_visibility="collapsed")

# ── Compute values ─────────────────────────────────────
sf    = FCAST[FCAST["state"] == selected_state]
tot   = int(sf["ev_total"].sum())
v0    = int(sf["ev_total"].iloc[0])  if len(sf) > 0 else 0
v1    = int(sf["ev_total"].iloc[-1]) if len(sf) > 0 else 0
gpct  = round((v1 - v0) / max(v0, 1) * 100, 1)
lvl, note = INFRA.get(selected_state, ("Low", "No data"))
url   = EVCS_LINKS.get(selected_state, "https://www.google.com/maps/search/EV+charging+Malaysia")
ports = int(HIST[HIST["state"] == selected_state]["cum_ports"].max())
evs_per_port = round(tot / max(ports, 1), 0)

badge = (
    '<span class="badge-high">HIGH</span>' if lvl == "High" else
    '<span class="badge-med">MEDIUM</span>' if lvl in ["Medium", "Low-Medium"] else
    '<span class="badge-low">LOW</span>'
)

# ── session state ──────────────────────────────────────
if "readiness_clicked" not in st.session_state:
    st.session_state.readiness_clicked = False

# ── Tabs ───────────────────────────────────────────────
tab_buyer, tab_policy = st.tabs(["🚗  EV Buyer Assessment", "🏛️  Policy Maker Strategic View"])

# ════════════════════════════════════════════════════════
# TAB 1 — EV BUYER
# ════════════════════════════════════════════════════════
with tab_buyer:

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="bento-card"><p class="metric-label">3-Year EV Forecast</p><p class="metric-value">{tot:,}</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">Oct 2025 – Sep 2028</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="bento-card"><p class="metric-label">Current Charger Ports</p><p class="metric-value">{ports:,}</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">as of Sep 2025</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="bento-card"><p class="metric-label">Forecast Growth</p><p class="metric-value">{gpct:+.1f}%</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">Oct 2025 → Sep 2028</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="bento-card"><p class="metric-label">Local Readiness</p><div style="margin:3px 0 2px 0;">{badge}</div><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">{lvl} infrastructure</p></div>', unsafe_allow_html=True)

    # ── col_l narrower, col_r wider, medium gap ──
    col_l, col_r = st.columns([1, 1.15], gap="medium")

    with col_l:
        if lvl == "High":
            verdict_icon = "✅"; verdict_title = f"Great time to buy an EV in {selected_state}"
            verdict_color = "#f0fdf4"; verdict_border = "#86efac"
        elif lvl in ["Medium", "Low-Medium"]:
            verdict_icon = "⚠️"; verdict_title = "Good — but check your area first"
            verdict_color = "#fffbeb"; verdict_border = "#fcd34d"
        else:
            verdict_icon = "🔴"; verdict_title = "Plan carefully before buying"
            verdict_color = "#fff1f0"; verdict_border = "#fca5a5"

        st.markdown(f"""
        <div class="bento-card" style="background:{verdict_color};border-color:{verdict_border};text-align:left;padding:8px 12px;">
            <p style="font-size:12px;font-weight:800;margin:0 0 3px 0;color:#1a2e0a;">{verdict_icon} {verdict_title}</p>
            <p style="color:#475569;margin:0 0 5px 0;font-size:11px;line-height:1.7;font-weight:300;">
                Infrastructure is <b style="font-weight:600;">{lvl.lower()}</b> — {note}.<br>
                EV demand forecast to grow <b style="font-weight:600;">{gpct:+.1f}%</b> from Oct 2025 to Sep 2028.
            </p>
            <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:6px 10px;">
                <p style="margin:0 0 2px 0;font-size:11px;font-weight:600;color:#1a2e0a;">📍 Nearest Charging Stations</p>
                <p style="margin:0;color:#475569;font-size:11px;font-weight:300;line-height:1.7;">
                    <b style="font-weight:600;">State:</b> {selected_state} &nbsp;·&nbsp;
                    <b style="font-weight:600;">Ports:</b> {ports:,} &nbsp;·&nbsp;
                    <b style="font-weight:600;">Level:</b> {lvl}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Google Maps button — same width as card above
        st.markdown(f'''
        <a href="{url}" target="_blank" style="display:block;text-align:center;background:#1a4d08;
           color:white;font-weight:700;font-size:11px;padding:7px 12px;border-radius:8px;
           text-decoration:none;margin-top:2px;">
            🗺️ Find Charging Stations on Google Maps
        </a>''', unsafe_allow_html=True)

    # ── RIGHT COLUMN ───────────────────────────────────
    with col_r:
        st.markdown("<p style='font-size:14px;font-weight:900;margin:0 0 4px 0;color:#1a2e0a;'>🧮 Personal EV Readiness Check</p>", unsafe_allow_html=True)

        # checkboxes | score + button + result
        c_checks, c_score = st.columns([1, 1.15], gap="small")

        with c_checks:
            has_home  = st.checkbox("Home parking for charger")
            near_pub  = st.checkbox("EVCS within 5 km")
            budget_ok = st.checkbox("Budget above RM 50,000 for EV ownership")
            commute   = st.slider("Daily commute — round trip (km)", 10, 300, 65, step=5)

        # ── Score calculation ──
        score = 0
        if has_home:  score += 35
        if near_pub:  score += 20
        if budget_ok: score += 20
        if commute <= 80:    score += 25
        elif commute <= 150: score += 12
        if lvl == "High":     score = min(score + 10, 100)
        elif lvl == "Medium": score = min(score + 5,  100)
        verdict_txt = ('🎉 Prime candidate!' if score >= 75 else '👍 Good potential.' if score >= 50 else '⚡ Plan carefully.')

        # ── Decision content ──
        if score >= 75:
            dec_icon = "🟢"; dec_title = "Yes — Go ahead and buy an EV!"
            dec_color = "#f0fdf4"; dec_border = "#86efac"
            dec_body = (
                f"Your profile suits EV ownership in <b style='font-weight:600;'>{selected_state}</b>. "
                f"Home charging, nearby EVCS, and a <b style='font-weight:600;'>{commute} km</b> commute — "
                f"infrastructure is <b style='font-weight:600;'>{lvl.lower()}</b> with <b style='font-weight:600;'>{gpct:+.1f}%</b> forecast growth."
            )
        elif score >= 50:
            dec_icon = "🟡"; dec_title = "Maybe — Prepare before you buy"
            dec_color = "#fffbeb"; dec_border = "#fcd34d"
            dec_body = (
                f"EV ownership in <b style='font-weight:600;'>{selected_state}</b> is possible but needs preparation. "
                + (f"Install a home charger. " if not has_home else "")
                + (f"Your <b style='font-weight:600;'>{commute} km</b> commute needs frequent top-ups. " if commute > 80 else "")
                + (f"Verify nearby EVCS. " if not near_pub else "")
                + "Plan your charging routine first."
            )
        else:
            dec_icon = "🔴"; dec_title = "Not yet — Address key gaps first"
            dec_color = "#fff1f0"; dec_border = "#fca5a5"
            dec_body = (
                f"EV ownership in <b style='font-weight:600;'>{selected_state}</b> is challenging now. "
                + (f"No home charging — the most critical gap. " if not has_home else "")
                + (f"A <b style='font-weight:600;'>{commute} km</b> commute is high for current range. " if commute > 150 else "")
                + (f"Limited public EVCS nearby. " if not near_pub else "")
                + "Resolve these gaps before purchasing."
            )

        with c_score:
            # Score + bar + verdict label
            st.markdown(f"""
            <div style="text-align:center;padding:2px 4px 4px 4px;">
                <p style="font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#4a7c2f;margin:0 0 1px 0;">Readiness Score</p>
                <p style="font-size:22px;font-weight:900;color:#236708;line-height:1;margin:0 0 3px 0;">{score}%</p>
                <div style="background:#86efac;border-radius:99px;height:6px;margin-bottom:3px;">
                    <div style="background:#236708;border-radius:99px;height:6px;width:{score}%;"></div>
                </div>
                <p style="font-size:10px;font-style:italic;color:#475569;margin:0 0 5px 0;">{verdict_txt}</p>
            </div>
            """, unsafe_allow_html=True)

            # Red button — full width of c_score
            if st.button("✅ Check My Readiness", use_container_width=True):
                st.session_state.readiness_clicked = True

            # Decision result — same text style as left card
            if st.session_state.readiness_clicked:
                st.markdown(f"""
                <div style="background:{dec_color};border:1.5px solid {dec_border};border-radius:8px;
                            padding:8px 10px;margin-top:4px;">
                    <p style="font-size:12px;font-weight:800;color:#1a2e0a;margin:0 0 3px 0;">{dec_icon} {dec_title}</p>
                    <p style="font-size:11px;color:#475569;margin:0;line-height:1.7;font-weight:300;">{dec_body}</p>
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 2 — POLICY MAKER
# ════════════════════════════════════════════════════════
with tab_policy:

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(f'<div class="bento-card"><p class="metric-label">Current Ports</p><p class="metric-value">{ports:,}</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">as of Sep 2025</p></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="bento-card"><p class="metric-label">3-Year EV Forecast</p><p class="metric-value">{tot:,}</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">Oct 2025 – Sep 2028</p></div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f'<div class="bento-card"><p class="metric-label">EVs per Port</p><p class="metric-value">{int(evs_per_port):,}</p><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">infrastructure gap ratio</p></div>', unsafe_allow_html=True)
    with p4:
        p_badge = (
            '<span class="badge-low">HIGH PRIORITY</span>' if (evs_per_port > 500 or lvl == "Low") else
            '<span class="badge-med">MED PRIORITY</span>'  if (evs_per_port > 200 or lvl == "Low-Medium") else
            '<span class="badge-high">STABLE</span>'
        )
        st.markdown(f'<div class="bento-card"><p class="metric-label">Deployment Priority</p><div style="margin:3px 0 2px 0;">{p_badge}</div><p style="font-size:9px;color:#64748b;text-align:center;margin:0;">{selected_state}</p></div>', unsafe_allow_html=True)

    col_main, col_side = st.columns([1.6, 1], gap="small")

    with col_main:
        if evs_per_port > 500 or lvl == "Low":
            pa_title = "🔴 HIGH PRIORITY — Immediate investment needed"
            pa_color = "#fff1f0"; pa_border = "#fca5a5"
            pa_text  = f"{selected_state} has {ports:,} charger ports for a 3-year forecast of {tot:,} EVs — a ratio of {int(evs_per_port):,} EVs per port. Urgent EVCS deployment is required to prevent infrastructure bottlenecks."
        elif evs_per_port > 200 or lvl == "Low-Medium":
            pa_title = "🟡 MEDIUM PRIORITY — Planned expansion recommended"
            pa_color = "#fffbeb"; pa_border = "#fcd34d"
            pa_text  = f"{selected_state} has {ports:,} ports for {tot:,} forecast EVs (ratio: {int(evs_per_port):,} EVs/port). Expansion should be planned within 12–18 months."
        else:
            pa_title = "🟢 LOWER PRIORITY — Maintain and monitor"
            pa_color = "#f0fdf4"; pa_border = "#86efac"
            pa_text  = f"{selected_state} has adequate infrastructure — {ports:,} ports for {tot:,} forecast EVs. Focus on improving the DC fast charger ratio and filling coverage gaps."

        st.markdown(f"""
        <div class="bento-card" style="background:{pa_color};border-color:{pa_border};text-align:left;padding:8px 12px;margin-bottom:6px;">
            <p style="font-size:12px;font-weight:800;color:#1a2e0a;margin:0 0 2px 0;">Infrastructure Gap Analysis — {selected_state}</p>
            <p style="color:#64748b;font-size:10px;margin:0 0 5px 0;">Based on XGBoost Demand Forecasting (Oct 2025 – Sep 2028)</p>
            <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:7px 10px;">
                <p style="margin:0 0 2px 0;font-weight:700;color:#1e293b;font-size:11px;">{pa_title}</p>
                <p style="margin:0;color:#475569;font-size:11px;">{pa_text}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:11px;font-weight:700;margin:2px 0 3px 0;'>📊 National Priority Ranking — All 16 States</p>", unsafe_allow_html=True)
        gap_rows = []
        for s in STATES:
            sp  = int(HIST[HIST["state"] == s]["cum_ports"].max())
            st_ = int(FCAST[FCAST["state"] == s]["ev_total"].sum())
            sr  = round(st_ / max(sp, 1), 0)
            sl  = INFRA.get(s, ("Unknown",""))[0]
            if sr > 500 or sl == "Low":            spr = "🔴 High"
            elif sr > 200 or sl == "Low-Medium":   spr = "🟡 Medium"
            else:                                  spr = "🟢 Lower"
            gap_rows.append({"State": s, "Ports": f"{sp:,}", "3yr EV Forecast": f"{st_:,}", "EVs / Port": f"{int(sr):,}", "Priority": spr})
        gap_df = pd.DataFrame(gap_rows).sort_values("EVs / Port", ascending=False).reset_index(drop=True)
        st.dataframe(gap_df, use_container_width=True, hide_index=True, height=220)

    with col_side:
        st.markdown(f'''<a href="{url}" target="_blank" style="display:block;text-align:center;background:#1a4d08;color:white;font-weight:700;font-size:11px;padding:7px 12px;border-radius:8px;text-decoration:none;margin-top:2px;">🗺️ View EVCS in {selected_state} on Google Maps</a>''', unsafe_allow_html=True)
        st.markdown("""
        <div class="bento-card" style="padding:8px 12px;text-align:left;margin-top:6px;">
            <p class="metric-label" style="text-align:left;margin-bottom:4px;">Recommended Deployment Venues</p>
            <p style="font-size:11px;line-height:1.8;margin:0;">
                🛍️ Shopping malls<br>
                ⛽ Petrol station forecourts<br>
                🏨 Hotels &amp; resorts<br>
                🏢 Office buildings<br>
                🅿️ Park &amp; ride hubs
            </p>
        </div>
        """, unsafe_allow_html=True)
