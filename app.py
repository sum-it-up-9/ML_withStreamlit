import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np


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

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

#rows = run_query("select * from ML;")


actual=run_query("select ACTUAL from ACTVSPREC;")
prediction=run_query("select PREDICTIONS from ACTVSPREC;")
date=run_query("select DDATE from ACTVSPREC;")

df2=pd.DataFrame(actual,prediction,date)



st.write(df2)
#chart_data = pd.DataFrame(
 #   np.random.randn(20, 3),
 #   columns=['a', 'b', 'c'])

#st.line_chart(rows)
# Print results.




