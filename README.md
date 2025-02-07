# Texas Real Estate Market Analysis

An interactive Streamlit dashboard for analyzing real estate market data in Texas, featuring:

- Interactive choropleth maps of various market indicators
- Correlation analysis between different market factors
- Statistical summaries and data exploration tools

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

## Data Structure

The application expects the following data files:

- `data/tmp/merge.csv`: Merged real estate market data
- `tx_texas_zip_codes_geo.min.json`: GeoJSON file containing Texas ZIP code boundaries

## Features

- Interactive choropleth map visualization
- Dynamic variable selection for different market indicators
- Correlation analysis between market factors
- Statistical summaries and data previews

## Deployment

This application can be deployed on:

- Streamlit Cloud
- Custom servers supporting Python and Streamlit

For deployment instructions, see [Streamlit Deployment](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

## License

[Your chosen license]
