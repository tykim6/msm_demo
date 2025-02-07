import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json
import numpy as np

# Set page config
st.set_page_config(layout="wide", page_title="Real Estate Market Analysis")


# Cache the data loading
@st.cache_data
def load_data():
    # Load the merged dataframe
    df = pd.read_csv("data/merge.csv")
    # Convert zip codes to strings
    df["zip"] = df["zip"].astype(str)
    return df


@st.cache_data
def load_geojson():
    # Load Texas zip codes geometry data
    with open("tx_texas_zip_codes_geo.min.json") as f:
        texas_zips = json.load(f)
    return texas_zips


# Initialize session state variables at the very beginning
if "df" not in st.session_state:
    st.session_state.df = None
if "texas_zips" not in st.session_state:
    st.session_state.texas_zips = None
if "initial_load" not in st.session_state:
    st.session_state.initial_load = True

# Load data if it hasn't been loaded yet
if st.session_state.initial_load:
    try:
        # Create progress indicators
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        with progress_placeholder.container():
            progress_bar = st.progress(0)
        with status_placeholder.container():
            status_text = st.empty()

        # Load data with progress updates
        status_text.text("Loading CSV data...")
        st.session_state.df = load_data()
        progress_bar.progress(50)

        status_text.text("Loading GeoJSON data...")
        st.session_state.texas_zips = load_geojson()
        progress_bar.progress(100)

        # Mark initial load as complete
        st.session_state.initial_load = False

        # Clean up progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Get the data from session state
df = st.session_state.df
texas_zips = st.session_state.texas_zips

# Ensure data is loaded before proceeding
if df is None or texas_zips is None:
    st.error("Data not properly loaded. Please refresh the page.")
    st.stop()

# Title
st.title("Texas Real Estate Market Analysis")

# Sidebar for controls
st.sidebar.header("Map Controls")

# Get numerical columns for color selection
num_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# Initialize color_variable in session state if not present
if "color_variable" not in st.session_state:
    st.session_state.color_variable = (
        "AVG_PRICE" if "AVG_PRICE" in num_cols else num_cols[0]
    )

# Update color_