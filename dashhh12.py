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
pages = ["🏠 Home", "ℹ️ About", "🔍 Filter & Insights", "📊 EDA", "🌟 Recommendations", "📞 Contact"]
selected_page = st.sidebar.radio("Navigate", pages)

# -------------------- Home --------------------
if selected_page == "🏠 Home":
    st.title("🌍 Global Cost of Living Explorer in India")
    st.markdown("""
Welcome to the **Smart City Cost and Affordability Dashboard** — an interactive platform that helps users 
**analyze and compare the cost of living across major Indian cities**.

💡 This dashboard provides insights into:
- 🏠 **Housing and rent prices**
- 🚗 **Transportation costs**
- 🛒 **Daily essentials and groceries**
- 💰 **Average salaries and affordability scores**
- 🌟 **AI-based city recommendations**
                
 Navigate the vibrant economics of Indian cities in one powerful dashboard 🚀

    **This tool allows you to:**
    - 🔎 Compare city-wise rent, groceries, transport, and salaries
    - 💰 Plan your relocation smartly with budget calculators
    - 🌐 Upload your own data to explore more

    **Made for dreamers, doers, and data lovers 💡**

Use the sidebar to explore:
- 📊 *Data Insights* — explore visual trends and comparisons  
- 💡 *Smart Recommendations* — find cities offering the best value for your budget  
- 📈 *EDA Section* — analyze the relationship between cost, salary, and lifestyle  

This project combines **data visualization**, **affordability modeling**, and **decision support** to guide
users in choosing cities that balance comfort and cost effectively.
""")


# -------------------- About --------------------
elif selected_page == "ℹ️ About":
    st.title("ℹ️ About This Dashboard")
    st.markdown("""
### 🎯 **Project Objective**
The **Smart City Cost and Affordability Dashboard** is designed to analyze and visualize 
the **cost of living across major Indian cities**.  
It helps users, students, and professionals identify **the most affordable and balanced cities** 
by comparing key parameters like rent, groceries, transportation, and salary.

---

### 🧠 **Key Features**
- 💰 **Affordability Analysis:** Calculates an affordability score using salary-to-expense ratio.  
- 📊 **Interactive Visualizations:** Explore city-wise comparisons using dynamic charts and maps.  
- 🌍 **Geographical Mapping:** View the top cities plotted on a real-time map using Folium.  
- 🤖 **Smart Recommendations:** Suggests cities that offer the best living value for your budget.  
- 📈 **Custom Analysis Tools:** Adjust budgets, compare spending patterns, and download reports.

---

### 🧮 **Data Description**
The dataset includes:
- **Average monthly salaries (after tax)**  
- **Rent of 1BHK apartments in city centres**  
- **Monthly transport pass prices**  
- **Groceries such as milk and rice**  
- **Derived affordability metrics**

All data has been **cleaned, standardized, and analyzed** to ensure reliability and comparability across cities.

---

### 🧰 **Technology Stack**
- 🐍 **Python**  
- 📊 **Pandas, NumPy** — data cleaning and computation  
- 📈 **Plotly, Matplotlib, Seaborn** — visualization  
- 🌐 **Streamlit** — interactive web interface  
- 🗺️ **Folium** — geographical mapping  

---

### 👩‍💻 **Team & Credits**
Developed as part of a **Data Analytics / Software Engineering project**  
by **[Your Name / Team Name]**, under the guidance of **[Mentor/Instructor Name]**.  
This project demonstrates how **data-driven decision-making** can help individuals 
choose better cities for living and working in India.

---

### 💡 **Future Enhancements**
- Integration with **real-time APIs** for updated cost-of-living data  
- Addition of **weather and safety indices**  
- Machine learning–based **predictive affordability modeling**
""")


# -------------------- EDA --------------------
elif selected_page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.subheader("1️. Summary Statistics")

 # --- Clean and handle missing data ---
    data['Salary'] = clean_numeric(data['Average Monthly Net Salary (After Tax)'])
    data['Rent'] = clean_numeric(data['Apartment (1 bedroom) in City Centre'])
    data['Milk'] = clean_numeric(data['Milk (regular), (1 liter)'])
    data['Bread'] = clean_numeric(data['Loaf of Fresh White Bread (500g)'])
    data['Rice'] = clean_numeric(data['Rice (white), (1kg)'])
    data['Groceries'] = data[['Milk', 'Bread', 'Rice']].sum(axis=1)
    data['Transport'] = clean_numeric(data['Monthly Pass (Regular Price)'])

# Drop rows with missing critical cost values
    data = data.dropna(subset=['Salary', 'Rent', 'Groceries', 'Transport'])

# --- Derived metrics ---
    data['Total Cost'] = data['Rent'] + data['Groceries'] + data['Transport']
    data['Affordability Index'] = np.where(data['Total Cost'] > 0, data['Salary'] / data['Total Cost'], np.nan)

# --- Calculate statistics manually using formulas ---
    mean_salary = data['Salary'].mean()
    median_salary = data['Salary'].median()
    mean_rent = data['Rent'].mean()
    median_rent = data['Rent'].median()
    mean_groceries = data['Groceries'].mean()
    mean_transport = data['Transport'].mean()
    mean_total_cost = data['Total Cost'].mean()
    median_total_cost = data['Total Cost'].median()
    mean_affordability = data['Affordability Index'].mean()
    std_affordability = data['Affordability Index'].std()

# --- Prepare clean summary table ---
    summary_stats = pd.DataFrame({
        "Metric": [
        "Average Salary (₹)",
        "Median Salary (₹)",
        "Average Rent (₹)",
        "Median Rent (₹)",
        "Average Groceries (₹)",
        "Average Transport (₹)",
        "Average Total Cost (₹)",
        "Median Total Cost (₹)",
        "Mean Affordability Index",
        "Std Dev of Affordability Index"
    ],
    "Value": [
        round(mean_salary, 2),
        round(median_salary, 2),
        round(mean_rent, 2),
        round(median_rent, 2),
        round(mean_groceries, 2),
        round(mean_transport, 2),
        round(mean_total_cost, 2),
        round(median_total_cost, 2),
        round(mean_affordability, 3),
        round(std_affordability, 3)
    ]
})

    st.dataframe(summary_stats, use_container_width=True)


    st.subheader("2. Correlation Heatmap")
    numeric_data = data.select_dtypes(include=[np.number])
    if not numeric_data.empty:      
        corr = numeric_data.corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)
    else:
        st.info("No numeric columns found for correlation analysis.")

    st.subheader("3. City-wise Distribution of Average Salary")
    data['Avg Salary Cleaned'] = clean_numeric(data['Average Monthly Net Salary (After Tax)'])
    fig_salary = px.box(data, x='City', y='Salary', points="all", title="Salary Distribution Across Cities")
    st.plotly_chart(fig_salary, use_container_width=True)

    st.subheader("4. Top 10 Expensive Cities by Rent")
    data['Rent'] = clean_numeric(data['Apartment (1 bedroom) in City Centre'])
    top_rent = data.sort_values(by='Rent', ascending=False).head(10)
    fig_rent = px.bar(top_rent, x='City', y='Rent', title="Top 10 Cities by Rent (City Centre)", color='Rent')
    st.plotly_chart(fig_rent)

    st.subheader("5. Affordability Index by City")
    fig_afford = px.bar(
        data.sort_values('Affordability Index', ascending=False),
        x='City', y='Affordability Index',
        color='Affordability Index',
        title="Affordability Index (Higher = More Affordable)"
    )
    st.plotly_chart(fig_afford, use_container_width=True)

    st.subheader("6. Spending Distribution Table")
    cost_columns = ['Apartment (1 bedroom) in City Centre', 'Monthly Pass (Regular Price)',
                'Milk (regular), (1 liter)', 'Loaf of Fresh White Bread (500g)', 'Rice (white), (1kg)']
    cost_df = data[['City'] + cost_columns].copy()

    # Normalize to percentage of total cost per city
    cost_df[cost_columns] = cost_df[cost_columns].apply(clean_numeric)
    cost_df['Total'] = cost_df[cost_columns].sum(axis=1)
    for col in cost_columns:
        cost_df[col] = (cost_df[col] / cost_df['Total']) * 100

    st.dataframe(cost_df.style.background_gradient(cmap='Blues'))

    st.subheader("7. Salary vs Total Cost Relationship")

    fig_scatter = px.scatter(
        data, x='Salary', y='Total Cost',
        color='City', size='Affordability Index',
        hover_name='City',
        trendline='ols',
        title="Correlation between Salary and Total Cost"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("8. Cost Components Trend Across Cities")

# Sort cities alphabetically for better visualization
    data_sorted = data.sort_values(by="City")

# Prepare a long-format dataframe for plotting multiple cost lines
    cost_trend_df = pd.melt(
        data_sorted,
        id_vars=['City'],
        value_vars=['Rent', 'Groceries', 'Transport'],
        var_name='Category',
        value_name='Cost'
    )

    fig_cost_trend = px.line(
        cost_trend_df,
        x='City', y='Cost',
        color='Category',
        markers=True,
        title="Trend of Major Monthly Expenses Across Cities"
    )

    fig_cost_trend.update_layout(
        xaxis_title="City",
        yaxis_title="Cost (₹)",
       legend_title="Expense Category"
    )
    st.plotly_chart(fig_cost_trend, use_container_width=True)

    


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
        "📤 Upload Your Data",
        "📊 Dataset Overview"
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

    with tabs[7]:
        st.subheader("Dataset Overview")
        st.dataframe(data)


# -------------------- Smart Recommendations --------------------
# -------------------- Smart Recommendations --------------------
elif selected_page == "🌟 Recommendations":
    st.title("🌟 Smart City Recommendations")
    st.markdown("""
    Here are the top cities based on your salary-to-cost ratio 🔍💡
    """)

    # --- Compute Top Cities by Affordability Score ---
    top_cities = recommend_city(data)

    st.subheader("📘 Recommendation Summary")

    avg_salary = data['Salary'].mean()
    avg_rent = data['Rent'].mean()
    avg_afford = data['Affordability Index'].mean()

    st.markdown(f"""
    The recommendations are based on the **Affordability Score** = Salary / (Rent + Transport + Basic Groceries).

    **National Averages:**
    - 💰 Average Salary: ₹{avg_salary:,.0f}  
    - 🏠 Average Rent: ₹{avg_rent:,.0f}  
    - ⚖️ Average Affordability Index: {avg_afford:.2f}

    Cities scoring higher than these are considered **better value-for-money**.
    """)

    # --- Bar Chart ---
    fig_top = px.bar(
        top_cities,
        x='City',
        y='Affordability Score',
        color='Affordability Score',
        text='Affordability Score',
        title="Top 5 Cities with Best Affordability",
        color_continuous_scale="viridis"
    )
    fig_top.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_top, use_container_width=True)

    # --- Best City Card ---
    st.subheader("🏆 Best City Overall")

    best_city = top_cities.iloc[0]
    st.markdown(f"""
    <div style="
        background-color:#f8fafc;
        padding:20px;
        border-radius:12px;
        box-shadow:0 2px 8px rgba(0,0,0,0.1);
        width:60%;
    ">
    <h3 style="color:#2b6cb0;">🌆 {best_city['City']}</h3>
    <p><b>Affordability Score:</b> {best_city['Affordability Score']:.2f}</p>
    <p><b>Salary:</b> ₹{best_city['Average Monthly Net Salary (After Tax)']}</p>
    <p><b>Rent:</b> ₹{best_city['Apartment (1 bedroom) in City Centre']}</p>
    <p><b>Transport:</b> ₹{best_city['Monthly Pass (Regular Price)']}</p>
    <p><b>Milk:</b> ₹{best_city['Milk (regular), (1 liter)']} | <b>Rice:</b> ₹{best_city['Rice (white), (1kg)']}</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- CONTACT PAGE --------------------
elif selected_page == "📞 Contact":

    st.title("📞 Contact & Feedback")

    st.markdown("""
Thank you for exploring the **Smart City Cost and Affordability Dashboard**! 🌆  
We’d love to hear your thoughts, suggestions, or collaboration ideas.

---

### ✉️ **Get in Touch**
                
-📍 **Location:** India 
-📧 **Email:** [inderpreet.kaur0605@gmail.com](mailto:inderpreet.kaur0605@gmail.com)  
-💼 **LinkedIn:** [LinkedIn](https://www.linkedin.com/in/inderpreet-kaur-59b4632b9?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)               
-🌐 **Portfolio / GitHub:** [https://github.com/Inderpreetkaur260](https://github.com/Inderpreetkaur260)  

---


""")






