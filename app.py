import streamlit as st
import snowflake.connector
# set_page_config needs to be the first Streamlit command in your script
st.set_page_config(layout="wide")
st.title("CPG Forecasting Models Monitoring")

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

def load_data():
   #rows = run_query("SELECT * from mytable;")
   cur = conn.cursor().execute("select CURRENT_ACCOUNT();")
  # cur = conn.cursor().execute(query)
   return cur.fetch_pandas_all()



df = load_data()
st.write(df)

