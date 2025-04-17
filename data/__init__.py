# For demo purposes, you can replace this with your actual dataframe logic
from data.create_dataframe import create_dataframe
import plotly.express as px

df = px.data.gapminder()
df_store_data = df.to_dict('records')
