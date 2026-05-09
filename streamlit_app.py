import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

st.set_page_config(
    page_title="MoPhones Credit Portfolio",
    layout="wide",
    page_icon=""
)

st.title("MoPhones Credit Portfolio Health Monitor")
st.markdown("### Real-time Credit Risk & Portfolio Dashboard")

# ==================== DATABASE CONNECTION (Cloud + Local) ====================
@st.cache_resource
def get_connection():
    try:
        # === Streamlit Cloud (using secrets) ===
        if "connections" in st.secrets:
            db = st.secrets["connections"]["mysql"]
            connection_string = (
                f"mysql+pymysql://{db['username']}:{db['password']}@"
                f"{db['host']}:{db['port']}/{db['database']}"
            )
            st.success("Connected using Streamlit Secrets (Cloud)")
        
        # === Local Development (using .env) ===
        else:
            user = os.getenv('MYSQL_USER')
            password = os.getenv('MYSQL_PASSWORD')
            host = os.getenv('MYSQL_HOST')
            port = os.getenv('MYSQL_PORT')
            database = os.getenv('MYSQL_DATABASE')

            if not all([user, password, host, port, database]):
                st.error("Missing database credentials in .env file")
                st.stop()

            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
            st.success(" Connected using .env (Local)")

        engine = create_engine(connection_string, pool_pre_ping=True)
        return engine

    except Exception as e:
        st.error(f"Connection Failed: {e}")
        st.info("Please check your `.streamlit/secrets.toml` configuration.")
        st.stop()

engine = get_connection()


# ==================== LOAD DATA ====================
with engine.connect() as conn:
    df_kpis = pd.read_sql("SELECT * FROM mart_portfolio_kpis", conn)

# ==================== SIDEBAR ====================
st.sidebar.success("Database Connected")

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

st.info("Toggle buttons for Vintage, Risk & Device Analysis coming in next update.")

# ==================== FOOTER ====================
st.divider()
st.caption("**Developed by Aklilu Abera** | Data Analyst")
st.caption("MoPhones Credit Portfolio Health Monitor • Built with MySQL • dbt • Streamlit")
