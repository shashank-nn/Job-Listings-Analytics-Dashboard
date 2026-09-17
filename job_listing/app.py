
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Job Listings Analytics Dashboard",
    page_icon="💼",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/cleaned_job_listings.csv")
    
    return df


df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💼 Job Listings Analytics Dashboard")

st.markdown(
    """
    ### Python Web Scraping & Data Analytics Project

    This dashboard analyzes job listings collected through
    web scraping and processed using Python, Pandas,
    exploratory data analysis and feature engineering.
    """
)

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

# Job Category
categories = sorted(
    df["job_category"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Job Category",
    categories,
    default=categories
)

# Job Level
levels = sorted(
    df["job_level"].dropna().unique().tolist()
)

selected_levels = st.sidebar.multiselect(
    "Select Job Level",
    levels,
    default=levels
)

# Location
locations = sorted(
    df["location"].dropna().unique().tolist()
)

selected_locations = st.sidebar.multiselect(
    "Select Location",
    locations,
    default=locations
)

# Python filter
python_filter = st.sidebar.selectbox(
    "Python Related Jobs",
    [
        "All",
        "Python Related",
        "Non-Python Related"
    ]
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df[
    df["job_category"].isin(selected_categories)
    &
    df["job_level"].isin(selected_levels)
    &
    df["location"].isin(selected_locations)
]

if python_filter == "Python Related":
    filtered_df = filtered_df[
        filtered_df["python_related"] == 1
    ]

elif python_filter == "Non-Python Related":
    filtered_df = filtered_df[
        filtered_df["python_related"] == 0
    ]

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

search_term = st.sidebar.text_input(
    "Search Job Title"
)

if search_term:
    filtered_df = filtered_df[
        filtered_df["job_title"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Jobs",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Companies",
        filtered_df["company"].nunique()
    )

with col3:
    st.metric(
        "Locations",
        filtered_df["location"].nunique()
    )

with col4:
    st.metric(
        "Python Jobs",
        int(filtered_df["python_related"].sum())
    )

st.divider()

# --------------------------------------------------
# CHART 1 — JOB CATEGORY
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    category_data = (
        filtered_df["job_category"]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Job Category",
        "Number of Jobs"
    ]

    fig_category = px.bar(
        category_data,
        x="Job Category",
        y="Number of Jobs",
        title="Jobs by Category",
        text="Number of Jobs"
    )

    fig_category.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# --------------------------------------------------
# CHART 2 — JOB LEVEL
# --------------------------------------------------

with col2:

    level_data = (
        filtered_df["job_level"]
        .value_counts()
        .reset_index()
    )

    level_data.columns = [
        "Job Level",
        "Number of Jobs"
    ]

    fig_level = px.pie(
        level_data,
        names="Job Level",
        values="Number of Jobs",
        title="Job Level Distribution"
    )

    st.plotly_chart(
        fig_level,
        use_container_width=True
    )

# --------------------------------------------------
# CHART 3 — TOP COMPANIES
# --------------------------------------------------

company_data = (
    filtered_df["company"]
    .value_counts()
    .head(10)
    .reset_index()
)

company_data.columns = [
    "Company",
    "Number of Jobs"
]

fig_company = px.bar(
    company_data.sort_values("Number of Jobs"),
    x="Number of Jobs",
    y="Company",
    orientation="h",
    title="Top 10 Companies by Job Listings",
    text="Number of Jobs"
)

st.plotly_chart(
    fig_company,
    use_container_width=True
)

# --------------------------------------------------
# CHART 4 — LOCATIONS
# --------------------------------------------------

location_data = (
    filtered_df["location"]
    .value_counts()
    .head(15)
    .reset_index()
)

location_data.columns = [
    "Location",
    "Number of Jobs"
]

fig_location = px.bar(
    location_data.sort_values("Number of Jobs"),
    x="Number of Jobs",
    y="Location",
    orientation="h",
    title="Top Job Locations"
)

st.plotly_chart(
    fig_location,
    use_container_width=True
)

# --------------------------------------------------
# CHART 5 — PYTHON JOBS
# --------------------------------------------------

python_data = (
    filtered_df["python_related"]
    .map({
        0: "Non-Python",
        1: "Python Related"
    })
    .value_counts()
    .reset_index()
)

python_data.columns = [
    "Type",
    "Number of Jobs"
]

fig_python = px.pie(
    python_data,
    names="Type",
    values="Number of Jobs",
    title="Python-Related Job Distribution"
)

st.plotly_chart(
    fig_python,
    use_container_width=True
)

# --------------------------------------------------
# TOP JOB TITLES
# --------------------------------------------------

title_data = (
    filtered_df["job_title"]
    .value_counts()
    .head(15)
    .reset_index()
)

title_data.columns = [
    "Job Title",
    "Number of Jobs"
]

fig_titles = px.bar(
    title_data.sort_values("Number of Jobs"),
    x="Number of Jobs",
    y="Job Title",
    orientation="h",
    title="Most Common Job Titles"
)

st.plotly_chart(
    fig_titles,
    use_container_width=True
)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.subheader("📋 Job Listings")

display_columns = [
    "job_title",
    "company",
    "location",
    "job_category",
    "job_level",
    "python_related"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_job_listings.csv",
    mime="text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Job Listings Analytics Dashboard | "
    "Python • Web Scraping • Pandas • EDA • Streamlit"
)
