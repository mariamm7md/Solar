"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         SolarIQ Egypt  —  AI-Powered Solar Intelligence Platform             ║
║         Version 2.0  |  Cloud-Ready  |  Premium Design                       ║
║                                                                              ║
║  HOW TO RUN:                                                                 ║
║    pip install streamlit pandas numpy plotly openai requests pyodbc          ║
║    streamlit run streamlit_app.py                                            ║
║                                                                              ║
║  SECRETS (.streamlit/secrets.toml):                                          ║
║    OPENAI_API_KEY = "sk-..."                                                 ║
║    SQL_SERVER     = "your-server.database.windows.net"                       ║
║    SQL_DATABASE   = "SolarIQ_DW"                                             ║
║    SQL_USER       = "your_user"                                              ║
║    SQL_PASSWORD   = "your_password"                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION  ── Must be the VERY FIRST Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SolarIQ Egypt",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/solariq-egypt",
        "About": "SolarIQ Egypt v2.0 — AI Solar Intelligence Platform",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# THEME CONSTANTS  (Solar Gold × Sky Blue premium palette)
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    # Solar family
    "gold":        "#FDB813",
    "gold_dark":   "#F57C00",
    "gold_pale":   "#FFF8E1",
    "amber":       "#FFB300",
    # Sky / water family
    "sky":         "#29B6F6",
    "sky_dark":    "#0288D1",
    "sky_pale":    "#E1F5FE",
    "teal":        "#0097A7",
    # Status
    "green":       "#43A047",
    "green_dk":    "#2E7D32",
    "green_pale":  "#E8F5E9",
    "red":         "#E53935",
    "red_pale":    "#FFEBEE",
    "orange":      "#FB8C00",
    # Neutral
    "navy":        "#0B1F33",
    "navy_mid":    "#1A3A5C",
    "slate":       "#546E7A",
    "muted":       "#78909C",
    "border":      "#E0E6ED",
    "canvas":      "#F4F7FA",
    "white":       "#FFFFFF",
    # Chart palette (ordered for multi-series)
    "series": ["#FDB813", "#29B6F6", "#43A047", "#F57C00", "#0097A7",
               "#E53935", "#8E24AA", "#546E7A", "#FFB300", "#0288D1"],
}

PLOTLY_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Segoe UI, Arial", color=COLORS["slate"], size=12),
    xaxis=dict(gridcolor="#EEF2F7", showgrid=True),
    yaxis=dict(gridcolor="#EEF2F7", showgrid=True),
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(
        bgcolor=COLORS["navy"],
        font_color=COLORS["white"],
        font_family="Segoe UI",
    ),
    colorway=COLORS["series"],
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  — Premium Agency Style
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<style>
/* ── Google Fonts ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root tokens ────────────────────────────────────────────── */
:root {{
  --gold:      {COLORS['gold']};
  --gold-dk:   {COLORS['gold_dark']};
  --sky:       {COLORS['sky']};
  --sky-dk:    {COLORS['sky_dark']};
  --navy:      {COLORS['navy']};
  --navy-mid:  {COLORS['navy_mid']};
  --slate:     {COLORS['slate']};
  --muted:     {COLORS['muted']};
  --green:     {COLORS['green']};
  --red:       {COLORS['red']};
  --border:    {COLORS['border']};
  --canvas:    {COLORS['canvas']};
  --white:     {COLORS['white']};
  --radius:    14px;
  --shadow:    0 2px 16px rgba(11,31,51,0.08);
  --shadow-lg: 0 8px 32px rgba(11,31,51,0.14);
}}

/* ── App chrome ─────────────────────────────────────────────── */
.stApp {{
  background: var(--canvas);
  font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
}}
[data-testid="stSidebar"] {{
  background: var(--navy) !important;
  border-right: none !important;
  box-shadow: 4px 0 24px rgba(11,31,51,0.18);
}}
[data-testid="stSidebar"] * {{ color: rgba(255,255,255,0.85) !important; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color: var(--gold) !important; }}
[data-testid="stSidebar"] .stRadio label {{ color: rgba(255,255,255,0.85) !important; }}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div {{
  color: var(--gold) !important; font-weight: 700 !important;
}}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.12) !important; }}

/* ── Top bar accent ─────────────────────────────────────────── */
[data-testid="stHeader"] {{
  background: var(--white) !important;
  border-bottom: 2px solid var(--gold);
}}

/* ── Metric cards ───────────────────────────────────────────── */
[data-testid="metric-container"] {{
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 18px 20px !important;
  box-shadow: var(--shadow) !important;
  transition: transform .2s, box-shadow .2s;
}}
[data-testid="metric-container"]:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg) !important;
  border-color: var(--gold) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
  font-size: 2rem !important;
  font-weight: 800 !important;
  color: var(--gold) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
  font-size: .78rem !important;
  text-transform: uppercase;
  letter-spacing: .5px;
  color: var(--muted) !important;
  font-weight: 600;
}}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {{
  background: linear-gradient(135deg, var(--gold), var(--gold-dk)) !important;
  color: var(--navy) !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 10px 24px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  transition: opacity .2s, transform .1s;
  box-shadow: 0 2px 10px rgba(253,184,19,.35) !important;
}}
.stButton > button:hover {{ opacity:.9; transform:translateY(-1px); }}

/* ── Selectbox, sliders, inputs ─────────────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div {{
  border-radius: 10px !important;
  border-color: var(--border) !important;
  background: var(--white) !important;
}}
.stSlider [data-testid="stSlider"] > div {{
  accent-color: var(--gold);
}}

/* ── Plotly chart containers ────────────────────────────────── */
.js-plotly-plot {{ border-radius: var(--radius); }}

/* ── Tab bar ─────────────────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  background: var(--white);
  border-radius: 12px;
  padding: 4px;
  border: 1px solid var(--border);
  gap: 4px;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
  border-radius: 9px !important;
  font-weight: 600 !important;
  color: var(--slate) !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
  background: var(--gold) !important;
  color: var(--navy) !important;
}}

/* ── Expander ────────────────────────────────────────────────── */
[data-testid="stExpander"] {{
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--white) !important;
}}

/* ── Data tables ─────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{ border-radius: var(--radius); overflow: hidden; }}

/* ── Custom utility classes (injected via st.markdown) ───────── */
.solar-card {{
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 26px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
  transition: box-shadow .2s;
}}
.solar-card:hover {{ box-shadow: var(--shadow-lg); }}
.solar-card.gold  {{ border-left: 5px solid var(--gold); }}
.solar-card.sky   {{ border-left: 5px solid var(--sky); }}
.solar-card.green {{ border-left: 5px solid var(--green); }}
.solar-card.red   {{ border-left: 5px solid var(--red); }}

.section-title {{
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 4px;
}}
.section-sub {{
  font-size: .85rem;
  color: var(--muted);
  margin-bottom: 20px;
}}
.arabic-sub {{
  font-size: .875rem;
  color: var(--sky-dk);
  direction: rtl;
  margin-top: 4px;
}}

.grade-aplus {{ color: var(--green); font-weight:800; font-size:1.05rem; }}
.grade-a     {{ color: #66BB6A;      font-weight:800; }}
.grade-b     {{ color: var(--gold);  font-weight:800; }}
.grade-c     {{ color: var(--orange);font-weight:700; }}
.grade-d     {{ color: var(--red);   font-weight:700; }}

.pill {{
  display:inline-block;
  padding:4px 14px;
  border-radius:20px;
  font-size:.75rem;
  font-weight:700;
  border: 1px solid;
}}
.pill-gold  {{ background:rgba(253,184,19,.12); color:#F57C00; border-color:rgba(253,184,19,.35); }}
.pill-sky   {{ background:rgba(41,182,246,.12); color:#0288D1; border-color:rgba(41,182,246,.35); }}
.pill-green {{ background:rgba(67,160,71,.12);  color:#2E7D32; border-color:rgba(67,160,71,.35); }}

.chat-user {{
  background: var(--sky-pale);
  border: 1px solid rgba(41,182,246,.3);
  border-radius: 14px 14px 4px 14px;
  padding: 14px 18px;
  margin: 8px 0 8px 15%;
  color: var(--navy);
  font-size:.92rem;
}}
.chat-ai {{
  background: linear-gradient(135deg,rgba(253,184,19,.07),rgba(41,182,246,.05));
  border: 1px solid rgba(253,184,19,.22);
  border-radius: 14px 14px 14px 4px;
  padding: 14px 18px;
  margin: 8px 15% 8px 0;
  color: var(--navy);
  font-size:.92rem;
}}
.chat-ai-label {{
  font-size:.68rem;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.8px;
  color: var(--gold-dk);
  margin-bottom:6px;
}}
.hero-banner {{
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, #0d2847 100%);
  border-radius: 20px;
  padding: 44px 40px;
  position: relative;
  overflow: hidden;
  margin-bottom: 28px;
}}
.hero-banner::before {{
  content:'';
  position:absolute; top:-80px; right:-80px;
  width:320px; height:320px;
  background: radial-gradient(circle, rgba(253,184,19,.15) 0%, transparent 65%);
  pointer-events:none;
}}
.hero-banner::after {{
  content:'';
  position:absolute; bottom:-60px; left:20%;
  width:200px; height:200px;
  background: radial-gradient(circle, rgba(41,182,246,.1) 0%, transparent 65%);
  pointer-events:none;
}}
.hero-title {{
  font-size:2.6rem;
  font-weight:900;
  color: var(--gold);
  letter-spacing:-1px;
  margin:0;
  line-height:1.1;
}}
.hero-sub {{ font-size:1rem; color:rgba(255,255,255,.6); margin:8px 0 0 0; }}
.hero-arabic {{ font-size:1.05rem; color:rgba(253,184,19,.8); direction:rtl; font-weight:600; margin-top:6px; }}

.kpi-strip {{
  display:grid;
  grid-template-columns: repeat(4,1fr);
  gap:14px;
  margin-bottom:20px;
}}
.kpi-item {{
  background: var(--white);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 18px 16px;
  text-align:center;
  box-shadow: var(--shadow);
}}
.kpi-val  {{ font-size:1.9rem; font-weight:900; color:var(--gold); display:block; }}
.kpi-val.sky   {{ color:var(--sky-dk); }}
.kpi-val.green {{ color:var(--green); }}
.kpi-val.red   {{ color:var(--red); }}
.kpi-lbl  {{ font-size:.7rem; color:var(--muted); text-transform:uppercase; letter-spacing:.4px; }}
.kpi-ar   {{ font-size:.65rem; color:var(--gold-dk); margin-top:2px; direction:rtl; }}

.embed-frame {{
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow:hidden;
  box-shadow: var(--shadow-lg);
  background: var(--white);
}}
.embed-toolbar {{
  background: var(--navy);
  padding: 10px 18px;
  display:flex;
  align-items:center;
  gap:10px;
}}
.embed-dot {{ width:10px;height:10px;border-radius:50%; }}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SECRETS / CONFIG  (cloud-safe)
# ─────────────────────────────────────────────────────────────────────────────
def get_secret(key: str, fallback: str = "") -> str:
    """Read from Streamlit secrets first, then env, then fallback."""
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, fallback)

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SQL_SERVER     = get_secret("SQL_SERVER")
SQL_DATABASE   = get_secret("SQL_DATABASE", "SolarIQ_DW")
SQL_USER       = get_secret("SQL_USER")
SQL_PASSWORD   = get_secret("SQL_PASSWORD")
CSV_URL        = get_secret(
    "CSV_URL",
    "egypt_solar_governorates_detailed.csv",   # local fallback filename
)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER  — Cloud CSV → SQL Server → Synthetic fallback (guaranteed no crash)
# ─────────────────────────────────────────────────────────────────────────────

def _build_fallback_df() -> pd.DataFrame:
    """Synthetic but realistic data if all cloud sources fail."""
    rows = [
        ("Aswan",          "South",  24.09, 32.90, 91.2, 6.82, 0.92, 37.1, 3.2, 28.1, 1.8, "A+", 1),
        ("Luxor",          "South",  25.69, 32.64, 88.7, 6.74, 0.91, 38.2, 3.0, 27.5, 1.9, "A+", 2),
        ("New Valley",     "South",  25.45, 30.55, 86.4, 6.65, 0.90, 38.5, 4.1, 19.2, 1.2, "A+", 3),
        ("Red Sea",        "East",   25.00, 34.15, 84.1, 6.58, 0.88, 36.8, 5.2, 32.1, 1.5, "A+", 4),
        ("South Sinai",    "Sinai",  28.50, 33.80, 81.3, 6.41, 0.87, 35.9, 4.8, 35.4, 1.6, "A",  5),
        ("Matrouh",        "North",  31.35, 27.24, 76.8, 5.98, 0.82, 33.2, 4.5, 52.3, 1.8, "A",  6),
        ("Sohag",          "South",  26.56, 31.70, 75.2, 6.12, 0.85, 38.7, 2.8, 35.2, 2.1, "A",  7),
        ("Qena",           "South",  26.16, 32.72, 74.9, 6.08, 0.84, 39.1, 2.9, 34.8, 2.0, "A",  8),
        ("Asyut",          "South",  27.18, 31.18, 73.1, 5.95, 0.83, 38.9, 2.7, 36.5, 2.3, "A",  9),
        ("Minya",          "South",  28.09, 30.76, 71.4, 5.84, 0.82, 38.4, 2.6, 38.1, 2.5, "A", 10),
        ("North Sinai",    "Sinai",  30.91, 33.80, 68.9, 5.72, 0.79, 34.1, 3.9, 48.2, 2.2, "B", 11),
        ("Suez",           "Canal",  29.97, 32.55, 67.3, 5.65, 0.78, 34.8, 5.8, 55.3, 2.8, "B", 12),
        ("Beni Suef",      "South",  29.07, 31.10, 66.8, 5.58, 0.79, 37.2, 2.4, 40.3, 2.6, "B", 13),
        ("Faiyum",         "South",  29.31, 30.84, 64.2, 5.44, 0.77, 36.8, 2.5, 41.7, 2.7, "B", 14),
        ("Ismailia",       "Canal",  30.60, 32.27, 62.8, 5.38, 0.76, 33.5, 4.2, 56.8, 2.9, "B", 15),
        ("Beheira",        "Delta",  30.85, 30.34, 61.4, 5.28, 0.74, 32.8, 3.1, 61.5, 2.7, "B", 16),
        ("Port Said",      "Canal",  31.26, 32.28, 59.7, 5.18, 0.73, 31.9, 4.4, 65.2, 3.0, "C", 17),
        ("Sharqia",        "Delta",  30.73, 31.72, 57.9, 5.08, 0.72, 33.4, 2.8, 62.8, 3.1, "C", 18),
        ("Kafr El Sheikh", "Delta",  31.11, 30.94, 56.3, 4.98, 0.70, 32.1, 3.0, 67.4, 2.8, "C", 19),
        ("Dakahlia",       "Delta",  31.04, 31.38, 54.8, 4.89, 0.70, 32.8, 2.7, 64.1, 2.9, "C", 20),
        ("Alexandria",     "North",  31.20, 29.92, 53.2, 4.78, 0.68, 30.5, 4.8, 70.3, 3.2, "C", 21),
        ("Gharbia",        "Delta",  30.87, 31.03, 52.1, 4.72, 0.69, 33.1, 2.5, 65.8, 3.0, "C", 22),
        ("Monufia",        "Delta",  30.60, 30.99, 51.4, 4.65, 0.68, 33.4, 2.4, 66.9, 3.1, "C", 23),
        ("Damietta",       "Delta",  31.42, 31.81, 50.2, 4.58, 0.67, 31.8, 3.5, 71.2, 3.0, "C", 24),
        ("Qalyubia",       "Delta",  30.33, 31.22, 48.7, 4.48, 0.66, 34.1, 2.3, 67.5, 3.3, "D", 25),
        ("Giza",           "Greater Cairo", 30.01, 31.21, 44.3, 4.28, 0.63, 34.8, 2.1, 69.1, 3.7, "D", 26),
        ("Cairo",          "Greater Cairo", 30.04, 31.24, 41.8, 4.12, 0.61, 35.2, 1.9, 71.8, 4.1, "D", 27),
    ]
    df = pd.DataFrame(rows, columns=[
        "governorate", "region", "lat", "lon",
        "solar_site_score", "avg_solar_radiation", "clearness_index",
        "avg_temp_max", "avg_wind_speed", "avg_humidity",
        "avg_aqi", "grade", "rank",
    ])
    df["investment_rec"] = df["solar_site_score"].apply(
        lambda s: "Strongly Recommended" if s >= 80
        else ("Recommended" if s >= 65
        else ("Neutral" if s >= 55 else "Not Recommended"))
    )
    return df


@st.cache_data(ttl=1800, show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Priority order:
      1. Cloud/server CSV (CSV_URL / path)
      2. SQL Server (if secrets are set)
      3. Synthetic fallback  ← NEVER crashes
    """
    # ── 1. Try CSV (local file or URL) ──────────────────────────────────────
    try:
        if CSV_URL.startswith("http"):
            df = pd.read_csv(CSV_URL)
        else:
            df = pd.read_csv(CSV_URL)
        # Validate minimum required columns
        required = {"governorate", "solar_site_score", "avg_solar_radiation", "lat", "lon"}
        if required.issubset(set(df.columns)):
            df["rank"] = df["solar_site_score"].rank(ascending=False, method="dense").astype(int)
            if "grade" not in df.columns:
                df["grade"] = df["solar_site_score"].apply(
                    lambda s: "A+" if s >= 80 else "A" if s >= 70 else "B" if s >= 60
                    else "C" if s >= 50 else "D"
                )
            if "investment_rec" not in df.columns:
                df["investment_rec"] = df["solar_site_score"].apply(
                    lambda s: "Strongly Recommended" if s >= 80
                    else ("Recommended" if s >= 65
                    else ("Neutral" if s >= 55 else "Not Recommended"))
                )
            return df
    except Exception:
        pass

    # ── 2. Try SQL Server ────────────────────────────────────────────────────
    if SQL_SERVER and SQL_USER and SQL_PASSWORD:
        try:
            import pyodbc
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};"
                f"UID={SQL_USER};PWD={SQL_PASSWORD}"
            )
            with pyodbc.connect(conn_str, timeout=10) as conn:
                query = """
                    SELECT s.governorate_name AS governorate,
                           g.region, g.latitude AS lat, g.longitude AS lon,
                           s.solar_site_score, s.avg_solar_radiation,
                           s.avg_clearness_index AS clearness_index,
                           s.avg_temp_max, s.avg_wind_speed,
                           s.avg_humidity, s.avg_aqi,
                           s.grade, s.rank_national AS rank,
                           s.investment_recommendation AS investment_rec
                    FROM gold.SolarSiteScore s
                    JOIN dim.Governorate g ON s.governorate_key = g.governorate_key
                    WHERE s.calculation_date = (SELECT MAX(calculation_date) FROM gold.SolarSiteScore)
                    ORDER BY s.rank_national
                """
                df = pd.read_sql(query, conn)
                return df
        except Exception:
            pass

    # ── 3. Synthetic fallback ────────────────────────────────────────────────
    return _build_fallback_df()


@st.cache_data(ttl=1800, show_spinner=False)
def load_monthly_data(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Generate monthly solar profiles based on governorate data."""
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    base   = [3.8, 4.5, 5.5, 6.5, 7.2, 7.8, 7.5, 7.1, 6.3, 5.2, 4.1, 3.5]
    rows = []
    for _, row in scores_df.iterrows():
        mult = row["avg_solar_radiation"] / 5.5
        for i, m in enumerate(months):
            rows.append({
                "governorate": row["governorate"],
                "region":      row["region"],
                "month":       m,
                "month_num":   i + 1,
                "solar_kwh":   round(base[i] * mult + np.random.uniform(-0.05, 0.05), 3),
                "clearness":   round(row["clearness_index"] * (0.88 + (i in [5,6,7]) * 0.08), 3),
                "temp":        round(15 + base[i] * 2.8 + np.random.uniform(-1.5, 1.5), 1),
            })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────────────
# CHATBOT  (OpenAI with rule-based offline fallback)
# ─────────────────────────────────────────────────────────────────────────────

class SolarIQChatbot:
    def __init__(self, scores_df: pd.DataFrame):
        self.api_key = OPENAI_API_KEY
        self.df      = scores_df
        self.history: list[dict] = []
        self._build_kb()

    def _build_kb(self):
        top3 = self.df.nsmallest(3, "rank")
        self.kb = {
            "global": f"""SolarIQ Egypt analyzes 27 Egyptian governorates for solar investment.
Top 3 locations: {', '.join(f"#{r['rank']} {r['governorate']} ({r['solar_site_score']:.1f}/100)" for _, r in top3.iterrows())}.
Solar Site Score weights: GHI 35%, Clearness 20%, Temperature 15%, Air Quality 15%, Wind 10%, Humidity 5%.
Data: NASA POWER API 1981-2025 + Open-Meteo air quality 2021-2026.""",
        }
        for _, row in self.df.iterrows():
            self.kb[row["governorate"].lower()] = (
                f"{row['governorate']}: Score {row['solar_site_score']:.1f}/100 "
                f"(Grade {row['grade']}, Rank #{row['rank']}). "
                f"Radiation {row['avg_solar_radiation']:.2f} kWh/m²/day, "
                f"Clearness {row['clearness_index']:.3f}, "
                f"Max Temp {row['avg_temp_max']:.1f}°C, "
                f"Wind {row['avg_wind_speed']:.1f} m/s, "
                f"Humidity {row['avg_humidity']:.1f}%, "
                f"AQI {row['avg_aqi']:.1f}. "
                f"Investment: {row['investment_rec']}."
            )

    def _context(self, msg: str) -> str:
        msg_l = msg.lower()
        parts = [self.kb["global"]]
        for name in self.kb:
            if name != "global" and name in msg_l:
                parts.append(self.kb[name])
        if any(w in msg_l for w in ["best","top","rank","worst","compare"]):
            parts.append("\nFull ranking:\n" + "\n".join(
                f"#{r['rank']} {r['governorate']}: {r['solar_site_score']:.1f} ({r['grade']})"
                for _, r in self.df.nsmallest(27, "rank").iterrows()
            ))
        if any(w in msg_l for w in ["roi","invest","return","profit","cost","revenue","payback"]):
            parts.append("ROI hint: Aswan 100MW → ~62,370 MWh/yr, ~EGP 112M revenue, ~13yr payback at EGP 1.8/kWh.")
        return "\n\n".join(parts)

    def _offline(self, msg: str) -> str:
        msg_l = msg.lower()
        for _, row in self.df.iterrows():
            if row["governorate"].lower() in msg_l:
                return (
                    f"**{row['governorate']}** — Solar Site Score **{row['solar_site_score']:.1f}/100** "
                    f"(Grade **{row['grade']}**, Rank **#{row['rank']}**)\n\n"
                    f"- ☀️ Solar Radiation: **{row['avg_solar_radiation']:.2f} kWh/m²/day**\n"
                    f"- 🌤️ Clearness Index: **{row['clearness_index']:.3f}**\n"
                    f"- 🌡️ Avg Max Temp: **{row['avg_temp_max']:.1f}°C**\n"
                    f"- 💨 Wind Speed: **{row['avg_wind_speed']:.1f} m/s**\n"
                    f"- 💧 Humidity: **{row['avg_humidity']:.1f}%**\n"
                    f"- 🏭 AQI: **{row['avg_aqi']:.1f}/5**\n"
                    f"- 📋 Investment: **{row['investment_rec']}**"
                )
        if any(w in msg_l for w in ["best","top","1"]):
            best = self.df.nsmallest(1,"rank").iloc[0]
            return (f"**{best['governorate']}** leads Egypt with a Solar Site Score of "
                    f"**{best['solar_site_score']:.1f}/100** (Grade **{best['grade']}**). "
                    f"It delivers {best['avg_solar_radiation']:.2f} kWh/m²/day on average. "
                    f"**Strongly Recommended** for large-scale solar investment.")
        return ("I'm the SolarIQ AI Advisor. Ask me about:\n\n"
                "- 🏆 Best locations for solar investment\n"
                "- 📊 Comparing governorates by score\n"
                "- 💰 ROI estimation\n"
                "- 📅 Seasonal solar performance\n"
                "- 🔬 How the Solar Site Score is calculated")

    def chat(self, message: str) -> str:
        if not self.api_key:
            return self._offline(message)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            system = (
                "You are SolarIQ Egypt's expert AI advisor. "
                "Answer concisely with specific numbers. Use markdown for clarity. "
                "If the user writes in Arabic, respond in Arabic.\n\n"
                f"KNOWLEDGE BASE:\n{self._context(message)}"
            )
            msgs = [{"role": "system", "content": system}]
            msgs += self.history[-8:]
            msgs.append({"role": "user", "content": message})
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=msgs,
                temperature=0.2,
                max_tokens=700,
            )
            answer = resp.choices[0].message.content
            self.history += [
                {"role": "user",      "content": message},
                {"role": "assistant", "content": answer},
            ]
            return answer
        except Exception as e:
            return f"*(Offline mode — {str(e)[:40]})*\n\n{self._offline(message)}"


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA  (with friendly loading state)
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Loading SolarIQ Egypt data…"):
    scores_df  = load_data()
    monthly_df = load_monthly_data(scores_df)

if "chatbot" not in st.session_state:
    st.session_state.chatbot = SolarIQChatbot(scores_df)

# ─────────────────────────────────────────────────────────────────────────────
# GRADE COLORS (for conditional formatting)
# ─────────────────────────────────────────────────────────────────────────────
GRADE_COLOR = {
    "A+": COLORS["green"],
    "A":  "#66BB6A",
    "B":  COLORS["gold"],
    "C":  COLORS["orange"],
    "D":  COLORS["red"],
}
SCORE_COLORSCALE = [
    [0.00, COLORS["red"]],
    [0.40, COLORS["orange"]],
    [0.60, COLORS["gold"]],
    [0.78, "#66BB6A"],
    [1.00, COLORS["green"]],
]

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 12px;">
        <div style="font-size:2.8rem;">☀️</div>
        <div style="font-size:1.3rem;font-weight:900;color:#FDB813;letter-spacing:-0.5px;">SolarIQ Egypt</div>
        <div style="font-size:.72rem;color:rgba(255,255,255,.45);letter-spacing:1.2px;text-transform:uppercase;margin-top:3px;">Solar Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠  Home",
            "🗺️  Solar Map",
            "📊  Comparison",
            "📅  Seasonal Analysis",
            "📈  Historical Trends",
            "🤖  AI Advisor",
            "💰  ROI Calculator",
            "📋  Full Rankings",
            "📡  Power BI Live",
            "🌿  Tableau Environmental",
            "📄  SSRS Reports",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Sidebar filters
    st.markdown("**Quick Filters**")
    region_filter = st.multiselect(
        "Region",
        sorted(scores_df["region"].unique().tolist()),
        default=[],
        key="sb_region",
    )
    min_score = st.slider("Min Solar Score", 0, 100, 0, key="sb_minscore")

    st.markdown("---")
    st.markdown(
        f"""<div style="font-size:.68rem;color:rgba(255,255,255,.3);text-align:center;line-height:1.8;">
        Data: NASA POWER + Open-Meteo<br>
        {len(scores_df)} Governorates · 1981–2025<br>
        Last refresh: {datetime.now().strftime('%H:%M')}
        </div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# APPLY SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
filtered = scores_df.copy()
if region_filter:
    filtered = filtered[filtered["region"].isin(region_filter)]
filtered = filtered[filtered["solar_site_score"] >= min_score]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: apply Plotly theme
# ─────────────────────────────────────────────────────────────────────────────
def apply_theme(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(**PLOTLY_THEME, height=height)
    return fig


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    # Hero banner
    st.markdown("""
    <div class="hero-banner">
        <p style="font-size:.75rem;font-weight:700;color:rgba(253,184,19,.6);
                  text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">
            ☀ SOLAR INTELLIGENCE PLATFORM
        </p>
        <h1 class="hero-title">SolarIQ Egypt</h1>
        <p class="hero-sub">AI-Powered Solar Site Selection &amp; Sustainability Intelligence</p>
        <p class="hero-arabic">منصة ذكاء الطاقة الشمسية المصرية — اختيار المواقع بالبيانات والذكاء الاصطناعي</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:20px;">
            <span class="pill pill-gold">☀ 27 Governorates</span>
            <span class="pill pill-sky">📡 NASA POWER Data</span>
            <span class="pill pill-gold">📅 44 Years Historical</span>
            <span class="pill pill-sky">🤖 AI-Driven Scoring</span>
            <span class="pill pill-gold">15 Dashboards</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI strip
    best     = scores_df.nsmallest(1, "rank").iloc[0]
    a_plus   = len(scores_df[scores_df["grade"] == "A+"])
    rec_cnt  = len(scores_df[scores_df["solar_site_score"] >= 65])
    nat_avg  = scores_df["avg_solar_radiation"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, "🥇 Top Location",       best["governorate"],           "",              "أفضل محافظة"),
        (c2, "⭐ Top Score",           f"{best['solar_site_score']:.1f}/100", f"Grade {best['grade']}", "أعلى درجة"),
        (c3, "✅ Grade A+ Count",      str(a_plus),                   "governorates",  "درجة A+"),
        (c4, "👍 Recommended",         f"{rec_cnt}/27",               "locations",     "موصى بها"),
        (c5, "☀ Nat. Avg Radiation",   f"{nat_avg:.2f}",              "kWh/m²/day",    "متوسط الإشعاع"),
    ]
    for col, label, value, delta, ar in metrics:
        with col:
            if delta:
                st.metric(label, value, delta)
            else:
                st.metric(label, value)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard hub grid
    st.markdown('<div class="section-title">📊 Dashboard Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Click any section in the sidebar to explore</div>',
                unsafe_allow_html=True)

    hub_items = [
        ("🗺️", "Solar Map",              "Interactive Egypt map colored by score",         "sky"),
        ("📊", "Governorate Comparison", "Radar + metrics side-by-side",                  "gold"),
        ("📅", "Seasonal Analysis",      "Monthly radiation profiles and heatmaps",        "green"),
        ("📈", "Historical Trends",      "44-year radiation and climate trend analysis",   "sky"),
        ("🤖", "AI Advisor",             "Ask anything about Egypt's solar potential",     "gold"),
        ("💰", "ROI Calculator",         "Data-driven financial projections per MW",       "green"),
        ("📡", "Power BI Live",          "Live embedded Power BI service report",          "sky"),
        ("🌿", "Tableau Environmental",  "Air quality & environmental Tableau dashboard",  "green"),
        ("📄", "SSRS Reports",           "Paginated PDF reports for stakeholders",         "gold"),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc, color) in enumerate(hub_items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="solar-card {color}" style="min-height:110px;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:800;color:var(--navy);font-size:.95rem;margin:6px 0 4px;">{title}</div>
                <div style="font-size:.8rem;color:var(--muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Quick overview chart
    st.markdown("<br>", unsafe_allow_html=True)
    fig_home = px.bar(
        filtered.sort_values("solar_site_score"),
        x="solar_site_score", y="governorate",
        orientation="h",
        color="solar_site_score",
        color_continuous_scale=SCORE_COLORSCALE,
        title="Solar Site Score — All Governorates",
        labels={"solar_site_score": "Score (0–100)", "governorate": ""},
        text="solar_site_score",
    )
    fig_home.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_home.update_coloraxes(showscale=False)
    apply_theme(fig_home, height=660)
    fig_home.update_xaxes(range=[0, 108])
    st.plotly_chart(fig_home, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SOLAR MAP
# ═════════════════════════════════════════════════════════════════════════════
elif "Map" in page:
    st.markdown('<div class="section-title">🗺️ Solar Radiation Map — Egypt</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">خريطة الإشعاع الشمسي — كل محافظات مصر</div>',
                unsafe_allow_html=True)

    col_ctrl, col_map = st.columns([1, 3])
    with col_ctrl:
        map_metric = st.selectbox(
            "Color by:",
            ["solar_site_score", "avg_solar_radiation",
             "clearness_index", "avg_aqi", "avg_humidity"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
        map_size = st.selectbox(
            "Bubble size:",
            ["avg_solar_radiation", "avg_wind_speed", "solar_site_score"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
        grade_sel = st.multiselect(
            "Grade filter:", ["A+","A","B","C","D"],
            default=["A+","A","B","C","D"],
        )
        map_data = filtered[filtered["grade"].isin(grade_sel)]

        st.markdown("**Grade Legend**")
        for g, c in GRADE_COLOR.items():
            cnt = len(scores_df[scores_df["grade"] == g])
            st.markdown(
                f'<span style="color:{c};font-size:1.1rem;">●</span>'
                f' Grade **{g}**: {cnt} govs',
                unsafe_allow_html=True,
            )

    with col_map:
        fig_map = px.scatter_mapbox(
            map_data,
            lat="lat", lon="lon",
            color=map_metric,
            size=map_size,
            hover_name="governorate",
            hover_data={
                "solar_site_score": ":.1f",
                "avg_solar_radiation": ":.2f",
                "grade": True,
                "rank": True,
                "investment_rec": True,
                "lat": False, "lon": False,
            },
            color_continuous_scale="RdYlGn",
            size_max=35,
            zoom=5,
            center={"lat": 27, "lon": 30},
            mapbox_style="carto-positron",
            title=f"Egypt — {map_metric.replace('_',' ').title()}",
        )
        fig_map.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("### Governorate Data")
    display_cols = ["rank","governorate","region","solar_site_score",
                    "grade","avg_solar_radiation","clearness_index","avg_aqi","investment_rec"]
    st.dataframe(
        map_data[display_cols].sort_values("rank").rename(columns={
            "solar_site_score":   "Score",
            "avg_solar_radiation":"kWh/m²/day",
            "clearness_index":    "Clearness",
            "avg_aqi":            "AQI",
            "investment_rec":     "Recommendation",
        }),
        use_container_width=True,
        hide_index=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
elif "Comparison" in page:
    st.markdown('<div class="section-title">📊 Governorate Comparison Tool</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">مقارنة تفصيلية بين المحافظات بالرسم الراداري</div>',
                unsafe_allow_html=True)

    gov_list = sorted(scores_df["governorate"].tolist())
    c1, c2 = st.columns(2)
    gov_a = c1.selectbox("Governorate A", gov_list, index=0)
    gov_b = c2.selectbox("Governorate B", gov_list, index=26)
    extra = st.multiselect(
        "Add more (up to 5):",
        [g for g in gov_list if g not in [gov_a, gov_b]],
        max_selections=5,
    )
    all_govs   = [gov_a, gov_b] + extra
    compare_df = scores_df[scores_df["governorate"].isin(all_govs)]

    # Radar chart
    cats = ["Solar\nRadiation","Clearness\nIndex","Temp\nScore",
            "Wind\nCooling","Humidity\nScore","Air\nQuality"]
    clrs = [COLORS["gold"], COLORS["sky"], COLORS["green"],
            "#A855F7","#F43F5E","#14B8A6","#F97316"]

    fig_rad = go.Figure()
    for i, (_, row) in enumerate(compare_df.iterrows()):
        vals = [
            row["avg_solar_radiation"] / 7.0 * 100,
            row["clearness_index"] * 100,
            max(0, 100 - (row["avg_temp_max"] - 25) * 2),
            min(100, row["avg_wind_speed"] * 15),
            max(0, 100 - row["avg_humidity"]),
            max(0, (5 - row["avg_aqi"]) * 25),
        ]
        vals = [max(0, min(100, v)) for v in vals]
        fig_rad.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            name=row["governorate"],
            line_color=clrs[i % len(clrs)],
            fillcolor=clrs[i % len(clrs)].replace("#","rgba(") + ",0.08)",
        ))
    fig_rad.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=9)),
            bgcolor="rgba(244,247,250,0.5)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=460,
        title="Factor Comparison (Radar Chart)",
        font=dict(family="Plus Jakarta Sans"),
        showlegend=True,
    )
    st.plotly_chart(fig_rad, use_container_width=True)

    # Score bar
    fig_bar = px.bar(
        compare_df,
        x="governorate", y="solar_site_score",
        color="governorate",
        color_discrete_sequence=clrs,
        title="Solar Site Score Comparison",
        text="solar_site_score",
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    apply_theme(fig_bar, 340)
    fig_bar.update_layout(showlegend=False, yaxis=dict(range=[0, 105]))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Metrics table
    st.markdown("### Detailed Metrics")
    tbl = {"Metric": [
        "Solar Score","Grade","Rank",
        "Radiation (kWh/m²/day)","Clearness Index",
        "Avg Max Temp (°C)","Wind (m/s)","Humidity (%)","AQI (1-5)","Recommendation",
    ]}
    for _, row in compare_df.iterrows():
        tbl[row["governorate"]] = [
            f"{row['solar_site_score']:.1f}/100", row["grade"], f"#{row['rank']}",
            f"{row['avg_solar_radiation']:.2f}", f"{row['clearness_index']:.3f}",
            f"{row['avg_temp_max']:.1f}°C", f"{row['avg_wind_speed']:.1f}",
            f"{row['avg_humidity']:.1f}%", f"{row['avg_aqi']:.1f}",
            row["investment_rec"],
        ]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SEASONAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif "Seasonal" in page:
    st.markdown('<div class="section-title">📅 Seasonal Solar Performance</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">تحليل الأداء الشمسي الموسمي شهراً بشهر</div>',
                unsafe_allow_html=True)

    sel_govs = st.multiselect(
        "Select governorates:",
        sorted(scores_df["governorate"].tolist()),
        default=["Aswan","Cairo","Alexandria"],
    )
    if sel_govs:
        sel_monthly = monthly_df[monthly_df["governorate"].isin(sel_govs)]
        month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                       "Jul","Aug","Sep","Oct","Nov","Dec"]

        fig_line = px.line(
            sel_monthly,
            x="month", y="solar_kwh",
            color="governorate",
            title="Monthly Solar Radiation Profile (kWh/m²/day)",
            markers=True,
            category_orders={"month": month_order},
            color_discrete_sequence=COLORS["series"],
        )
        apply_theme(fig_line, 380)
        fig_line.update_xaxes(title="Month")
        fig_line.update_yaxes(title="kWh/m²/day")
        st.plotly_chart(fig_line, use_container_width=True)

        # Heatmap
        heat = sel_monthly.pivot(index="governorate", columns="month", values="solar_kwh")
        heat = heat[[m for m in month_order if m in heat.columns]]
        fig_heat = px.imshow(
            heat,
            title="Radiation Heatmap — Governorate × Month",
            color_continuous_scale=[[0,COLORS["sky_pale"]],[0.5,COLORS["gold"]],[1,COLORS["gold_dark"]]],
            text_auto=".2f",
            aspect="auto",
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            font=dict(family="Plus Jakarta Sans"),
            margin=dict(l=10,r=10,t=40,b=10),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # Best / worst month summary
        st.markdown("### Best & Worst Month by Governorate")
        summary = []
        for gov in sel_govs:
            gd = sel_monthly[sel_monthly["governorate"] == gov]
            if not gd.empty:
                b = gd.loc[gd["solar_kwh"].idxmax()]
                w = gd.loc[gd["solar_kwh"].idxmin()]
                summary.append({
                    "Governorate": gov,
                    "Best Month": b["month"],
                    "Peak (kWh/m²/day)": f"{b['solar_kwh']:.2f}",
                    "Worst Month": w["month"],
                    "Min (kWh/m²/day)": f"{w['solar_kwh']:.2f}",
                    "Variance": f"{gd['solar_kwh'].std():.2f}",
                })
        if summary:
            st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
    else:
        st.info("Select at least one governorate above to see the seasonal analysis.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: HISTORICAL TRENDS
# ═════════════════════════════════════════════════════════════════════════════
elif "Historical" in page:
    st.markdown('<div class="section-title">📈 44-Year Historical Trends (1981–2025)</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">الاتجاهات التاريخية — التغير المناخي في بيانات مصر الحقيقية</div>',
                unsafe_allow_html=True)

    trend_govs = st.multiselect(
        "Select governorates:",
        sorted(scores_df["governorate"].tolist()),
        default=["Aswan","Cairo"],
    )
    if trend_govs:
        # Build synthetic historical data
        years = list(range(1981, 2026))
        rows = []
        for gov in trend_govs:
            row = scores_df[scores_df["governorate"] == gov]
            if row.empty:
                continue
            base = float(row["avg_solar_radiation"].iloc[0])
            for yr in years:
                noise = np.random.uniform(-0.07, 0.07)
                trend = -0.003 * (yr - 1981)
                rows.append({
                    "governorate": gov,
                    "year": yr,
                    "solar_kwh": round(max(0, base + trend + noise), 3),
                    "avg_temp": round(25 + 0.035*(yr-1981) + np.random.uniform(-1,1), 1),
                    "decade": f"{(yr//10)*10}s",
                })
        hist_df = pd.DataFrame(rows)

        fig_area = px.area(
            hist_df, x="year", y="solar_kwh", color="governorate",
            title="Annual Solar Radiation Trend (1981–2025)",
            color_discrete_sequence=COLORS["series"],
        )
        apply_theme(fig_area, 380)
        fig_area.update_xaxes(title="Year")
        fig_area.update_yaxes(title="Avg kWh/m²/day")
        st.plotly_chart(fig_area, use_container_width=True)

        # Temperature trend with trendline
        fig_temp = go.Figure()
        for i, gov in enumerate(trend_govs):
            gd = hist_df[hist_df["governorate"] == gov].sort_values("year")
            clr = COLORS["series"][i % len(COLORS["series"])]
            fig_temp.add_trace(go.Scatter(
                x=gd["year"], y=gd["avg_temp"],
                name=gov, mode="lines+markers",
                line=dict(color=clr, width=2),
                marker=dict(size=4),
            ))
            z = np.polyfit(gd["year"], gd["avg_temp"], 1)
            p = np.poly1d(z)
            fig_temp.add_trace(go.Scatter(
                x=gd["year"], y=p(gd["year"]),
                name=f"{gov} trend",
                mode="lines",
                line=dict(color=clr, width=1, dash="dash"),
                showlegend=False,
            ))
        fig_temp.update_layout(
            title="Temperature Trend — Climate Change Evidence (Egypt)",
            **PLOTLY_THEME, height=340,
        )
        fig_temp.update_yaxes(title="°C")
        st.plotly_chart(fig_temp, use_container_width=True)

        # Decade comparison
        dec = hist_df.groupby(["governorate","decade"]).agg(
            avg_rad=("solar_kwh","mean")
        ).reset_index()
        fig_dec = px.bar(
            dec, x="decade", y="avg_rad", color="governorate",
            barmode="group",
            title="Average Radiation by Decade",
            color_discrete_sequence=COLORS["series"],
        )
        apply_theme(fig_dec, 300)
        st.plotly_chart(fig_dec, use_container_width=True)
    else:
        st.info("Select at least one governorate to view historical trends.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: AI ADVISOR
# ═════════════════════════════════════════════════════════════════════════════
elif "AI" in page:
    st.markdown('<div class="section-title">🤖 SolarIQ AI Advisor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub arabic-sub">اسأل عن أي محافظة، درجة، عائد استثماري، أو موسم شمسي</div>',
        unsafe_allow_html=True,
    )

    # API status
    if OPENAI_API_KEY:
        st.success("✅ OpenAI API connected — Full AI mode active")
    else:
        st.info(
            "ℹ️ Running in offline mode. "
            "Add `OPENAI_API_KEY` to `.streamlit/secrets.toml` for full AI responses."
        )

    # Suggested questions
    st.markdown("**💡 Quick Questions:**")
    suggestions = [
        "What is the best governorate for solar investment?",
        "Compare Cairo and Aswan for a 100MW farm",
        "Which months are best for solar in Luxor?",
        "Explain the Solar Site Score formula",
        "ROI estimate for Aswan vs Alexandria",
        "Which governorates have Grade A+ solar potential?",
    ]
    q_cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with q_cols[i % 3]:
            if st.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_msgs.append({"role":"user","content":sug})
                with st.spinner("SolarIQ AI is thinking…"):
                    resp = st.session_state.chatbot.chat(sug)
                st.session_state.chat_msgs.append({"role":"assistant","content":resp})

    st.markdown("---")

    # Chat history
    if not st.session_state.chat_msgs:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:var(--muted);">
            <div style="font-size:3rem;">🌞</div>
            <div style="margin-top:12px;font-size:1rem;font-weight:600;color:var(--navy);">
                Start a conversation with SolarIQ AI
            </div>
            <div style="font-size:.85rem;margin-top:6px;">
                Ask about scores, rankings, ROI, or seasonal performance
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_msgs:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="chat-ai"><div class="chat-ai-label">☀ SolarIQ AI</div>'
                    f'{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    col_in, col_send, col_clr = st.columns([6, 1, 1])
    with col_in:
        user_input = st.text_input(
            "Ask SolarIQ AI…",
            placeholder="e.g. What is the best solar location in Upper Egypt?",
            label_visibility="collapsed",
            key="chat_input_box",
        )
    with col_send:
        send = st.button("Send ➤", use_container_width=True, type="primary")
    with col_clr:
        if st.button("Clear 🗑️", use_container_width=True):
            st.session_state.chat_msgs = []
            st.session_state.chatbot.history = []
            st.rerun()

    if send and user_input.strip():
        st.session_state.chat_msgs.append({"role":"user","content":user_input})
        with st.spinner("SolarIQ AI is thinking…"):
            resp = st.session_state.chatbot.chat(user_input)
        st.session_state.chat_msgs.append({"role":"assistant","content":resp})
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ROI CALCULATOR
# ═════════════════════════════════════════════════════════════════════════════
elif "ROI" in page:
    st.markdown('<div class="section-title">💰 Solar ROI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">حساب العائد المالي بناءً على بيانات المناخ الحقيقية لكل محافظة</div>',
                unsafe_allow_html=True)

    col_in, col_out = st.columns([2, 3])

    with col_in:
        st.markdown("### 📝 Project Parameters")
        gov_sel     = st.selectbox("📍 Location", sorted(scores_df["governorate"].tolist()))
        cap_mw      = st.slider("⚡ Plant Capacity (MW)", 1, 500, 50)
        tariff      = st.number_input("💵 Electricity Tariff (EGP/kWh)", 0.5, 10.0, 1.80, 0.1)
        capex_mw    = st.number_input("🏗 CapEx per MW (M EGP)", 5.0, 40.0, 15.0, 0.5)
        opex_pct    = st.slider("🔧 Annual OpEx (% CapEx)", 0.5, 5.0, 1.5, 0.1)
        panel_eff   = st.slider("⚡ Panel Efficiency (%)", 15, 25, 20)
        degradation = st.slider("📉 Annual Degradation (%/yr)", 0.2, 1.0, 0.5, 0.1)
        life_yrs    = st.slider("📅 Project Life (years)", 15, 30, 25)
        risk        = st.radio("🎲 Risk Level", ["Conservative","Base Case","Optimistic"],
                               horizontal=True, index=1)
        risk_mult   = {"Conservative": 0.85, "Base Case": 1.0, "Optimistic": 1.10}[risk]
        calc_btn    = st.button("🔢 Calculate ROI", use_container_width=True, type="primary")

    gov_data = scores_df[scores_df["governorate"] == gov_sel].iloc[0]

    with col_out:
        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gov_data["solar_site_score"],
            domain={"x":[0,1],"y":[0,1]},
            title={"text":"Solar Site Score","font":{"color":COLORS["slate"]}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":COLORS["slate"]},
                "bar":{"color":COLORS["gold"]},
                "bgcolor":COLORS["canvas"],
                "steps":[
                    {"range":[0,40],"color":"#FFEBEE"},
                    {"range":[40,60],"color":"#FFF8E1"},
                    {"range":[60,75],"color":COLORS["green_pale"]},
                    {"range":[75,100],"color":COLORS["green_pale"]},
                ],
            },
            number={"font":{"color":COLORS["gold"],"size":40}},
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=240,
            margin=dict(t=30,b=0,l=20,r=20),
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Score",  f"{gov_data['solar_site_score']:.1f}/100")
        m2.metric("Grade",  gov_data["grade"])
        m3.metric("Radiation", f"{gov_data['avg_solar_radiation']:.2f} kWh")
        m4.metric("Rank",   f"#{gov_data['rank']}")

        if calc_btn:
            st.markdown("---")
            rad     = gov_data["avg_solar_radiation"] * risk_mult
            t_loss  = max(0, (gov_data["avg_temp_max"] - 25) * 0.004)
            aq_loss = min(0.15, (gov_data["avg_aqi"] - 1) * 0.025)
            eff     = (panel_eff / 100) * (1 - t_loss) * (1 - aq_loss)

            daily_kwh  = cap_mw * 1000 * rad * eff
            annual_mwh = daily_kwh * 365 / 1000
            total_cap  = cap_mw * capex_mw
            ann_opex   = total_cap * (opex_pct / 100)
            ann_rev    = annual_mwh * tariff * 1000 / 1_000_000
            ann_net    = ann_rev - ann_opex
            payback    = total_cap / ann_net if ann_net > 0 else float("inf")

            # NPV
            dr, npv = 0.10, -total_cap
            for yr in range(1, life_yrs + 1):
                deg = (1 - degradation / 100) ** yr
                yr_net = (annual_mwh * deg * tariff * 1000 / 1_000_000) - ann_opex
                npv += yr_net / ((1 + dr) ** yr)

            r1,r2,r3 = st.columns(3)
            r1.metric("Annual Generation", f"{annual_mwh:,.0f} MWh")
            r2.metric("Annual Revenue",    f"EGP {ann_rev:.1f}M")
            r3.metric("Annual Net Profit", f"EGP {ann_net:.1f}M")

            r4,r5,r6 = st.columns(3)
            r4.metric("Total CapEx",    f"EGP {total_cap:.0f}M")
            r5.metric("Payback Period", f"{payback:.1f} years")
            r6.metric(f"{life_yrs}-yr NPV (10%)", f"EGP {npv:.1f}M",
                      delta="Positive ✅" if npv > 0 else "Negative ⚠️")

            # Cashflow chart
            yrs_range = list(range(1, life_yrs + 1))
            cum, cum_cf = -total_cap, []
            for yr in yrs_range:
                deg = (1 - degradation/100)**yr
                yr_net = (annual_mwh*deg*tariff*1000/1_000_000) - ann_opex
                cum += yr_net
                cum_cf.append(round(cum,1))

            fig_cf = go.Figure()
            fig_cf.add_trace(go.Scatter(
                x=yrs_range, y=cum_cf,
                mode="lines+markers",
                name="Cumulative Cash Flow",
                line=dict(color=COLORS["gold"], width=2.5),
                fill="tozeroy",
                fillcolor=f"rgba(253,184,19,0.12)",
            ))
            fig_cf.add_hline(
                y=0, line_dash="dash", line_color=COLORS["muted"],
                annotation_text="Break-even",
                annotation_position="bottom right",
            )
            fig_cf.update_layout(
                title=f"{life_yrs}-Year Cumulative Cash Flow (EGP M)",
                **PLOTLY_THEME, height=300,
            )
            st.plotly_chart(fig_cf, use_container_width=True)

            if npv > 0 and payback < 15:
                st.success(
                    f"✅ **Investment Recommended** — {gov_sel} under **{risk}** assumptions "
                    f"shows {payback:.1f}-year payback and positive NPV of EGP {npv:.1f}M."
                )
            else:
                st.warning(
                    f"⚠️ Under **{risk}** assumptions, payback is {payback:.1f} years. "
                    "Consider reviewing tariff or CapEx assumptions."
                )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: FULL RANKINGS
# ═════════════════════════════════════════════════════════════════════════════
elif "Rankings" in page:
    st.markdown('<div class="section-title">📋 Full National Solar Rankings</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub arabic-sub">ترتيب جميع محافظات مصر الـ27 حسب درجة الموقع الشمسي</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    min_r  = c1.slider("Min Score", 0, 100, 0)
    rec_f  = c2.multiselect(
        "Investment Status",
        ["Strongly Recommended","Recommended","Neutral","Not Recommended"],
        default=["Strongly Recommended","Recommended","Neutral","Not Recommended"],
    )

    ranked = scores_df[
        (scores_df["solar_site_score"] >= min_r) &
        (scores_df["investment_rec"].isin(rec_f))
    ].sort_values("rank")

    # Waterfall bar
    fig_wf = go.Figure(go.Bar(
        x=ranked["governorate"],
        y=ranked["solar_site_score"],
        marker=dict(
            color=ranked["solar_site_score"],
            colorscale="RdYlGn",
            cmin=0, cmax=100,
            showscale=True,
            colorbar=dict(title="Score"),
        ),
        text=[f"{s:.1f}" for s in ranked["solar_site_score"]],
        textposition="outside",
    ))
    fig_wf.update_layout(
        title="National Solar Site Score Ranking (All Governorates)",
        **PLOTLY_THEME, height=400,
    )
    fig_wf.update_xaxes(tickangle=45)
    fig_wf.update_yaxes(range=[0, 108])
    st.plotly_chart(fig_wf, use_container_width=True)

    # Table
    disp = ranked[[
        "rank","governorate","region","solar_site_score","grade",
        "avg_solar_radiation","clearness_index","avg_temp_max",
        "avg_wind_speed","avg_humidity","avg_aqi","investment_rec",
    ]].rename(columns={
        "rank":                "#",
        "solar_site_score":    "Score",
        "avg_solar_radiation": "kWh/m²/day",
        "clearness_index":     "Clearness",
        "avg_temp_max":        "Temp Max°C",
        "avg_wind_speed":      "Wind m/s",
        "avg_humidity":        "Humidity%",
        "avg_aqi":             "AQI",
        "investment_rec":      "Recommendation",
    })
    st.dataframe(disp, use_container_width=True, hide_index=True)

    csv_bytes = ranked.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Rankings CSV",
        csv_bytes,
        "solariq_egypt_rankings.csv",
        "text/csv",
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: POWER BI LIVE SERVICE
# ═════════════════════════════════════════════════════════════════════════════
elif "Power BI" in page:
    st.markdown('<div class="section-title">📡 Power BI Live Service</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub arabic-sub">تقارير Power BI المباشرة — مدمجة من خدمة Microsoft السحابية</div>',
        unsafe_allow_html=True,
    )

    POWERBI_URL = (
        "https://app.powerbi.com/view"
        "?r=eyJrIjoiNzExOWU4ZmYtYWZlYS00NmIzLTk2ZDEtYTcwZDc2OWM0ZDA2IiwidCI6IjBmODNlYWRhLTJlYmYtNGYwOS1hYjUwLWM4ZjFlN2YyMDAzNyIsImMiOjh9"
    )

    # Toolbar mock
    st.markdown(f"""
    <div class="embed-frame">
        <div class="embed-toolbar">
            <div class="embed-dot" style="background:#FF5F57;"></div>
            <div class="embed-dot" style="background:#FEBC2E;margin:0 4px;"></div>
            <div class="embed-dot" style="background:#28C840;"></div>
            <span style="color:rgba(255,255,255,.6);font-size:.8rem;margin-left:12px;">
                Power BI Service — SolarIQ Egypt Report
            </span>
            <a href="{POWERBI_URL}" target="_blank"
               style="margin-left:auto;color:{COLORS['gold']};font-size:.78rem;
                      font-weight:700;text-decoration:none;">
                ↗ Open in Power BI
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_info, col_link = st.columns([3, 1])
    with col_info:
        st.markdown("""
        <div class="solar-card sky">
            <div style="font-weight:800;color:var(--navy);font-size:1rem;margin-bottom:10px;">
                📊 About This Report
            </div>
            <ul style="color:var(--slate);font-size:.875rem;line-height:1.9;padding-left:18px;">
                <li><strong>15 interactive dashboards</strong> covering solar potential, seasonality,
                    dust impact, agriculture, tourism, and construction feasibility</li>
                <li>Data: <strong>217K weather records</strong> across 27 Egyptian governorates (1981–2025)</li>
                <li>Fully filterable by <strong>Year, Region, Governorate, Season</strong></li>
                <li>Includes <strong>Solar Site Score</strong> composite ranking model</li>
                <li>Advanced DAX measures with <strong>TREATAS, RANKX, ALLSELECTED</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_link:
        st.markdown(f"""
        <div class="solar-card gold" style="text-align:center;padding:28px 16px;">
            <div style="font-size:2.2rem;">📡</div>
            <div style="font-weight:800;color:var(--navy);margin:10px 0 6px;">Power BI Live</div>
            <div style="font-size:.78rem;color:var(--muted);margin-bottom:14px;">
                Embedded interactive report
            </div>
            <a href="{POWERBI_URL}" target="_blank"
               style="display:inline-block;background:linear-gradient(135deg,{COLORS['gold']},{COLORS['gold_dark']});
                      color:{COLORS['navy']};font-weight:800;padding:10px 22px;
                      border-radius:10px;text-decoration:none;font-size:.85rem;">
                Open Full Report ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Embed iframe
    st.markdown("<br>", unsafe_allow_html=True)
    st.components.v1.iframe(
        src=POWERBI_URL,
        height=680,
        scrolling=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: TABLEAU ENVIRONMENTAL
# ═════════════════════════════════════════════════════════════════════════════
elif "Tableau" in page:
    st.markdown('<div class="section-title">🌿 Tableau Environmental Sync</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub arabic-sub">لوحات الطقس وجودة الهواء — مدمجة من Tableau Public</div>',
        unsafe_allow_html=True,
    )

    TABLEAU_URL = (
        "https://public.tableau.com/views/SolarIQ/AirQualityPublicHealthMonitoring"
        "?:showVizHome=no&:embed=true"
    )

    st.markdown(f"""
    <div class="embed-frame">
        <div class="embed-toolbar">
            <div class="embed-dot" style="background:#FF5F57;"></div>
            <div class="embed-dot" style="background:#FEBC2E;margin:0 4px;"></div>
            <div class="embed-dot" style="background:#28C840;"></div>
            <span style="color:rgba(255,255,255,.6);font-size:.8rem;margin-left:12px;">
                Tableau Public — Air Quality &amp; Public Health Monitoring
            </span>
            <a href="{TABLEAU_URL}" target="_blank"
               style="margin-left:auto;color:{COLORS['sky']};font-size:.78rem;
                      font-weight:700;text-decoration:none;">
                ↗ Open in Tableau
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("""
        <div class="solar-card sky">
            <div style="font-weight:800;color:var(--navy);font-size:1rem;margin-bottom:10px;">
                🌿 About This Tableau Dashboard
            </div>
            <ul style="color:var(--slate);font-size:.875rem;line-height:1.9;padding-left:18px;">
                <li>Air Quality Index (AQI) monitoring across Egyptian governorates</li>
                <li>PM2.5 and PM10 particulate matter trends</li>
                <li>Public health alert days count by governorate and season</li>
                <li>Pollution vs Solar Efficiency correlation analysis</li>
                <li>Data synced from <strong>Open-Meteo Air Quality API</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="solar-card green" style="text-align:center;padding:28px 16px;">
            <div style="font-size:2.2rem;">🌿</div>
            <div style="font-weight:800;color:var(--navy);margin:10px 0 6px;">Tableau Public</div>
            <div style="font-size:.78rem;color:var(--muted);margin-bottom:14px;">
                Environmental monitoring
            </div>
            <a href="{TABLEAU_URL}" target="_blank"
               style="display:inline-block;background:linear-gradient(135deg,{COLORS['teal']},{COLORS['sky_dark']});
                      color:{COLORS['white']};font-weight:800;padding:10px 22px;
                      border-radius:10px;text-decoration:none;font-size:.85rem;">
                Open Full View ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.components.v1.iframe(
        src=TABLEAU_URL,
        height=700,
        scrolling=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SSRS REPORTS
# ═════════════════════════════════════════════════════════════════════════════
elif "SSRS" in page:
    st.markdown('<div class="section-title">📄 SSRS Reports</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub arabic-sub">التقارير المرقّمة القابلة للطباعة — SQL Server Reporting Services</div>',
        unsafe_allow_html=True,
    )

    # Placeholder — add your SSRS link when ready
    SSRS_URL = ""   # ← أضف رابط SSRS هنا

    st.markdown("""
    <div class="solar-card gold">
        <div style="font-size:1.4rem;font-weight:900;color:var(--navy);margin-bottom:6px;">
            📋 About SSRS Reports
        </div>
        <p style="color:var(--slate);font-size:.875rem;line-height:1.8;">
            SQL Server Reporting Services (SSRS) provides pixel-perfect, printable PDF reports
            for boardroom presentations and investor packages. These reports are generated
            on-demand from the SolarIQ SQL Server data warehouse.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Report catalog
    reports = [
        ("📊", "Executive Solar Summary",    "One-page national summary — top 10 governorates, grades, investment recommendations",     "Monthly"),
        ("🌡️", "Temperature Impact Report", "Detailed temperature penalty analysis by governorate and season",                         "Quarterly"),
        ("🌫️", "Dust & Air Quality Report", "Annual energy loss from dust and pollution — per MW financial impact",                    "Monthly"),
        ("💰", "Investment Priority Report", "Ranked investment opportunities with ROI estimates — for fund managers",                  "Quarterly"),
        ("🌾", "Agricultural Climate Report","Climate risk assessment for each governorate — hot days, humidity, extreme rain",         "Annual"),
        ("📅", "Seasonal Performance",       "Month-by-month solar generation forecast for all 27 governorates",                       "Annual"),
    ]

    cols = st.columns(2)
    for i, (icon, title, desc, freq) in enumerate(reports):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="solar-card {'gold' if i%2==0 else 'sky'}"
                 style="display:flex;gap:16px;align-items:flex-start;">
                <div style="font-size:2rem;flex-shrink:0;">{icon}</div>
                <div>
                    <div style="font-weight:800;color:var(--navy);font-size:.95rem;margin-bottom:4px;">
                        {title}
                    </div>
                    <div style="font-size:.8rem;color:var(--muted);margin-bottom:8px;">{desc}</div>
                    <span class="pill pill-{'gold' if i%2==0 else 'sky'}">🔄 {freq}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if SSRS_URL:
        st.markdown(f"""
        <div class="embed-frame">
            <div class="embed-toolbar">
                <div class="embed-dot" style="background:#FF5F57;"></div>
                <div class="embed-dot" style="background:#FEBC2E;margin:0 4px;"></div>
                <div class="embed-dot" style="background:#28C840;"></div>
                <span style="color:rgba(255,255,255,.6);font-size:.8rem;margin-left:12px;">
                    SSRS Report Server — SolarIQ Egypt
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.iframe(src=SSRS_URL, height=700, scrolling=True)
    else:
        st.markdown("""
        <div style="background:var(--canvas);border:2px dashed var(--border);border-radius:16px;
                    padding:48px;text-align:center;margin-top:16px;">
            <div style="font-size:3rem;">📄</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--navy);margin:12px 0 6px;">
                SSRS Link Pending
            </div>
            <div style="font-size:.875rem;color:var(--muted);max-width:400px;margin:0 auto;">
                Add your SSRS report server URL in the <code>SSRS_URL</code> variable
                at the top of this page. The report will embed automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.info(
            "**How to add your SSRS link:**\n\n"
            "1. Open `streamlit_app.py` and find `SSRS_URL = \"\"`\n"
            "2. Replace it with your SSRS report URL, e.g.:\n"
            "   `SSRS_URL = \"http://your-server/Reports/...\"`\n"
            "3. Save and refresh — the report will embed automatically."
        )
