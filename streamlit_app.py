import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px
import os

load_dotenv()

#PAGE CONFIG
st.set_page_config(
    page_title="MoPhones Credit Portfolio",
    layout="wide",
    page_icon=""
)

st.title("MoPhones Credit Portfolio Health Monitor")
st.markdown("### Real-time Credit Risk & Portfolio Dashboard")

#DATABASE CONNECTION
@st.cache_resource
def get_connection():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
    )
    return engine

engine = get_connection()
st.success("Connected to MoPhones Credit Database")

# Load basic data for sidebar
with engine.connect() as conn:
    df_loans = pd.read_sql("SELECT * FROM stg_loans", conn)
    df_customers = pd.read_sql("SELECT * FROM stg_customers", conn)
    df_kpis = pd.read_sql("SELECT * FROM mart_portfolio_kpis", conn)

#SIDEBAR
st.sidebar.success(f"Total Loans: **{len(df_loans):,}**")

st.sidebar.header("Filters")
device_options = ["All"] + sorted(df_loans['device_model'].unique().tolist())
selected_device = st.sidebar.selectbox("Device Model", device_options)

location_options = ["All"] + sorted(df_customers['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Location", location_options)

promo_filter = st.sidebar.radio("Promo Filter", ["All", "Promo Only", "Non-Promo"])

#  KPI CARDS
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("**Total Disbursed**", f"KES {df_kpis['total_disbursed'].iloc[0]:,}")

with col2:
    st.metric("**PAR30**", f"{df_kpis['PAR30'].iloc[0]}%")

with col3:
    st.metric("**PAR60**", f"{df_kpis['PAR60'].iloc[0]}%")

with col4:
    st.metric("**Avg Loan Size**", f"KES {df_kpis['avg_loan_size'].iloc[0]:,}")

st.divider()

# TOGGLE BUTTONS
col_a, col_b, col_c = st.columns(3)

if 'show_vintage' not in st.session_state:
    st.session_state.show_vintage = True
if 'show_risk' not in st.session_state:
    st.session_state.show_risk = False
if 'show_device' not in st.session_state:
    st.session_state.show_device = False

with col_a:
    if st.button("Vintage Analysis", use_container_width=True):
        st.session_state.show_vintage = not st.session_state.show_vintage

with col_b:
    if st.button("Risk Segmentation", use_container_width=True):
        st.session_state.show_risk = not st.session_state.show_risk

with col_c:
    if st.button("Device Performance", use_container_width=True):
        st.session_state.show_device = not st.session_state.show_device

# VINTAGE ANALYSIS 
if st.session_state.show_vintage:
    with st.expander("Vintage Analysis", expanded=True):
        vintage_query = """
        SELECT 
            DATE_FORMAT(disbursed_date, '%%Y-%%m') as vintage_month,
            COUNT(loan_id) as loans,
            ROUND(SUM(principal), 0) as disbursed,
            ROUND(AVG(CASE WHEN max_days_late >= 30 THEN 1 ELSE 0 END)*100, 2) as par30_pct
        FROM int_loans_repayments
        GROUP BY vintage_month
        ORDER BY vintage_month
        """
        with engine.connect() as conn:
            vintage_df = pd.read_sql(vintage_query, conn)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(vintage_df, x='vintage_month', y='par30_pct', markers=True,
                           title="PAR30 Trend by Vintage Month")
            fig1.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(vintage_df, x='vintage_month', y='disbursed',
                          title="Disbursed Amount by Vintage")
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(vintage_df, use_container_width=True)

# RISK SEGMENTATION
if st.session_state.show_risk:
    with st.expander("Risk Segmentation", expanded=True):
        seg_query = """
        SELECT 
            c.location, 
            c.income_band,
            COUNT(l.loan_id) as loan_count,
            ROUND(AVG(CASE WHEN r.max_days_late >= 30 THEN 1 ELSE 0 END)*100, 2) as par30_rate,
            ROUND(SUM(l.principal), 0) as total_disbursed
        FROM stg_loans l
        JOIN stg_customers c ON l.customer_id = c.customer_id
        JOIN int_loans_repayments r ON l.loan_id = r.loan_id
        GROUP BY c.location, c.income_band
        """
        with engine.connect() as conn:
            segments = pd.read_sql(seg_query, conn)

        st.dataframe(segments.sort_values('par30_rate', ascending=False), use_container_width=True)

        fig_seg = px.bar(segments, x='location', y='par30_rate', color='income_band',
                         title="PAR30 Rate by Location & Income Band")
        st.plotly_chart(fig_seg, use_container_width=True)

# DEVICE PERFORMANCE 
if st.session_state.show_device:
    with st.expander("Device Performance Analysis", expanded=True):
        device_query = """
        SELECT 
            device_model,
            COUNT(loan_id) as loan_count,
            ROUND(AVG(CASE WHEN max_days_late >= 30 THEN 1 ELSE 0 END)*100, 2) as par30_rate,
            ROUND(SUM(principal), 0) as disbursed
        FROM int_loans_repayments
        GROUP BY device_model
        ORDER BY par30_rate DESC
        """
        with engine.connect() as conn:
            device_perf = pd.read_sql(device_query, conn)

        st.dataframe(device_perf, use_container_width=True)

# FOOTER
st.divider()
st.caption("**Developed by Aklilu Abera** | **Data Analyst**")
st.caption("MoPhones Credit Portfolio Health Monitor • Built with MySQL • dbt • Streamlit")