import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import io
import numpy as np


# -------------------- Helpers --------------------
st.set_page_config(page_title="Global Cost of Living Explorer in India", layout="wide")
def clean_numeric(series):
    return pd.to_numeric(series.replace('[^0-9.]', '', regex=True), errors='coerce').fillna(0)

def recommend_city(df):
    df = df.copy()
    df['Affordability Score'] = clean_numeric(df['Average Monthly Net Salary (After Tax)']) / (
        clean_numeric(df['Apartment (1 bedroom) in City Centre']) +
        clean_numeric(df['Monthly Pass (Regular Price)']) +
        clean_numeric(df['Milk (regular), (1 liter)']) +
        clean_numeric(df['Rice (white), (1kg)'])
    )
    df['Affordability Score'] = df['Affordability Score'].replace([np.inf, -np.inf], 0).fillna(0)
    return df.sort_values(by='Affordability Score', ascending=False).head(5)

# -------------------- Load Data --------------------
try:
    data = pd.read_csv("cost_of_living_indian_cities.csv")
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'cost_of_living_indian_cities.csv' is present in the working directory.")
    st.stop()


# -------------------- Sidebar Navigation --------------------
pages = ["🏠 Home", "ℹ️ About", "🔍 Filter & Insights", "📊 EDA", "🌟 Recommendations"]
selected_page = st.sidebar.radio("Navigate", pages)

# -------------------- Home --------------------
if selected_page == "🏠 Home":
    st.title("🌍 Global Cost of Living Explorer in India")
    st.markdown("""
    ## 👋 Welcome Explorer!

    Navigate the vibrant economics of Indian cities in one powerful dashboard 🚀

    **This tool allows you to:**
    - 🔎 Compare city-wise rent, groceries, transport, and salaries
    - 💰 Plan your relocation smartly with budget calculators
    - 🌐 Upload your own data to explore more

    **Made for dreamers, doers, and data lovers 💡**

    Use the sidebar to dive into data-driven decisions 🎯
    """)

# -------------------- About --------------------
elif selected_page == "ℹ️ About":
    st.title("ℹ️ About This Dashboard")
    st.markdown("""
    ## ✨ What's this all about?

    The **India Livability Explorer** is a data-rich dashboard that:
    - 📈 Visualizes cost-of-living metrics in Indian cities
    - 🧭 Helps users evaluate where to live based on affordability
    - 📊 Provides interactive analytics, insights, and planning tools

    ---
    **Tech Stack 💻**
    - Python + Pandas for data crunching
    - Streamlit for sleek UI
    - Plotly + Folium for interactive charts and maps

    Developed with ❤️ to make economic decisions visual and vibrant.
    """)

# -------------------- EDA --------------------
elif selected_page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.subheader("1. Summary Statistics")
    st.dataframe(data.describe(include='all'))

    st.subheader("2. Missing Values Heatmap")
    # fig, ax = plt.subplots(figsize=(10, 5))
    # sns.heatmap(data.isnull(), cbar=False, cmap="Reds", ax=ax)
    # st.pyplot(fig)
    
    missing = data.isnull().mean().sort_values(ascending=False)
    if missing.sum() > 0:  # Only show if missing values exist
        fig_missing = px.bar(
            missing,
            x=missing.index,
            y=missing.values,
            labels={'x': 'Column', 'y': 'Missing %'},
            title="Missing Values Percentage by Column"
        )
        st.plotly_chart(fig_missing)


    st.subheader("3. Correlation Heatmap")
    numeric_data = data.select_dtypes(include=[np.number])
    if not numeric_data.empty:      
        corr = numeric_data.corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)
    else:
        st.info("No numeric columns found for correlation analysis.")

    st.subheader("4. City-wise Distribution of Average Salary")
    data['Avg Salary Cleaned'] = clean_numeric(data['Average Monthly Net Salary (After Tax)'])
    fig_salary = px.box(data, y='Avg Salary Cleaned', points="all", title="Salary Distribution Across Cities")
    st.plotly_chart(fig_salary)

    st.subheader("5. Top 10 Expensive Cities by Rent")
    data['Rent'] = clean_numeric(data['Apartment (1 bedroom) in City Centre'])
    top_rent = data.sort_values(by='Rent', ascending=False).head(10)
    fig_rent = px.bar(top_rent, x='City', y='Rent', title="Top 10 Cities by Rent (City Centre)", color='Rent')
    st.plotly_chart(fig_rent)

    st.subheader("6. Affordability Index by City")
    data['Groceries'] = (
        clean_numeric(data['Milk (regular), (1 liter)']) +
        clean_numeric(data['Loaf of Fresh White Bread (500g)']) +
        clean_numeric(data['Rice (white), (1kg)'])
    )
    data['Transport'] = clean_numeric(data['Monthly Pass (Regular Price)'])
    data['Total Cost'] = data['Rent'] + data['Groceries'] + data['Transport']
    data['Affordability Index'] = data['Total Cost'] / data['Avg Salary Cleaned']

    fig_afford = px.bar(data.sort_values('Affordability Index'), x='City', y='Affordability Index',
                        title="Affordability Index by City", color='Affordability Index')
    st.plotly_chart(fig_afford)

# -------------------- Filter & Insights --------------------
elif selected_page == "🔍 Filter & Insights":
    st.title("🔍 Filter & Insights")
    st.markdown("""
    Use filters on the sidebar to slice the data and dive deeper 🔬
    """)

    st.sidebar.header("🎛️ Filters")
    region_map = {
        "North": ["Delhi", "Chandigarh", "Jaipur", "Lucknow"],
        "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi"],
        "East": ["Kolkata", "Bhubaneswar", "Guwahati"],
        "West": ["Mumbai", "Pune", "Ahmedabad"],
        "Central": ["Bhopal", "Nagpur"]
    }

    region_selected = st.sidebar.selectbox("🌍 Select Region", ["All"] + list(region_map.keys()))
    if region_selected != "All":
        cities = region_map[region_selected]
    else:
        cities = data["City"].unique()

    selected_city = st.sidebar.selectbox("🏙️ Select a City", cities)
    min_salary = st.sidebar.slider("💵 Minimum Avg Salary (₹)", 10000, 100000, 20000)
    max_aff_index = st.sidebar.slider("📊 Max Affordability Index", 0.1, 5.0, 1.0)
    normalize = st.sidebar.checkbox("📉 Show Normalized (% of Salary) Costs")
    
    st.success(f"You're exploring data for {selected_city} in the {region_selected} region.")

    filtered_df = data[data["City"].isin([selected_city])].copy()
    filtered_df['Salary'] = clean_numeric(filtered_df['Average Monthly Net Salary (After Tax)'])
    filtered_df['Rent'] = clean_numeric(filtered_df['Apartment (1 bedroom) in City Centre'])
    filtered_df['Groceries'] = (
        clean_numeric(filtered_df['Milk (regular), (1 liter)']) +
        clean_numeric(filtered_df['Loaf of Fresh White Bread (500g)']) +
        clean_numeric(filtered_df['Rice (white), (1kg)'])
    )
    filtered_df['Transport'] = clean_numeric(filtered_df['Monthly Pass (Regular Price)'])
    filtered_df['Total Cost'] = filtered_df['Rent'] + filtered_df['Groceries'] + filtered_df['Transport']
    filtered_df['Affordability Index'] = filtered_df['Salary'] / filtered_df['Total Cost']

    tabs = st.tabs([
        "🏙️ City Overview",
        "📊 Compare Cities",
        "🧲 Budget Planner",
        "🗺️ Map View",
        "🧮 Cost Calculator",
        "🗃️ Raw Data Explorer",
        "📤 Upload Your Data"
    ])

    with tabs[0]:
        st.markdown(
            f"""
            <div style="
                background-color:#f9fafb;
                border-radius:16px;
                padding:20px;
                box-shadow:0 4px 12px rgba(0,0,0,0.1);
                margin-bottom:15px;
                width: 60%;
            ">
                <h3 style="margin:0; color:#2d3748;">💸 Cost Breakdown for {selected_city}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            row = filtered_df.iloc[0]  # just the first row (assuming one city is selected)
        st.markdown(
            f"""
            <div style="
                background-color:white;
                border-radius:12px;
                padding:16px 20px;
                margin:8px 0;
                box-shadow:0 2px 8px rgba(0,0,0,0.12);
                width: 60%;
            ">
                <h4 style="margin-top:0; margin-bottom:10px; color:#2b6cb0;">{row['City']}</h4>
                <table style="width:100%; font-size:14px; color:#4a5568;">
                    <tr><td><b>Salary</b></td><td>{row['Salary']}</td></tr>
                    <tr><td><b>Rent</b></td><td>{row['Rent']}</td></tr>
                    <tr><td><b>Groceries</b></td><td>{row['Groceries']}</td></tr>
                    <tr><td><b>Transport</b></td><td>{row['Transport']}</td></tr>
                    <tr><td><b>Total Cost</b></td><td>{row['Total Cost']}</td></tr>
                    <tr><td><b>Affordability Index</b></td><td>{row['Affordability Index']}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tabs[1]:
        st.subheader("📊 Compare Cities")
        compare_cities = st.multiselect("Select cities to compare", options=data["City"].unique(), default=[selected_city])
        compare_df = data[data["City"].isin(compare_cities)].copy()

        compare_df['Salary'] = clean_numeric(compare_df['Average Monthly Net Salary (After Tax)'])
        compare_df['Rent'] = clean_numeric(compare_df['Apartment (1 bedroom) in City Centre'])
        compare_df['Groceries'] = (
            clean_numeric(compare_df['Milk (regular), (1 liter)']) +
            clean_numeric(compare_df['Loaf of Fresh White Bread (500g)']) +
            clean_numeric(compare_df['Rice (white), (1kg)'])
        )
        compare_df['Transport'] = clean_numeric(compare_df['Monthly Pass (Regular Price)'])
        compare_df['Total Cost'] = compare_df['Rent'] + compare_df['Groceries'] + compare_df['Transport']
        compare_df['Affordability Index'] =  compare_df['Salary'] / compare_df['Total Cost']

        fig_compare = px.bar(compare_df, x='City', y='Total Cost', color='City', title="Total Monthly Cost by City")
        st.plotly_chart(fig_compare)

        fig_scatter = px.scatter(compare_df, x='Salary', y='Total Cost', color='City', size='Affordability Index',
                                title="Affordability: Salary vs Total Cost")
        st.plotly_chart(fig_scatter)


    with tabs[2]:
        st.subheader("🧲 Budget Planner")
        budget = st.slider("Set your monthly budget", 5000, 100000, 30000)
        if filtered_df['Total Cost'].values[0] <= budget:
            st.success(f"{selected_city} fits your budget!")
        else:
            st.warning(f"{selected_city} exceeds your budget.")

    with tabs[3]:
        st.subheader("🗺️ Map View")
        city_coords = {
            "Delhi": [28.7041, 77.1025],
            "Mumbai": [19.0760, 72.8777],
            "Bengaluru": [12.9716, 77.5946],
            "Chennai": [13.0827, 80.2707],
            "Hyderabad": [17.3850, 78.4867],
            "Kolkata": [22.5726, 88.3639],
            "Pune": [18.5204, 73.8567],
            "Ahmedabad": [23.0225, 72.5714],
            "Jaipur": [26.9124, 75.7873],
            "Lucknow": [26.8467, 80.9462],
            "Chandigarh": [30.7333, 76.7794],
            "Bhopal": [23.2599, 77.4126],
            "Nagpur": [21.1458, 79.0882],
            "Kochi": [9.9312, 76.2673],
            "Bhubaneswar": [20.2961, 85.8245],
            "Guwahati": [26.1445, 91.7362]
        }

        if selected_city in city_coords:
            lat, lon = city_coords[selected_city]

            # Create Folium map
            m = folium.Map(location=[lat, lon], zoom_start=10, tiles="CartoDB positron")

            # Take the selected city's row safely
            row = filtered_df.iloc[0]

            # Create popup (string only, no functions!)
            popup_html = f"""
            <b>{selected_city}</b><br>
            💰 Salary: ₹{row['Salary']:,}<br>
            🏠 Rent: ₹{row['Rent']:,}<br>
            🛒 Groceries: ₹{row['Groceries']:,}<br>
            🚇 Transport: ₹{row['Transport']:,}<br>
            📊 Total Cost: ₹{row['Total Cost']:,}<br>
            ⚖️ Affordability Index: {row['Affordability Index']:.2f}
            """

            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=250),  # ✅ wrapped in folium.Popup
                tooltip=f"{selected_city}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

            # Render map safely
            st_folium(m, width=725, height=500)
        else:
            st.info("Coordinates not available for this city.")

    with tabs[4]:
        st.subheader("🧮 Cost Calculator")
        milk_qty = st.number_input("Milk (liters)", 0.0, 10.0, 1.0)
        bread_qty = st.number_input("Bread (loaves)", 0.0, 10.0, 1.0)
        rice_qty = st.number_input("Rice (kg)", 0.0, 10.0, 1.0)
        milk_price = clean_numeric(filtered_df['Milk (regular), (1 liter)']).values[0]
        bread_price = clean_numeric(filtered_df['Loaf of Fresh White Bread (500g)']).values[0]
        rice_price = clean_numeric(filtered_df['Rice (white), (1kg)']).values[0]
        total = milk_qty * milk_price + bread_qty * bread_price + rice_qty * rice_price
        st.write(f"Estimated Grocery Cost: ₹{total:.2f}")

    with tabs[5]:
        st.subheader("🗃️ Raw Data Explorer")
        st.dataframe(filtered_df)

    with tabs[6]:
        st.subheader("📤 Upload Your Data")
        uploaded_file = st.file_uploader("Upload a CSV file")
        if uploaded_file:
            uploaded_df = pd.read_csv(uploaded_file)
            st.write("First 5 rows of uploaded data:")
            st.dataframe(uploaded_df.head())

# -------------------- Smart Recommendations --------------------
elif selected_page == "🌟 Recommendations":
    st.title("🌟 Smart City Recommendations")
    st.markdown("""
    Here are the top cities based on your salary-to-cost ratio 🔍💡
    """)
    top_cities = recommend_city(data)
    st.dataframe(top_cities[['City', 'Affordability Score']])