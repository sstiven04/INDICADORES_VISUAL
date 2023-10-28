import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

st.set_page_config(layout='wide')
st.title("Indicador del bienestar")
bienestar = pd.read_csv('---')