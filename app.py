import streamlit as st
import plotly.express as px
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


actual=run_query("select ACTUAL from ACTVSPREC limit 5;")
prediction=run_query("select PREDICTIONS from ACTVSPREC limit 5;")
date=run_query("select DDATE from ACTVSPREC limit 5 ;")


# Create DataFrame from multiple lists


df2=pd.DataFrame(list(zip(date,actual,prediction)),columns=['date','actual','prediction'])
st.write(df2)

#chart_data = pd.DataFrame(
 #   np.random.randn(20, 3),
 #   columns=['a', 'b', 'c'])

#st.line_chart(rows)
line_fig = px.line(
   df2,
   x="date",
   y=["actual", "prediction"],
   title="Actual Values vs Forecasted values",
 
)


df = pd.DataFrame({
  'date': ['10/1/2019','10/2/2019', '10/3/2019', '10/4/2019','10/5/2019','10/6/2019','10/7/2019','10/8/2019','10/9/2019'],
  'Actual': [46.53, 48.33, 47.05, 44.05,45,46,43,47,46],
    'Prediction':[47,47,45,46,44.05,45,46,43,47,46]
})






# Print results.


st.line_chart(df2, x="date",
   y=["actual", "prediction"],)

