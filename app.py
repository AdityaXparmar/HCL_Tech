import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VehicleIQ Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Light Theme CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #f5f3ef;
    color: #1a1a2e;
}

h1, h2, h3, h4 {
    font-family: 'Fraunces', serif !important;
    font-weight: 700 !important;
}

.stApp {
    background: linear-gradient(145deg, #f5f3ef 0%, #ede8e0 40%, #f0ece4 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #faf8f4 100%);
    border-right: 1.5px solid #e2d9cc;
    box-shadow: 2px 0 20px rgba(139,109,56,0.06);
}
section[data-testid="stSidebar"] * { color: #3d3530 !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #7a6a5a !important; }

.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1.5px solid #e8dfd2;
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 4px 20px rgba(139,109,56,0.07), 0 1px 4px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(139,109,56,0.12);
}
[data-testid="metric-container"] label {
    color: #9e8c7b !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #2d5a27 !important;
    font-family: 'Fraunces', serif !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    background: #f0ece4;
    border-radius: 14px;
    padding: 4px;
    border: 1.5px solid #e2d9cc;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #7a6a5a !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    padding: 8px 18px;
    font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #2d5a27 !important;
    box-shadow: 0 2px 8px rgba(45,90,39,0.12);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2d5a27, #3d7a35);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s ease;
    box-shadow: 0 3px 12px rgba(45,90,39,0.2);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(45,90,39,0.3);
}

/* Upload area */
[data-testid="stFileUploader"] {
    border: 2px dashed #c8bfb0;
    border-radius: 14px;
    background: rgba(255,255,255,0.6);
    padding: 0.8rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: #2d5a27; }

/* Select boxes */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #ffffff !important;
    border: 1.5px solid #e2d9cc !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}

/* Radio */
.stRadio > div { gap: 8px; }
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #3d3530 !important;
    font-weight: 500;
}

/* Sliders */
.stSlider [data-baseweb="slider"] { color: #2d5a27 !important; }

/* Alerts */
.stAlert {
    border-radius: 12px;
    border-left: 4px solid #2d5a27;
    background: rgba(45,90,39,0.06);
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #ffffff 0%, #f7f4ef 60%, #eef5ec 100%);
    border: 1.5px solid #ddd5c8;
    border-radius: 22px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 6px 30px rgba(139,109,56,0.08);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(45,90,39,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(184,142,70,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: #1a2e1a;
    margin: 0;
    line-height: 1.1;
}
.hero-title span { color: #2d5a27; }
.hero-sub { color: #7a6a5a; font-size: 1rem; margin-top: 0.5rem; }
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #2d5a27, #3d7a35);
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

.section-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    color: #9e8c7b;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1.5px solid #e8dfd2;
}

.insight-card {
    background: linear-gradient(135deg, #f0f7ee, #e8f5e3);
    border: 1.5px solid #c5dfc0;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin: 0.4rem 0;
    box-shadow: 0 2px 8px rgba(45,90,39,0.06);
}
.insight-card p { margin: 0; font-size: 0.88rem; color: #2a5025; font-weight: 500; }

hr { border-color: #e2d9cc !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1.5px solid #e2d9cc;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

/* Logo area */
.sidebar-logo {
    text-align: center;
    padding: 1.2rem 0 0.8rem;
}
.sidebar-logo-title {
    font-family: 'Fraunces', serif;
    font-size: 1.6rem;
    font-weight: 900;
    color: #2d5a27 !important;
}
.sidebar-logo-sub {
    color: #9e8c7b !important;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    font-weight: 600;
    text-transform: uppercase;
}

/* Chip / tag style */
.chip {
    display: inline-block;
    background: #eef5ec;
    border: 1px solid #c5dfc0;
    color: #2d5a27;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 3px 10px;
    margin: 2px;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #2d5a27, #3d7a35) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 12px rgba(45,90,39,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Plotly light theme ───────────────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fafaf7",
        font=dict(family="Plus Jakarta Sans", color="#3d3530"),
        title_font=dict(family="Fraunces", color="#1a2e1a", size=16),
        xaxis=dict(
            gridcolor="#ede8e0",
            linecolor="#d5cdc2",
            zerolinecolor="#d5cdc2",
            tickfont=dict(color="#7a6a5a"),
        ),
        yaxis=dict(
            gridcolor="#ede8e0",
            linecolor="#d5cdc2",
            zerolinecolor="#d5cdc2",
            tickfont=dict(color="#7a6a5a"),
        ),
        colorway=["#2d5a27","#b88e46","#4a90d9","#c04a3f","#7a5fa0","#4aada0","#d4742a","#7aa832"],
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2d9cc",
            borderwidth=1.5,
            font=dict(color="#3d3530"),
        ),
        margin=dict(l=40, r=20, t=50, b=40),
    )
)

COLORS = {
    "primary":   "#2d5a27",
    "secondary": "#b88e46",
    "accent":    "#4a90d9",
    "success":   "#3a8c32",
    "warning":   "#d4742a",
    "danger":    "#c04a3f",
    "gradient":  ["#2d5a27","#b88e46","#4a90d9","#c04a3f","#7a5fa0","#4aada0","#d4742a","#7aa832"],
    "green_seq": ["#eef5ec","#c5dfc0","#8abe82","#3d7a35","#1e4a1a"],
}

def apply_theme(fig, height=420):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=height)
    return fig

# ─── Data Helpers ─────────────────────────────────────────────────────────────
def load_data(file):
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        df.drop_duplicates(inplace=True)
        return df, None
    except Exception as e:
        return None, str(e)

def safe_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def numeric_cols(df):  return df.select_dtypes(include=np.number).columns.tolist()
def cat_cols(df):      return df.select_dtypes(include="object").columns.tolist()

def metric_row(cols_data):
    cols = st.columns(len(cols_data))
    for col, (label, val, delta) in zip(cols, cols_data):
        with col:
            st.metric(label, val, delta)

@st.cache_data
def generate_sample_data(n=500):
    np.random.seed(42)
    fuel_types    = np.random.choice(["Petrol","Diesel","Electric","Hybrid"], n, p=[0.4,0.35,0.1,0.15])
    transmissions = np.random.choice(["Automatic","Manual","CVT"], n, p=[0.5,0.35,0.15])
    tire_cond     = np.random.choice(["Good","Fair","Poor"], n, p=[0.5,0.35,0.15])
    brake_cond    = np.random.choice(["Good","Fair","Poor"], n, p=[0.55,0.3,0.15])
    vehicle_age   = np.random.randint(1, 16, n)
    mileage       = vehicle_age * np.random.uniform(8000, 15000, n) + np.random.normal(0, 5000, n)
    mileage       = np.clip(mileage, 500, 200000)
    engine_size   = np.random.choice([1.0,1.2,1.4,1.6,1.8,2.0,2.5,3.0], n)
    fuel_eff      = 35 - engine_size*3 + np.random.normal(0, 3, n)
    fuel_eff      = np.clip(fuel_eff, 10, 55)
    last_service  = np.random.randint(0, 24, n)
    owner_count   = np.random.randint(1, 5, n)
    need_maint    = ((last_service > 12) | (tire_cond == "Poor") | (brake_cond == "Poor")).astype(int)
    return pd.DataFrame({
        "vehicle_age": vehicle_age, "mileage": mileage.astype(int),
        "engine_size": engine_size, "fuel_type": fuel_types,
        "transmission_type": transmissions, "tire_condition": tire_cond,
        "brake_condition": brake_cond, "fuel_efficiency": fuel_eff.round(1),
        "last_service_months_ago": last_service, "owner_count": owner_count,
        "need_maintenance": need_maint,
    })

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <div style='font-size:2rem; margin-bottom:4px;'>🚗</div>
        <div class='sidebar-logo-title'>VehicleIQ</div>
        <div class='sidebar-logo-sub'>Analytics Platform</div>
    </div>
    <hr style='margin: 0.8rem 0; border-color:#e2d9cc;'>
    """, unsafe_allow_html=True)

    st.markdown("**📂 Data Source**")
    uploaded = st.file_uploader("Upload CSV File", type=["csv"], help="Upload your vehicle maintenance dataset")
    if uploaded is None:
        use_sample = st.checkbox("Use sample dataset", value=True)
    else:
        use_sample = False

    st.markdown("<hr style='border-color:#e2d9cc;margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("**🗂 Navigation**")
    page = st.radio("", [
        "🏠  Overview",
        "📊  Distribution Analysis",
        "🔬  Feature Relationships",
        "🛠  Maintenance Insights",
        "🔥  Correlation Matrix",
        "🗃  Data Explorer",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#e2d9cc;margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#b0a090;text-align:center;'>
    VehicleIQ v2.0 &nbsp;·&nbsp; Streamlit + Plotly
    </div>
    """, unsafe_allow_html=True)

# ─── Load data ───────────────────────────────────────────────────────────────
if uploaded:
    df_raw, err = load_data(uploaded)
    if err:
        st.error(f"❌ Error loading file: {err}")
        st.stop()
    st.sidebar.success(f"✅ Loaded {len(df_raw):,} rows")
elif use_sample:
    df_raw = generate_sample_data()
    st.sidebar.info("🔄 Using sample data")
else:
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-badge'>Get Started</div>
        <div class='hero-title'>Vehicle<span>IQ</span> Analytics</div>
        <div class='hero-sub'>Upload a CSV file or enable the sample dataset to begin your analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = df_raw.copy()

# ─── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.markdown("<hr style='border-color:#e2d9cc;margin:1rem 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("**🎛 Global Filters**")

for c in cat_cols(df):
    if df[c].nunique() <= 10:
        vals = sorted(df[c].dropna().unique().tolist())
        sel  = st.sidebar.multiselect(c.replace("_"," ").title(), vals, default=vals, key=f"f_{c}")
        if sel:
            df = df[df[c].isin(sel)]

age_col = safe_col(df, ["vehicle_age","age"])
if age_col and df[age_col].nunique() > 1:
    mn, mx = int(df[age_col].min()), int(df[age_col].max())
    if mn < mx:
        rng = st.sidebar.slider("Vehicle Age Range", mn, mx, (mn, mx))
        df = df[(df[age_col] >= rng[0]) & (df[age_col] <= rng[1])]

st.sidebar.markdown(f"<span class='chip'>Rows: {len(df):,}</span>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-badge'>Live Dashboard</div>
        <div class='hero-title'>Fleet Intelligence <span>Overview</span></div>
        <div class='hero-sub'>Comprehensive vehicle maintenance analytics — powered by your data</div>
    </div>
    """, unsafe_allow_html=True)

    n_rows    = len(df)
    mileage_c = safe_col(df, ["mileage"])
    maint_c   = safe_col(df, ["need_maintenance"])
    eff_c     = safe_col(df, ["fuel_efficiency"])

    kpis = [("🚗 Total Vehicles", f"{n_rows:,}", None)]
    if mileage_c:
        kpis.append(("📍 Avg Mileage", f"{df[mileage_c].mean():,.0f} km", None))
    if maint_c:
        pct = df[maint_c].mean()*100
        kpis.append(("🛠 Needs Maintenance", f"{pct:.1f}%", f"{df[maint_c].sum():,} vehicles"))
    if eff_c:
        kpis.append(("⛽ Avg Fuel Efficiency", f"{df[eff_c].mean():.1f} mpg", None))

    metric_row(kpis)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("<div class='section-header'>Maintenance Status</div>", unsafe_allow_html=True)
        if maint_c:
            counts = df[maint_c].value_counts().reset_index()
            counts.columns = ["Status","Count"]
            counts["Status"] = counts["Status"].map({0:"✅ OK", 1:"🛠 Needs Service"})
            fig = px.pie(counts, names="Status", values="Count", hole=0.6,
                         color_discrete_sequence=["#2d5a27","#c04a3f"])
            fig.update_traces(
                textfont_size=13,
                marker=dict(line=dict(color="#f5f3ef", width=3))
            )
            fig.update_layout(
                legend=dict(orientation="h", y=-0.1),
                annotations=[dict(text=f"<b>{n_rows}</b><br>vehicles",
                                  x=0.5, y=0.5, font_size=14,
                                  font_color="#1a2e1a", showarrow=False)]
            )
            st.plotly_chart(apply_theme(fig, 340), use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Fleet by Fuel Type</div>", unsafe_allow_html=True)
        fuel_c = safe_col(df, ["fuel_type"])
        if fuel_c:
            vc = df[fuel_c].value_counts().reset_index()
            vc.columns = ["Fuel","Count"]
            fig = px.bar(vc, x="Fuel", y="Count",
                         color="Fuel",
                         color_discrete_sequence=COLORS["gradient"],
                         text="Count")
            fig.update_traces(textposition="outside", textfont_size=12, marker_line_width=0)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Vehicles")
            st.plotly_chart(apply_theme(fig, 340), use_container_width=True)

    # Mileage area
    if age_col and mileage_c:
        st.markdown("<div class='section-header'>Average Mileage by Vehicle Age</div>", unsafe_allow_html=True)
        grp = df.groupby(age_col)[mileage_c].mean().reset_index()
        fig = px.area(grp, x=age_col, y=mileage_c,
                      color_discrete_sequence=["#2d5a27"],
                      labels={age_col:"Vehicle Age (yrs)", mileage_c:"Avg Mileage (km)"})
        fig.update_traces(fill="tozeroy", fillcolor="rgba(45,90,39,0.12)", line=dict(width=2.5))
        st.plotly_chart(apply_theme(fig, 300), use_container_width=True)

    # Transmission pie
    trans_c = safe_col(df, ["transmission_type"])
    if trans_c:
        st.markdown("<div class='section-header'>Transmission Type Split</div>", unsafe_allow_html=True)
        vc2 = df[trans_c].value_counts().reset_index()
        vc2.columns = ["Type","Count"]
        fig = px.bar(vc2, x="Count", y="Type", orientation="h",
                     color="Type", color_discrete_sequence=COLORS["gradient"],
                     text="Count")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Count")
        st.plotly_chart(apply_theme(fig, 240), use_container_width=True)

    # Insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>💡 Auto-Generated Insights</div>", unsafe_allow_html=True)
    insights = []
    if mileage_c and age_col:
        corr = df[[age_col, mileage_c]].corr().iloc[0,1]
        insights.append(f"Vehicle age and mileage share a <b>{corr:.2f}</b> correlation — {'strong positive' if corr > 0.7 else 'moderate'} relationship detected.")
    if maint_c:
        pct = df[maint_c].mean()*100
        insights.append(f"<b>{pct:.1f}%</b> of the fleet ({df[maint_c].sum():,} vehicles) currently requires maintenance intervention.")
    if fuel_c and maint_c:
        worst = df.groupby(fuel_c)[maint_c].mean().idxmax()
        insights.append(f"<b>{worst}</b> vehicles show the highest maintenance rate among all fuel types — prioritise inspection.")
    for ins in insights:
        st.markdown(f"<div class='insight-card'><p>➤ {ins}</p></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Distribution Analysis":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='hero-title' style='font-size:2rem;margin-bottom:1.5rem;color:#1a2e1a;'>Distribution Analysis</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Histogram", "📦 Box Plots", "🎻 Violin Plots"])
    num = numeric_cols(df)

    with tab1:
        c1, c2, c3 = st.columns(3)
        col_sel  = c1.selectbox("Numeric column", num, key="hist_col")
        color_by = c2.selectbox("Color by", ["None"]+cat_cols(df), key="hist_color")
        bins     = c3.slider("Bins", 10, 80, 30)
        fig = px.histogram(df, x=col_sel,
                           color=None if color_by=="None" else color_by,
                           nbins=bins, marginal="box",
                           color_discrete_sequence=COLORS["gradient"],
                           opacity=0.8,
                           labels={col_sel: col_sel.replace("_"," ").title()})
        fig.update_layout(bargap=0.05)
        st.plotly_chart(apply_theme(fig, 500), use_container_width=True)

    with tab2:
        c1, c2, c3 = st.columns(3)
        y_col  = c1.selectbox("Numeric (Y)", num, key="box_y")
        x_col  = c2.selectbox("Category (X)", ["None"]+cat_cols(df), key="box_x")
        color_b= c3.selectbox("Color by", ["None"]+cat_cols(df), key="box_c")
        fig = px.box(df, x=None if x_col=="None" else x_col, y=y_col,
                     color=None if color_b=="None" else color_b,
                     color_discrete_sequence=COLORS["gradient"],
                     points="outliers",
                     labels={y_col: y_col.replace("_"," ").title()})
        st.plotly_chart(apply_theme(fig, 500), use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        y_col2 = c1.selectbox("Numeric (Y)", num, key="vio_y")
        x_col2 = c2.selectbox("Category (X)", ["None"]+cat_cols(df), key="vio_x")
        fig = px.violin(df, x=None if x_col2=="None" else x_col2, y=y_col2,
                        box=True, points="all",
                        color=None if x_col2=="None" else x_col2,
                        color_discrete_sequence=COLORS["gradient"],
                        labels={y_col2: y_col2.replace("_"," ").title()})
        st.plotly_chart(apply_theme(fig, 500), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>📋 Descriptive Statistics</div>", unsafe_allow_html=True)
    desc = df[num].describe().T.round(2)
    desc["cv_%"] = (desc["std"]/desc["mean"]*100).round(1)
    st.dataframe(desc.style.background_gradient(cmap="YlGn", subset=["mean","std"]), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔬  Feature Relationships":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='hero-title' style='font-size:2rem;margin-bottom:1.5rem;color:#1a2e1a;'>Feature Relationships</div>", unsafe_allow_html=True)

    num  = numeric_cols(df)
    cats = cat_cols(df)

    tab1, tab2, tab3 = st.tabs(["🔵 Scatter", "📉 Regression", "🌐 3D Scatter"])

    with tab1:
        c1,c2,c3 = st.columns(3)
        x_  = c1.selectbox("X axis", num, key="sc_x")
        y_  = c2.selectbox("Y axis", num, index=min(1,len(num)-1), key="sc_y")
        col_= c3.selectbox("Color by", ["None"]+cats, key="sc_c")
        sz_ = c3.selectbox("Size by",  ["None"]+num,  key="sc_sz")
        fig = px.scatter(df, x=x_, y=y_,
                         color=None if col_=="None" else col_,
                         size=None if sz_=="None" else sz_,
                         color_discrete_sequence=COLORS["gradient"],
                         opacity=0.65)
        fig.update_traces(marker=dict(size=7, line=dict(width=0.8, color="rgba(255,255,255,0.6)")))
        st.plotly_chart(apply_theme(fig, 500), use_container_width=True)

    with tab2:
        c1,c2,c3 = st.columns(3)
        xr = c1.selectbox("X axis", num, key="reg_x")
        yr = c2.selectbox("Y axis", num, index=min(1,len(num)-1), key="reg_y")
        cr = c3.selectbox("Color by", ["None"]+cats, key="reg_c")
        fig = px.scatter(df, x=xr, y=yr,
                         color=None if cr=="None" else cr,
                         trendline="ols",
                         color_discrete_sequence=COLORS["gradient"],
                         opacity=0.55)
        st.plotly_chart(apply_theme(fig, 500), use_container_width=True)

    with tab3:
        if len(num) >= 3:
            c1,c2,c3,c4 = st.columns(4)
            x3  = c1.selectbox("X", num, key="3d_x")
            y3  = c2.selectbox("Y", num, index=1, key="3d_y")
            z3  = c3.selectbox("Z", num, index=2, key="3d_z")
            c3d = c4.selectbox("Color", ["None"]+cats, key="3d_c")
            fig = px.scatter_3d(df.sample(min(1000,len(df))), x=x3, y=y3, z=z3,
                                color=None if c3d=="None" else c3d,
                                color_discrete_sequence=COLORS["gradient"],
                                opacity=0.75, size_max=8)
            fig.update_layout(scene=dict(
                bgcolor="#fafaf7",
                xaxis=dict(backgroundcolor="#f5f3ef", gridcolor="#e2d9cc"),
                yaxis=dict(backgroundcolor="#f5f3ef", gridcolor="#e2d9cc"),
                zaxis=dict(backgroundcolor="#f5f3ef", gridcolor="#e2d9cc"),
            ))
            st.plotly_chart(apply_theme(fig, 540), use_container_width=True)
        else:
            st.info("Need at least 3 numeric columns for 3D scatter.")

    st.markdown("---")
    st.markdown("<div class='section-header'>Pair Plot (Sampled)</div>", unsafe_allow_html=True)
    pair_cols = st.multiselect("Select columns (2-5)", num, default=num[:min(4,len(num))])
    if len(pair_cols) >= 2:
        color_pair = st.selectbox("Color by", ["None"]+cats, key="pair_c")
        sample_df  = df.sample(min(600,len(df)))
        fig = px.scatter_matrix(sample_df, dimensions=pair_cols,
                                color=None if color_pair=="None" else color_pair,
                                color_discrete_sequence=COLORS["gradient"],
                                opacity=0.55)
        fig.update_traces(diagonal_visible=False, showupperhalf=False, marker=dict(size=3))
        st.plotly_chart(apply_theme(fig, 600), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🛠  Maintenance Insights":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='hero-title' style='font-size:2rem;margin-bottom:1.5rem;color:#1a2e1a;'>Maintenance Intelligence</div>", unsafe_allow_html=True)

    maint_c = safe_col(df, ["need_maintenance"])
    if maint_c is None:
        st.warning("No 'need_maintenance' column found.")
        st.stop()

    df_m = df.copy()
    df_m["Maintenance"] = df_m[maint_c].map({0:"✅ No Action", 1:"🛠 Needs Service"})
    cats = cat_cols(df_m)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 By Category","📈 Age & Mileage","🔍 Risk Profile","📋 Summary Table"])

    with tab1:
        cat_sel = st.selectbox("Group by", [c for c in cats if c not in [maint_c,"Maintenance"]], key="mc_cat")
        grp = df_m.groupby([cat_sel,"Maintenance"]).size().reset_index(name="Count")
        fig = px.bar(grp, x=cat_sel, y="Count", color="Maintenance", barmode="group",
                     color_discrete_map={"✅ No Action":"#2d5a27","🛠 Needs Service":"#c04a3f"})
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(apply_theme(fig, 400), use_container_width=True)

        rate = df_m.groupby(cat_sel)[maint_c].mean().mul(100).round(1).reset_index()
        rate.columns = [cat_sel,"Maintenance Rate (%)"]
        rate = rate.sort_values("Maintenance Rate (%)", ascending=False)
        fig2 = px.bar(rate, x=cat_sel, y="Maintenance Rate (%)",
                      color="Maintenance Rate (%)",
                      color_continuous_scale=["#2d5a27","#d4742a","#c04a3f"],
                      text="Maintenance Rate (%)")
        fig2.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(apply_theme(fig2, 360), use_container_width=True)

    with tab2:
        age_c = safe_col(df_m, ["vehicle_age","age"])
        mil_c = safe_col(df_m, ["mileage"])
        if age_c:
            mba = df_m.groupby(age_c)[maint_c].mean().mul(100).round(1).reset_index()
            mba.columns = [age_c,"Maintenance Rate (%)"]
            fig = px.line(mba, x=age_c, y="Maintenance Rate (%)",
                          markers=True, color_discrete_sequence=["#b88e46"])
            fig.update_traces(line=dict(width=3), marker=dict(size=9, color="#c04a3f", line=dict(width=2, color="white")))
            fig.add_hrect(y0=50, y1=100, fillcolor="rgba(192,74,63,0.05)", line_width=0)
            st.plotly_chart(apply_theme(fig, 360), use_container_width=True)
        if mil_c:
            df_m["mileage_bin"] = pd.cut(df_m[mil_c], bins=8)
            mb = df_m.groupby("mileage_bin")[maint_c].mean().mul(100).round(1).reset_index()
            mb["mileage_bin"] = mb["mileage_bin"].astype(str)
            fig2 = px.bar(mb, x="mileage_bin", y=maint_c,
                          color=maint_c,
                          color_continuous_scale=["#2d5a27","#d4742a","#c04a3f"],
                          labels={maint_c:"Maintenance Rate (%)"})
            fig2.update_coloraxes(showscale=False)
            fig2.update_traces(marker_line_width=0)
            st.plotly_chart(apply_theme(fig2, 360), use_container_width=True)

    with tab3:
        tire_c  = safe_col(df_m, ["tire_condition"])
        brake_c = safe_col(df_m, ["brake_condition"])
        if tire_c and brake_c:
            pivot = df_m.pivot_table(values=maint_c, index=tire_c, columns=brake_c, aggfunc="mean").mul(100).round(1)
            fig = px.imshow(pivot, text_auto=True, aspect="auto",
                            color_continuous_scale=["#eef5ec","#d4742a","#c04a3f"],
                            labels=dict(color="Maint. Rate %"))
            fig.update_layout(title="Risk Matrix — Tire vs Brake Condition")
            st.plotly_chart(apply_theme(fig, 380), use_container_width=True)

        if tire_c:
            sb_cols = [c for c in [safe_col(df_m,["fuel_type"]), tire_c] if c]
            if sb_cols:
                sb_data = df_m.groupby(sb_cols+["Maintenance"]).size().reset_index(name="Count")
                fig2 = px.sunburst(sb_data, path=sb_cols+["Maintenance"], values="Count",
                                   color="Maintenance",
                                   color_discrete_map={"✅ No Action":"#2d5a27","🛠 Needs Service":"#c04a3f"})
                st.plotly_chart(apply_theme(fig2, 450), use_container_width=True)

    with tab4:
        cats_for_t = [c for c in cats if c not in [maint_c,"Maintenance"]]
        rows = []
        for c in cats_for_t:
            grp = df_m.groupby(c)[maint_c].agg(["sum","count","mean"]).reset_index()
            grp.columns = [c,"needs","total","rate"]
            grp["rate"] = (grp["rate"]*100).round(1)
            for _, row in grp.iterrows():
                rows.append({
                    "Category": c.replace("_"," ").title(),
                    "Value": row[c], "Total": int(row["total"]),
                    "Needs Maintenance": int(row["needs"]),
                    "Rate (%)": row["rate"],
                    "Risk": "🔴 High" if row["rate"]>50 else ("🟡 Medium" if row["rate"]>25 else "🟢 Low"),
                })
        if rows:
            st.dataframe(pd.DataFrame(rows).sort_values("Rate (%)", ascending=False),
                         use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔥  Correlation Matrix":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='hero-title' style='font-size:2rem;margin-bottom:1.5rem;color:#1a2e1a;'>Correlation Matrix</div>", unsafe_allow_html=True)

    num = numeric_cols(df)
    if len(num) < 2:
        st.warning("Need at least 2 numeric columns.")
        st.stop()

    col_sel = st.multiselect("Select columns", num, default=num)
    if len(col_sel) < 2:
        st.info("Select at least 2 columns.")
        st.stop()

    method = st.radio("Correlation method", ["pearson","spearman","kendall"], horizontal=True)
    corr = df[col_sel].corr(method=method).round(3)

    tab1, tab2 = st.tabs(["🌡 Heatmap","📊 Top Correlations"])

    with tab1:
        mask = np.triu(np.ones_like(corr), k=1).astype(bool)
        corr_l = corr.copy(); corr_l[mask] = None
        fig = px.imshow(corr_l, text_auto=True, aspect="auto",
                        color_continuous_scale=["#c04a3f","#f5f3ef","#2d5a27"],
                        zmin=-1, zmax=1, labels=dict(color="Correlation"))
        fig.update_layout(title=f"{method.title()} Correlation Matrix")
        fig.update_traces(textfont_size=11)
        st.plotly_chart(apply_theme(fig, 560), use_container_width=True)

    with tab2:
        pairs = corr.unstack().reset_index()
        pairs.columns = ["Feature A","Feature B","Correlation"]
        pairs = pairs[pairs["Feature A"] < pairs["Feature B"]].dropna()
        pairs["Abs"] = pairs["Correlation"].abs()
        pairs = pairs.sort_values("Abs", ascending=False).head(20)
        pairs["Pair"] = pairs["Feature A"] + " × " + pairs["Feature B"]
        pairs["Direction"] = pairs["Correlation"].apply(lambda x: "Positive" if x>0 else "Negative")
        fig = px.bar(pairs, x="Correlation", y="Pair", orientation="h",
                     color="Direction",
                     color_discrete_map={"Positive":"#2d5a27","Negative":"#c04a3f"},
                     text=pairs["Correlation"].round(3))
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(apply_theme(fig, max(400,len(pairs)*28)), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>Top 4 Strongest Pairs — Scatter Plots</div>", unsafe_allow_html=True)
    top4 = pairs.head(4)
    c1, c2 = st.columns(2)
    for i, (_, row) in enumerate(top4.iterrows()):
        fig = px.scatter(df, x=row["Feature A"], y=row["Feature B"],
                         opacity=0.45, color_discrete_sequence=["#2d5a27"],
                         trendline="ols")
        fig.update_traces(selector=dict(mode="markers"), marker=dict(size=5))
        (c1 if i%2==0 else c2).plotly_chart(apply_theme(fig, 320), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗃  Data Explorer":
# ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='hero-title' style='font-size:2rem;margin-bottom:1.5rem;color:#1a2e1a;'>Data Explorer</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Browse Data","🔎 Column Profiler","💾 Export"])

    with tab1:
        search = st.text_input("🔍 Search any value (across string columns)")
        disp = df.copy()
        if search:
            mask = pd.Series([False]*len(disp), index=disp.index)
            for c in cat_cols(disp):
                mask |= disp[c].astype(str).str.contains(search, case=False, na=False)
            disp = disp[mask]
        st.markdown(f"**Showing** `{len(disp):,}` rows × `{len(disp.columns)}` columns")
        st.dataframe(disp, use_container_width=True, height=420)

    with tab2:
        col_p = st.selectbox("Column to profile", df.columns.tolist())
        col_data = df[col_p].dropna()

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Count",  f"{len(col_data):,}")
        m2.metric("Nulls",  f"{df[col_p].isnull().sum():,}")
        m3.metric("Unique", f"{col_data.nunique():,}")
        m4.metric("Type",   str(col_data.dtype))

        if pd.api.types.is_numeric_dtype(col_data):
            m5,m6,m7,m8 = st.columns(4)
            m5.metric("Min",     f"{col_data.min():.2f}")
            m6.metric("Max",     f"{col_data.max():.2f}")
            m7.metric("Mean",    f"{col_data.mean():.2f}")
            m8.metric("Std Dev", f"{col_data.std():.2f}")

            fig = make_subplots(rows=1, cols=2, subplot_titles=("Distribution","Box Plot"))
            fig.add_trace(go.Histogram(x=col_data, nbinsx=30, marker_color="#2d5a27", opacity=0.8, name="Dist"), row=1, col=1)
            fig.add_trace(go.Box(y=col_data, marker_color="#b88e46", name="Box"), row=1, col=2)
            st.plotly_chart(apply_theme(fig, 380), use_container_width=True)
        else:
            vc = col_data.value_counts().head(20).reset_index()
            vc.columns = ["Value","Count"]
            fig = px.bar(vc, x="Value", y="Count",
                         color="Count",
                         color_continuous_scale=COLORS["green_seq"])
            fig.update_coloraxes(showscale=False)
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(apply_theme(fig, 380), use_container_width=True)

    with tab3:
        st.markdown("**Download filtered dataset**")
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_buf.getvalue(),
            file_name="vehicleiq_filtered.csv",
            mime="text/csv",
        )
        st.markdown(f"**File contains:** `{len(df):,}` rows × `{len(df.columns)}` columns")
        st.dataframe(df.head(5), use_container_width=True)