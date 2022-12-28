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


actual=run_query("select ACTUAL from ACTVSPREC;")
prediction=run_query("select PREDICTIONS from ACTVSPREC;")
date=run_query("select DDATE from ACTVSPREC;")


# Create DataFrame from multiple lists


df2=pd.DataFrame(list(zip(date,actual,prediction)))
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
   labels={
       "sales_date": "Date",
       "value": "Pairs",
       "variable": "Legend"
   }
)

# Plotly graph configs
legend_names = {"sales": "Actual Sales", "sales_forecast": "Forecasted Sales"}
line_fig.for_each_trace(lambda t: t.update(name=legend_names[t.name],
                                     legendgroup=legend_names[t.name]))
line_fig.update_layout(
   xaxis=dict(showgrid=False),
   legend=dict(
       yanchor="top",
       y=0.99,
       xanchor="right",
       x=0.99
   ),
   title_x=0.5,
   height=600
)

# passing in the Plotly graph object to Streamlit
st.plotly_chart(line_fig, use_container_width=True)

# Print results.




