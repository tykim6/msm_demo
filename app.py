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
    df = pd.read_csv("data/tmp/merge.csv")
    # Convert zip codes to strings
    df["zip"] = df["zip"].astype(str)
    return df


@st.cache_data
def load_geojson():
    # Load Texas zip codes geometry data
    with open("tx_texas_zip_codes_geo.min.json") as f:
        texas_zips = json.load(f)
    return texas_zips


# Initialize session state for tracking initial load
if "initial_load" not in st.session_state:
    st.session_state.initial_load = True
    # Create progress indicators only during initial load
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    with progress_placeholder.container():
        progress_bar = st.progress(0)
    with status_placeholder.container():
        status_text = st.empty()

    # Load data with progress updates
    status_text.text("Loading CSV data...")
    df = load_data()
    progress_bar.progress(25)

    status_text.text("Loading GeoJSON data (this might take a moment)...")
    texas_zips = load_geojson()
    progress_bar.progress(50)

    # Store data in session state
    st.session_state.df = df
    st.session_state.texas_zips = texas_zips

    # Clean up progress indicators
    progress_placeholder.empty()
    status_placeholder.empty()
else:
    # Use stored data on subsequent renders
    df = st.session_state.df
    texas_zips = st.session_state.texas_zips

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

# Update color_variable when selectbox changes
color_variable = st.sidebar.selectbox(
    "Select Variable to Display",
    num_cols,
    index=num_cols.index(st.session_state.color_variable),
)
st.session_state.color_variable = color_variable

# Main content area
st.header("Geographic Distribution")


# Create choropleth map function (removed caching)
def create_choropleth(_df, _color_var, _geojson):
    return px.choropleth_map(
        _df,
        geojson=_geojson,
        locations="zip",
        featureidkey="properties.ZCTA5CE10",
        color=_color_var,
        color_continuous_scale="Mint",
        title=f"{_color_var} Distribution by ZIP Code",
        center={"lat": 32.7767, "lon": -96.7970},
        opacity=0.7,
        color_continuous_midpoint=_df[_color_var].mean(),
    )


# Create and style the map
fig = create_choropleth(df, color_variable, texas_zips)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    scope="usa",
    projection_scale=7,
    center={"lat": 31, "lon": -100},
)
fig.update_traces(marker_line_width=1, marker_line_color="black")
fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0}, height=600, geo=dict(scope="usa")
)

# Display the map
st.plotly_chart(fig, use_container_width=True)


# Cache the correlation analysis
@st.cache_data
def create_correlation_matrix(_df):
    correlation_cols = _df.select_dtypes(include=["float64", "int64"]).columns
    correlation_cols = correlation_cols[
        ~correlation_cols.isin(
            ["zip", "coli", "demographics_senior", "health_care_system"]
        )
    ]
    return _df[correlation_cols].corr()


# Correlation Analysis
st.header("Correlation Analysis")

# Create correlation matrix
corr_matrix = create_correlation_matrix(df)

# Create heatmap
fig_corr, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
plt.title("Correlation Matrix of Numerical Variables")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()

# Display correlation heatmap
st.pyplot(fig_corr)

# Add data statistics
st.header("Data Statistics")
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Summary Statistics for {color_variable}")
    st.write(df[color_variable].describe())

with col2:
    st.subheader("Sample Data")
    st.write(df.head())
