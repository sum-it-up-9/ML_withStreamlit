import streamlit as st
import plotly.express as px
import snowflake.connector

import pandas as pd
import numpy as np


# set_page_config needs to be the first Streamlit command in your script
st.set_page_config(layout="wide")
st.title("FOREX Forecasting Models Monitoring")

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
  'date': ['12/28/2022','12/29/2022','12/30/2022','12/31/2022','01/1/2023','01/2/2023', '01/3/2023', '01/4/2023','01/5/2023','01/6/2023'],
  'Actual': [ 46.53, 46.53,  46.54, 46.64,46.645,46.62,46.665,46.63,46.7,46.68],
    'Prediction':[ 46.52, 46.530, 46.52, 46.54,46.66,46.643,46.624,46.666,46.619,46.721]
})






# Print results.


st.line_chart(df, x="date",
   y=["Actual", "Prediction"],)

