import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ================= CONFIG =================
st.set_page_config(page_title="Smart Dashboard", layout="wide")

# ================= DARK UI =================
st.markdown("""
<style>
.stApp { background-color: #0b1220; color: white; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* KPI cards */
.kpi {
    background: #111827;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

/* Buttons */
.back-btn {
    position: fixed;
    top: 15px;
    right: 20px;
    background-color: #2563eb;
    color: white;
    padding: 10px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= PATH =================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "current_dataset.txt")

# ================= GET DATASET =================
dataset_path = None

query_params = st.query_params
if "dataset" in query_params:
    dataset_path = query_params["dataset"]

if not dataset_path and os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        dataset_path = f.read().strip()

if not dataset_path:
    uploads_folder = os.path.join(BASE_DIR, "uploads")
    if os.path.exists(uploads_folder):
        files = [
            os.path.join(uploads_folder, f)
            for f in os.listdir(uploads_folder)
            if f.endswith((".csv", ".xlsx"))
        ]
        if files:
            dataset_path = max(files, key=os.path.getctime)

# ================= VALIDATION =================
if not dataset_path or not os.path.exists(dataset_path):
    st.error("❌ No dataset available")
    st.stop()

# ================= LOAD =================
if dataset_path.endswith(".csv"):
    df = pd.read_csv(dataset_path)
else:
    df = pd.read_excel(dataset_path)

filename = os.path.basename(dataset_path)

col_btn1, col_btn2 = st.columns([9, 1])

with col_btn2:
    if st.button("⬅ AI Mode"):
        st.markdown(
            """<meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/ai">""",
            unsafe_allow_html=True
        )

# ================= SIDEBAR FILTERS =================
st.sidebar.title("📊 Filters")

df_filtered = df.copy()

cat_cols = df.select_dtypes(include="object").columns
for col in cat_cols:
    selected = st.sidebar.multiselect(col, df[col].dropna().unique())
    if selected:
        df_filtered = df_filtered[df_filtered[col].isin(selected)]

num_cols = df.select_dtypes(include="number").columns
for col in num_cols:
    min_val = float(df[col].min())
    max_val = float(df[col].max())

    selected = st.sidebar.slider(col, min_val, max_val, (min_val, max_val))

    df_filtered = df_filtered[
        (df_filtered[col] >= selected[0]) &
        (df_filtered[col] <= selected[1])
    ]

# ================= MAIN TITLE =================
st.title("🚀 Smart Analytics Dashboard")
st.caption(f"Dataset: {filename}")

num_cols = df_filtered.select_dtypes(include="number").columns
cat_cols = df_filtered.select_dtypes(include="object").columns

# ================= KPI ROW =================
st.markdown("### 📌 Key Insights")

if len(num_cols) > 0:
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown(f"<div class='kpi'><h4>{num_cols[0]}</h4><h2>{round(df_filtered[num_cols[0]].mean(),2)}</h2></div>", unsafe_allow_html=True)

    if len(num_cols) > 1:
        k2.markdown(f"<div class='kpi'><h4>{num_cols[1]}</h4><h2>{round(df_filtered[num_cols[1]].mean(),2)}</h2></div>", unsafe_allow_html=True)

    if len(num_cols) > 2:
        k3.markdown(f"<div class='kpi'><h4>{num_cols[2]}</h4><h2>{round(df_filtered[num_cols[2]].mean(),2)}</h2></div>", unsafe_allow_html=True)

    if len(num_cols) > 3:
        k4.markdown(f"<div class='kpi'><h4>{num_cols[3]}</h4><h2>{round(df_filtered[num_cols[3]].mean(),2)}</h2></div>", unsafe_allow_html=True)

# ================= CHART LAYOUT =================
st.markdown("### 📊 Visual Analysis")

col1, col2 = st.columns(2)

# BAR CHART
if len(cat_cols) > 0 and len(num_cols) > 0:
    grouped = df_filtered.groupby(cat_cols[0])[num_cols[0]].mean().reset_index()

    fig1 = px.bar(grouped, x=cat_cols[0], y=num_cols[0], color=num_cols[0])
    fig1.update_layout(plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", font_color="white")

    col1.plotly_chart(fig1, use_container_width=True)

# DISTRIBUTION
if len(num_cols) > 0:
    fig2 = px.histogram(df_filtered, x=num_cols[0], marginal="box")
    fig2.update_layout(plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", font_color="white")

    col2.plotly_chart(fig2, use_container_width=True)

# ================= SECOND ROW =================
col3, col4 = st.columns(2)

# CORRELATION
if len(num_cols) >= 2:
    corr = df_filtered[num_cols].corr()

    fig3 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu")
    fig3.update_layout(plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", font_color="white")

    col3.plotly_chart(fig3, use_container_width=True)

# SCATTER
if len(num_cols) >= 2:
    fig4 = px.scatter(df_filtered, x=num_cols[0], y=num_cols[1])
    fig4.update_layout(plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", font_color="white")

    col4.plotly_chart(fig4, use_container_width=True)

st.markdown("### 🧠 Insights")

# ================= SAFE NUMERIC =================
if len(num_cols) > 0:
    col = num_cols[0]

    if not df_filtered.empty and df_filtered[col].dropna().shape[0] > 0:
        avg_val = df_filtered[col].mean()
        st.success(f"Average {col}: {round(avg_val, 2)}")
    else:
        st.warning(f"No valid data for {col}")

# ================= SAFE CATEGORICAL =================
if len(cat_cols) > 0:
    col = cat_cols[0]

    if not df_filtered.empty:
        vc = df_filtered[col].dropna().value_counts()

        if not vc.empty:
            st.success(f"Top {col}: {vc.idxmax()}")
        else:
            st.warning(f"No valid category data for {col}")
    else:
        st.warning("No data after applying filters")