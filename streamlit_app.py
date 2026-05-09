import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

st.set_page_config(
    page_title="MoPhones Credit Portfolio",
    layout="wide",
    page_icon="🛡️"
)

st.title("🛡️ MoPhones Credit Portfolio Health Monitor")
st.markdown("### Real-time Credit Risk & Portfolio Dashboard")

# ==================== DATABASE CONNECTION (Cloud First) ====================
@st.cache_resource
def get_connection():
    try:
        # Streamlit Cloud - Use secrets.toml
        if "connections" in st.secrets:
            db = st.secrets["connections"]["mysql"]
            conn_str = (
                f"mysql+pymysql://{db['username']}:{db['password']}@"
                f"{db['host']}:{db['port']}/{db['database']}"
            )
            st.success("✅ Connected using Streamlit Secrets (Cloud)")
        
        # Local Development - Fallback to .env
        else:
            conn_str = (
                f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
                f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
            )
            st.success("✅ Connected using .env (Local)")

        engine = create_engine(conn_str, pool_pre_ping=True)
        return engine

    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")
        st.info("💡 Make sure you have added the secrets correctly in Streamlit Cloud Settings.")
        st.stop()


engine = get_connection()

# ==================== LOAD DATA ====================
with engine.connect() as conn:
    df_kpis = pd.read_sql("SELECT * FROM mart_portfolio_kpis LIMIT 1", conn)

# ==================== KPI CARDS ====================
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

st.info("🔄 More sections (Vintage Analysis, Risk Segmentation, Device Performance) will be added soon.")

# ==================== FOOTER ====================
st.divider()
st.caption("**Developed by Aklilu Abera** | Data Analyst")
st.caption("MoPhones Credit Portfolio Health Monitor • Built with MySQL • dbt • Streamlit")
