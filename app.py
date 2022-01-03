import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import csv
import plotly.graph_objects as go

gss_data = pd.read_csv('gss2016.csv', delimiter=",")

st.title("The General Social Survey Data Analytics Web App")
# st.write(f'<iframe></iframe>',unsafe_allow_html=True)
st.write("")
st.header("GSS 2016 Dataset")

# st.dataframe(gss_data)

gss_data_filtered = gss_data[['sex','race','age','degree','wrkstat','income','happy']]
st.dataframe(gss_data_filtered.head())

columns = {
    "sex","race","age","degree","wrkstat","income","happy"
}

pick_columns = st.selectbox("Count By column: ", list(columns))

gss_data_filtered['Count'] = 0
gss_data_filtered_count = gss_data_filtered.groupby(pick_columns).count()
gss_data_filtered_count = gss_data_filtered_count[["Count"]]
gss_data_filtered_count.columns = ['Count']
gss_data_filtered_count["Percentages"] = (gss_data_filtered_count.Count/gss_data_filtered_count.Count.sum()) * 100

st.dataframe(gss_data_filtered_count)

multi_select_column = st.multiselect("Columns for Correlation", list(columns), default=["sex"])

multi_select_gss_data_filtered = gss_data_filtered[multi_select_column]

st.dataframe(multi_select_gss_data_filtered.head())

multi_select_column2 = st.multiselect("Multi-select columns grouped by: ",list(columns),default=["sex"])

multi_select_groupby = gss_data_filtered[multi_select_column2].groupby(multi_select_column2).size().reset_index(name="Count")

multi_select_groupby["Percentages"] = (multi_select_groupby.Count/multi_select_groupby.Count.sum()) * 100

st.dataframe(multi_select_groupby)

pick_columns_visualized = st.selectbox("Visualize by Column", list(columns))
gss_data_filtered_count_visual = gss_data_filtered.groupby(pick_columns_visualized).count()

gss_data_filtered_count_visual['x-axis'] = gss_data_filtered_count_visual.index
fig = go.Figure(
    data = [
        go.Pie(
            labels=gss_data_filtered_count_visual["x-axis"],
            values=gss_data_filtered_count_visual["Count"]
               )
    ]
)

st.plotly_chart(fig)