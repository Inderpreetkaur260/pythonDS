# ✅ Full Corrected Streamlit App (Syntax Fixed, Heatmaps Removed, Accurate EDA, Detailed Text)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page config MUST be at the top before any Streamlit output
st.set_page_config(page_title="Global Cost of Living Explorer in India", layout="wide")

# -------------------- Helpers --------------------
def clean_numeric(series: pd.Series) -> pd.Series:
    """Convert strings with symbols to numeric, coerce errors to 0."""
    return pd.to_numeric(series.replace('[^0-9.]', '', regex=True), errors='coerce').fillna(0)


def recommend_city(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    salary = clean_numeric(df['Average Monthly Net Salary (After Tax)'])
    rent = clean_numeric(df['Apartment (1 bedroom) in City Centre)']) if 'Apartment (1 bedroom) in City Centre)' in df.columns else clean_numeric(df['Apartment (1 bedroom) in City Centre'])
    transport = clean_numeric(df['Monthly Pass (Regular Price)'])
    milk = clean_numeric(df['Milk (regular), (1 liter)'])
    rice = clean_numeric(df['Rice (white), (1kg)'])

    denom = rent + transport + milk + rice
    with np.errstate(divide='ignore', invalid='ignore'):
        score = salary / denom
    score = pd.Series(score).replace([np.inf, -np.inf], 0).fillna(0)
    df['Affordability Score'] = score
    return df.sort_values(by='Affordability Score', ascending=False).head(5)

# -------------------- Load Data --------------------
try:
    data = pd.read_csv("cost_of_living_indian_cities.csv")
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'cost_of_living_indian_cities.csv' is present in the working directory.")
    st.stop()

# -------------------- Clean numeric columns once --------------------
# Guard missing columns with get and defaults
required_cols = {
    'Average Monthly Net Salary (After Tax)': 'Salary',
    'Apartment (1 bedroom) in City Centre': 'Rent',
    'Milk (regular), (1 liter)': 'Milk',
    'Loaf of Fresh White Bread (500g)': 'Bread',
    'Rice (white), (1kg)': 'Rice',
    'Monthly Pass (Regular Price)': 'Transport',
}

for raw_col, clean_col in required_cols.items():
    if raw_col not in data.columns:
        st.error(f"Missing required column in CSV: {raw_col}")
        st.stop()
    data[clean_col] = clean_numeric(data[raw_col])

# Derived columns
data['Groceries'] = data['Milk'] + data['Bread'] + data['Rice']
data['Total Cost'] = data['Rent'] + data['Groceries'] + data['Transport']
with np.errstate(divide='ignore', invalid='ignore'):
    data['Affordability Index'] = (data['Total Cost'] / data['Salary']).replace([np.inf, -np.inf], 0).fillna(0)

# -------------------- Sidebar Navigation --------------------
pages = ["🏠 Home", "ℹ️ About", "🔍 Filter & Insights", "📊 EDA", "🌟 Recommendations"]
selected_page = st.sidebar.radio("Navigate", pages)

# -------------------- Home --------------------
if selected_page == "🏠 Home":
    st.title("🌍 Global Cost of Living Explorer in India")
    st.markdown(
        """
        ## 👋 Welcome Explorer!

        Welcome to the **Global Cost of Living Explorer — India Edition**, your all-in-one dashboard designed to help you
        understand, compare, and analyze the cost-of-living landscape across major Indian cities.

        This dashboard brings together **housing**, **transportation**, **groceries**, **salaries**, and **overall affordability indicators** in one elegant interface.

        ### ✅ What You Can Do Here
        - **Explore individual cities** and understand their economic profile
        - **Compare multiple cities** side-by-side to make smarter decisions
        - **Use the Budget Planner** to check if a city fits your income
        - **Calculate grocery costs** instantly for personalized estimates
        - **Understand affordability** using smart indexes and data-driven formulas
        - **Upload your own dataset** to explore more

        Whether you're a **student**, **job seeker**, **planner**, **researcher**, or someone preparing to **relocate**,
        this tool offers accurate and insightful economic information.

        ### 🚀 How to Begin
        Use the **sidebar** on the left to jump into different sections.

        Let’s make data-driven decisions easier and smarter! 🌟
        """
    )

# -------------------- About --------------------
elif selected_page == "ℹ️ About":
    st.title("ℹ️ About This Dashboard")
    st.markdown(
        """
        ## 📘 About the India Cost of Living Explorer

        The **India Livability Explorer** is a comprehensive analytical platform developed to simplify economic comparison across cities.

        ### 🎯 Purpose of This Dashboard
        India is incredibly diverse — economically, culturally, and geographically. This dashboard aims to provide:
        - **Transparency** in city-level living costs
        - **Realistic comparisons** across multiple expense categories
        - **Tools** to evaluate affordability
        - **Visual insights** that make complex data easy to understand

        ### 🧠 What This Dashboard Calculates
        - **Accurate salary metrics** using cleaned numeric data
        - **Rent levels** for central urban housing
        - **Groceries bundle cost** including milk, bread, and rice
        - **Transportation cost** using monthly pass data
        - **Total monthly cost** per city
        - **Affordability Index** → total cost ÷ salary
        - **Affordability Score** → smart formula for ranking cities

        ### 🛠 Tech Behind the Dashboard
        - **Python** for data logic
        - **Pandas** for data cleanup
        - **Plotly** for interactive graphs
        - **Streamlit** for UI components

        ### ❤️ Built For
        Students • Working professionals • Relocators • Travelers • Analysts • Recruiters • Researchers

        This tool aims to make economic planning **clear**, **visual**, and **actionable**.
        """
    )

# -------------------- Filter & Insights --------------------
elif selected_page == "🔍 Filter & Insights":
    st.title("🔍 Filter & Insights")
    st.markdown(
        """
        ## 🔎 Explore Cities Through Filters
        This section helps you **deep-dive into specific cities**, compare them, plan budgets, and calculate personal expenses.

        You can filter by:
        - **Region**: North, South, East, West, Central
        - **City**: choose from available cities
        - **Budget preferences**
        - **Grocery quantities** (for calculations)

        Each tab offers a different kind of insight.
        """
    )

    region_map = {
        "North": ["Delhi", "Chandigarh", "Jaipur", "Lucknow"],
        "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi"],
        "East": ["Kolkata", "Bhubaneswar", "Guwahati"],
        "West": ["Mumbai", "Pune", "Ahmedabad"],
        "Central": ["Bhopal", "Nagpur"],
    }

    region_selected = st.sidebar.selectbox("🌍 Select Region", ["All"] + list(region_map.keys()))
    if region_selected != "All":
        cities = [c for c in region_map[region_selected] if c in set(data['City'])]
        # Fallback to all cities if none from the region are present in data
        if not cities:
            cities = sorted(data['City'].unique())
    else:
        cities = sorted(data['City'].unique())

    selected_city = st.sidebar.selectbox("🏙️ Select a City", cities)

    st.success(f"You're exploring {selected_city} ({region_selected} region)")

    filtered_df = data[data["City"] == selected_city].copy()

    tabs = st.tabs([
        "🏙️ Overview",
        "📊 Compare Cities",
        "🧲 Budget Planner",
        "🗺️ Map View",
        "🧮 Grocery Calculator",
        "🗃️ Raw Data",
        "📤 Upload",
    ])

    with tabs[0]:
        st.subheader(f"Cost Overview — {selected_city}")
        if filtered_df.empty:
            st.info("Selected city is not present in the dataset.")
        else:
            st.dataframe(
                filtered_df[
                    ['City', 'Salary', 'Rent', 'Groceries', 'Transport', 'Total Cost', 'Affordability Index']
                ]
            )

    with tabs[1]:
        st.subheader("Compare Cities")
        compare_cities = st.multiselect(
            "Select cities to compare", options=sorted(data["City"].unique()), default=[selected_city]
        )
        compare_df = data[data["City"].isin(compare_cities)].copy()
        if compare_df.empty:
            st.info("Please select at least one city that exists in the dataset.")
        else:
            fig = px.bar(compare_df, x='City', y='Total Cost', title="Total Monthly Cost by City")
            st.plotly_chart(fig, use_container_width=True)

            fig_scatter = px.scatter(
                compare_df,
                x='Salary', y='Total Cost', color='City',
                size=(1 / (compare_df['Affordability Index'].replace(0, np.nan))).fillna(0),
                title="Affordability: Salary vs Total Cost",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    with tabs[2]:
        st.subheader("Budget Planner")
        budget = st.slider("Monthly Budget (₹)", 5000, 200000, 30000, step=1000)
        if filtered_df.empty:
            st.info("Select a valid city to evaluate budget fit.")
        else:
            total_cost = float(filtered_df['Total Cost'].iloc[0])
            if total_cost <= budget:
                st.success(f"✅ {selected_city} fits your budget! (Estimated total: ₹{total_cost:,.0f})")
            else:
                st.warning(f"❌ {selected_city} exceeds your budget. (Estimated total: ₹{total_cost:,.0f})")

    with tabs[3]:
        st.subheader("Map View (Static)")
        st.caption("This is a placeholder map centered over India. Add per-city coordinates for precision.")
        st.map(pd.DataFrame({'lat': [22.59], 'lon': [78.96]}))

    with tabs[4]:
        st.subheader("Grocery Calculator")
        if filtered_df.empty:
            st.info("Select a valid city to calculate groceries.")
        else:
            milk_qty = st.number_input("Milk (liters)", 0.0, 50.0, 1.0)
            bread_qty = st.number_input("Bread (loaves)", 0.0, 50.0, 1.0)
            rice_qty = st.number_input("Rice (kg)", 0.0, 50.0, 1.0)
            total = (
                milk_qty * float(filtered_df['Milk'].iloc[0]) +
                bread_qty * float(filtered_df['Bread'].iloc[0]) +
                rice_qty * float(filtered_df['Rice'].iloc[0])
            )
            st.write(f"Estimated Grocery Cost: ₹{total:,.2f}")

    with tabs[5]:
        st.subheader("Raw Data (Selected City)")
        if filtered_df.empty:
            st.info("No rows to display for the selected city.")
        else:
            st.dataframe(filtered_df)

    with tabs[6]:
        st.subheader("Upload Your Data")
        file = st.file_uploader("Upload CSV")
        if file is not None:
            try:
                df_up = pd.read_csv(file)
                st.success("File loaded successfully. Preview below:")
                st.dataframe(df_up.head())
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")

# -------------------- EDA --------------------
elif selected_page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.subheader("✅ Accurate Summary Statistics (Cleaned Values)")
    stats_df = data[['Salary', 'Rent', 'Groceries', 'Transport', 'Total Cost', 'Affordability Index']].describe()
    st.dataframe(stats_df)

    st.subheader("Salary Distribution Across Cities")
    fig_salary = px.box(data, y='Salary', points='all', title="Salary Distribution Across Cities")
    st.plotly_chart(fig_salary, use_container_width=True)

    st.subheader("Top 10 Expensive Cities by Rent (City Centre)")
    top_rent = data.sort_values('Rent', ascending=False).head(10)
    fig_rent = px.bar(top_rent, x='City', y='Rent', title="Top 10 Cities by Rent (City Centre)")
    st.plotly_chart(fig_rent, use_container_width=True)

    st.subheader("Affordability Index by City (Lower is Better)")
    fig_aff = px.bar(data.sort_values('Affordability Index'), x='City', y='Affordability Index', title="Affordability Index by City")
    st.plotly_chart(fig_aff, use_container_width=True)

# -------------------- Smart Recommendations --------------------
elif selected_page == "🌟 Recommendations":
    st.title("🌟 Smart City Recommendations")
    st.markdown("Here are the top cities based on your salary-to-cost ratio 🔍💡")
    try:
        top_cities = recommend_city(data)
        st.dataframe(top_cities[['City', 'Affordability Score']])
    except Exception as e:
        st.error(f"Could not compute recommendations: {e}")


