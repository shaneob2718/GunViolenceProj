import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Page setup
st.set_page_config(page_title="Gun Violence Analysis", layout="wide")
st.title("Mass Shootings in the U.S. (2015-2023)")

#======================== Loading in the Data ===============================
ms_2015 = pd.read_csv('MS_2015.csv', delimiter=',')
ms_2016 = pd.read_csv('MS_2016.csv', delimiter=',')
ms_2017 = pd.read_csv('MS_2017.csv', delimiter=',')
ms_2018 = pd.read_csv('MS_2018.csv', delimiter=',')
ms_2019 = pd.read_csv('MS_2019.csv', delimiter=',')
ms_2020 = pd.read_csv('MS_2020.csv', delimiter=',')
ms_2021 = pd.read_csv('MS_2021.csv', delimiter=',')
ms_2022 = pd.read_csv('MS_2022.csv', delimiter=',')
ms_2023 = pd.read_csv('MS_2023.csv', delimiter=',')

# Concatenate all the data into one data frame:
ms_data = pd.concat([ms_2015, ms_2016, ms_2017, ms_2018, ms_2019,ms_2020, ms_2021, ms_2022, ms_2023], ignore_index=True)

# Data Cleaning and Definition: 

# General Info
ms_data['Incident Date'] = pd.to_datetime(ms_data['Incident Date'], format='%B %d, %Y')
ms_year = ms_data['Incident Date'].dt.year

ms_state = ms_data['State']
ms_deaths = ms_data['Victims Killed']
ms_injured = ms_data['Victims Injured']
# Total victims
ms_total_vics = ms_deaths + ms_injured
# Suspect data
ms_susdeaths = ms_data['Suspects Killed']
ms_susinjured = ms_data['Suspects Injured']
ms_susarrested = ms_data['Suspects Arrested']

# We can define these for individual years too!

#========================== Variable Definitions =============================

# State name and abbreviation list
# We get a list of all state names
us_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

us_state_abbreviations = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

#========================== Tabs & Pages =============================

# Create tabs
tab_intro, tab1, tab2, tab3 = st.tabs([
    "Introduction", 
    "Mass Shootings by Year", 
    "Mass Shootings by State", 
    "Mass Shootings by Month"
])

# 📊 
with tab_intro:
    st.header("Mass Shooting Data Dashboard")
    st.markdown("""

    This tool was built to explore mass shooting data in the United States. "Mass Shootings", in this context, are defined as 
    incidents that result in four or more people being shot, but not necessarily killed. 
    This is not inclusive of the shooter themselves. "Victims" are defined as the sum of those injured and those who were killed.

    ### Contents:
    - **Mass Shootings by Year**: A yearly breakdown of incidents, showing how the frequnecy of these events change over time.
    - **Mass Shootings by State**: Total incidents per state, showing which states have the highest rates.
    - **Mass Shooting by Month**: Total incidents per month, showing which months (and thus seasons) have a higher number of mass 
        shooting incidents.

    ---
    **Data Sources**:
    - [Gun Violence Archive](https://www.gunviolencearchive.org/)
    - [U.S. Census Bureau (2020)](https://www.census.gov/)
    """)

    st.info("Dashboard was created for educational purposes only. Data Sourced from provided sources.")

#
#with tab1:
#    st.header("Mass Shootings per Year")
#    fig1, ax1 = plt.subplots()
#    ax1.hist(ms_year, bins=range(ms_year.min(), ms_year.max() + 1), edgecolor='black', align='left')
#    ax1.set_title("Mass Shootings per Year")
#    ax1.set_xlabel("Year")
#    ax1.set_ylabel("Number of Incidents")
#    ax1.grid(axis='y', alpha=0.7)
#    st.pyplot(fig1, use_container_width=False)

with tab1:
    st.header("Mass Shootings by Year")

    # Create 2 columns: one for text, one for the plot
    col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

    with col1:
        st.subheader("Mass Shootings Over Time")
        st.markdown("""
        This histogram shows the number of **mass shooting incidents per year** between 2015 and 2023. 
                    
        - Mass shooting incidents have seen a rise in prevalence since the beginning of the 2020 decade.
        - Yearly rates appear to have kept at a high level (compared to pre-2020 data) since 2020
        
        """)

    with col2:
        #st.subheader("Mass Shootings Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(ms_year, bins=range(ms_year.min(), ms_year.max() + 2), edgecolor='black', align='left')
        #ax.set_title("Mass Shootings per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Incidents")
        ax.set_xticks(list(range(ms_year.min(), ms_year.max() + 1)))
        ax.grid(axis='y', alpha=0.7)
        st.pyplot(fig)

    st.subheader(f"Metrics for Each Year")
    # Add Year column to DataFrame
    ms_data['Year'] = ms_year

    # Get sorted list of unique years
    year_list = sorted(ms_data['Year'].dropna().unique().astype(int))
    selected_year = None

    # Create button columns (max 5 per row for layout)
    year_buttons = ['All Years (Total)'] + [str(year) for year in year_list]
    cols = st.columns(len(year_buttons))

    # Button row to select year
    cols = st.columns(len(year_buttons))
    selected_year = None

    for i, label in enumerate(year_buttons):
        if cols[i].button(label, key=f"year_button_{label}"):
            selected_year = label

    # Default to "All Years" if no button pressed yet
    if selected_year is None:
        selected_year = 'All Years (Total)'

    # Filter data
    if selected_year == 'All Years (Total)':
        filtered_data = ms_data
    else:
        filtered_data = ms_data[ms_data['Year'] == int(selected_year)]

    # Calculate metrics
    num_incidents = len(filtered_data)
    num_killed = filtered_data['Victims Killed'].sum()
    num_injured = filtered_data['Victims Injured'].sum()
    num_total_victims = num_killed + num_injured

    # Display metrics
    #st.subheader(f"Metrics for {selected_year}")
    col3, col4, col5, col6 = st.columns(4)
    with col3: st.metric("Incidents", num_incidents)
    with col4: st.metric("Killed", int(num_killed))
    with col5: st.metric("Injured", int(num_injured))
    with col6: st.metric("Total Victims", int(num_total_victims))

    col7, col8 = st.columns([1, 2])
    with col7:
        st.subheader("Total Victims per Year")
        st.markdown("""
        This histogram shows the number of **mass shooting victims per year** between 2015 and 2023. 
                    
        - Just as is the case with the number of incidents, the number of victims appears to have increased to a new avereage level in 2020
        - Just like with the number of incidents, the number of victims per year appear to have kept at a high level (compared to pre-2020 data) since 2020
        
        """)
    with col8:
        # Create a DataFrame combining years and total victims
        victims_df = pd.DataFrame({
            'Year': ms_year,
            'Total Victims': ms_total_vics
        })

        # Group by year and sum victims
        victims_per_year = victims_df.groupby('Year')['Total Victims'].sum().sort_index()

        # Streamlit plot
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(victims_per_year.index, victims_per_year.values, edgecolor='black')
        #ax.set_title("Total Victims per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Victims")
        ax.set_xticks(range(ms_year.min(), ms_year.max() + 1))
        ax.set_xticklabels(range(ms_year.min(), ms_year.max() + 1), rotation=45)
        ax.grid(axis='y', alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig)


with tab2:
    st.header("Mass Shootings by State")
    col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

    with col1:
        st.subheader("Mass Shooting Incidents per State (Total)")
        st.markdown("""
        This histogram shows the total number of **mass shooting incidents per state** between 2015 and 2023. 
                    
        - Illinois notably has the highest number of mass shootings over this 8 year period
        
        """)

    with col2:
        # Need to count incidents per state:
        incidents_by_state = [] # In alphabetical order, to be plotted with above name list
        for name in us_states: # For each state name
            count = 0
            for incident in ms_state: # Count the amount of times the name occurs
                if incident == name:
                    count+=1
                else:
                    pass
            incidents_by_state.append(count) # Append that count to the incidents list

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(us_state_abbreviations, incidents_by_state)
        #ax.set_title("Number of Mass Shootings per State (2015-2023)")
        ax.set_xlabel("State")
        ax.set_ylabel("Number of Incidents")
        ax.set_xticks(range(len(us_state_abbreviations)))
        ax.set_xticklabels(us_state_abbreviations, rotation=45)
        ax.grid(axis="y", alpha=0.7)
        fig.tight_layout()
        st.pyplot(fig)
        


with tab3:
    st.header("Mass Shootings by Month")

    col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

    with col1:
        st.subheader("Mass Shooting Incidents per Season")
        st.markdown("""
        This histogram shows the number of **mass shooting incidents per year** between 2015 and 2023. 
                    
        - Mass shooting incidents have seen a rise in prevalence since the beginning of the 2020 decade.
        - Yearly rates appear to have kept at a high level (compared to pre-2020 data) since 2020
        
        """)
    with col2:
        # Make sure 'Incident Date' is in datetime format
        ms_data['Incident Date'] = pd.to_datetime(ms_data['Incident Date'], errors='coerce')

        # Extract month and day
        ms_data['Month'] = ms_data['Incident Date'].dt.month
        ms_data['Day'] = ms_data['Incident Date'].dt.day

        # Define a function to assign seasons
        def get_season(row):
            month = row['Month']
            day = row['Day']
            
            if (month == 12 and day >= 21) or (month <= 3 and (month != 3 or day < 20)):
                return 'Winter'
            elif (month == 3 and day >= 20) or (month == 4) or (month == 5) or (month == 6 and day < 21):
                return 'Spring'
            elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day < 23):
                return 'Summer'
            elif (month == 9 and day >= 23) or (month == 10) or (month == 11) or (month == 12 and day < 21):
                return 'Fall'
            else:
                return 'Unknown'

        # Apply season assignment
        ms_data['Season'] = ms_data.apply(get_season, axis=1)

        # Group by season
        season_counts = ms_data['Season'].value_counts().reindex(['Winter', 'Spring', 'Summer', 'Fall'])

        # Plot in Streamlit
        fig, ax = plt.subplots(figsize=(10, 4))
        season_counts.plot(kind='bar', edgecolor='black', ax=ax)
        #ax.set_title("Mass Shootings by Season")
        ax.set_xlabel("Season")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.set_ylabel("Number of Incidents")
        ax.grid(axis='y', alpha=0.5)
        plt.tight_layout()

        # Show plot
        st.pyplot(fig)

    col3, col4 = st.columns([1, 2])  # Adjust width ratio if needed
    with col3:
        st.subheader("Periodic Trend of Mass Shooting Events")
        st.markdown("""
        This histogram shows the number of **mass shooting incidents per year** between 2015 and 2023. 
                    
        - Mass shooting incidents have seen a rise in prevalence since the beginning of the 2020 decade.
        - Yearly rates appear to have kept at a high level (compared to pre-2020 data) since 2020
        
        """)
    with col4:
        # Load your data here
        # ms_data = pd.read_csv('your_data.csv')

        # Ensure datetime format and extract monthly period
        ms_data['Incident Date'] = pd.to_datetime(ms_data['Incident Date'], errors='coerce')
        ms_data['Month'] = ms_data['Incident Date'].dt.to_period('M')

        # Group by Month and count incidents
        monthly_trend = ms_data.groupby('Month').size()

        # Convert PeriodIndex to datetime for plotting
        monthly_trend.index = monthly_trend.index.to_timestamp()

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(monthly_trend.index, monthly_trend.values)

        # Add vertical lines for each June — only label the first one
        first = True
        for date in monthly_trend.index:
            if date.month == 6:
                if first:
                    ax.axvline(x=date, color='red', linestyle='--', alpha=0.5, label="June 1st Spike")
                    first = False
                else:
                    ax.axvline(x=date, color='red', linestyle='--', alpha=0.5)

        # Labeling and styling
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Incidents")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        fig.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(fig)
    
    col5, col6 = st.columns([1, 2])  # Adjust width ratio if needed

    with col5:
        st.subheader("Fitting a Periodic Model to the Data")
        st.markdown("""
        This histogram shows the number of **mass shooting incidents per year** between 2015 and 2023. 
                    
        - Mass shooting incidents have seen a rise in prevalence since the beginning of the 2020 decade.
        - Yearly rates appear to have kept at a high level (compared to pre-2020 data) since 2020
        
        """)
    with col6:
        # --- Step 1: Process data ---

        # Ensure 'Incident Date' is datetime
        ms_data['Incident Date'] = pd.to_datetime(ms_data['Incident Date'], errors='coerce')

        # Extract month (year + month only)
        ms_data['Month'] = ms_data['Incident Date'].dt.to_period('M')

        # Group by month and count number of incidents
        monthly_trend = ms_data.groupby('Month').size()

        # Convert PeriodIndex to datetime (first day of each month)
        monthly_trend.index = monthly_trend.index.to_timestamp()

        # --- Step 2: Create periodic features ---
        # Time index: 0, 1, ..., N
        t = np.arange(len(monthly_trend))
        y = monthly_trend.values

        # Add sin and cos components for 12-month cycle + harmonics
        X = np.column_stack([
            np.sin(2 * np.pi * t / 12),
            np.cos(2 * np.pi * t / 12),
            np.sin(4 * np.pi * t / 12),
            np.cos(4 * np.pi * t / 12),
            np.sin(6 * np.pi * t / 12),
            np.cos(6 * np.pi * t / 12),
        ])

        # Fit linear regression model to sin/cos basis
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # --- Step 3: Plot in Streamlit ---
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot actual data
        ax.plot(monthly_trend.index, y, label="Actual Monthly Incidents", marker='o')

        # Plot fitted trend
        ax.plot(monthly_trend.index, y_pred, label="Fitted Periodic Trend (12-month)", linestyle='--')

        # Labels and legend
        #ax.set_title("Monthly Mass Shooting Incidents with Periodic Model")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Incidents")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)







#with tab2:
#    st.header("Mass Shootings by State")
#    fig2, ax2 = plt.subplots(figsize=(12, 6))
#    ax2.bar(us_state_abbreviations, incidents_by_state)
#    ax2.set_title("Mass Shootings per State (2022–2025)")
#    ax2.set_xlabel("State")
#    ax2.set_ylabel("Number of Incidents")
#    ax2.grid(axis='y', alpha=0.7)
#    plt.xticks(rotation=45)
#    #st.pyplot(fig2)
#    st.pyplot(fig2, use_container_width=False)


#with tab3:
#    st.header("Mass Shootings per Capita")
#    fig3, ax3 = plt.subplots(figsize=(12, 6))
#    ax3.bar(us_state_abbreviations, incidents_per_capita)
#    ax3.set_title("Mass Shootings per 100,000 People")
#    ax3.set_xlabel("State")
#    ax3.set_ylabel("Incidents per 100,000 people")
#    ax3.grid(axis='y', alpha=0.7)
#    plt.xticks(rotation=45)
#    #st.pyplot(fig3)
#    st.pyplot(fig3, use_container_width=False)
