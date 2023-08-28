import pandas as pd
import streamlit as st
import seaborn as sb
import matplotlib.pyplot as plt
st.sidebar.title("Navigation")
filepath1 = r"G:/pathsetter/all_files_in_one01.csv"
data1 = pd.read_csv(filepath1)
filepath2= r"G:/pathsetter/all_files_in_one02.csv"
data2 = pd.read_csv(filepath2)
#data2.drop(columns=['Unnamed: 19','Unnamed: 20'],inplace=True)
data=pd.concat([data1,data2])
data['Sale Date'] = pd.to_datetime(data['Sale Date'], dayfirst=True)
data['monthAndYear'] = data['Sale Date'].dt.strftime('%m-%Y')
data['monthExtention'] = data['Sale Date'].dt.month
data['Center Name'] = data['Center Name'].str.replace('Ahmadabad', 'Ahmedabad')
# Extract city names and create a new 'city' column
city_extract = data['Center Name'].str.extract(r'([A-Za-z\s]+)(?=\s*-\s)')[0]
city_extract.fillna(data['Center Name'], inplace=True)
data['city'] = city_extract
data['city'] = data['city'].replace({'Ahmedabad Narayani Hotel': 'Ahmedabad'})
data['city'] = data['city'].replace({'Bangalore Forum Whitefield': 'Bangalore'})
data['city'] = data['city'].replace({'Bangalore Grand Mercure': 'Bangalore'})
data['city'] = data['city'].replace({'Bangalore Kamanhalli': 'Bangalore'})
data['city'] = data['city'].replace({'Bangalore La Marvella hotel': 'Bangalore'})
data['city'] = data['city'].replace({'Bangalore Novotel hotel': 'Bangalore'})
data['city'] = data['city'].replace({'Bangalore Sarjapur': 'Bangalore'})
data['city'] = data['city'].replace({'Chennai Express Avenue': 'Chennai'})
data['city'] = data['city'].replace({'Delhi Airport': 'Delhi'})
data['city'] = data['city'].replace({'Pune Baner': 'Pune'})
data['city'] = data['city'].replace({'Pune Corinthians': 'Pune'})
data['city'] = data['city'].replace({'Pune Sayaji Hotel': 'Pune'})
data['city'] = data['city'].replace({'Goa Acron Regina': 'Goa'})
data['city'] = data['city'].replace({'Goa International Airport': 'Goa'})
data['city'] = data['city'].replace({'Goa Lemon Tree': 'Goa'})
data['city'] = data['city'].replace({'Google Delhi': 'Delhi'})
data['city'] = data['city'].replace({'Gurgaon DoubleTree': 'Gurgaon'})
data['city'] = data['city'].replace({'Gurgaon Fortune Hotel': 'Gurgaon'})
data['city'] = data['city'].replace({'Hyd': 'Hyderabad'})
data['city'] = data['city'].replace({'HYD': 'Hyderabad'})
data['city'] = data['city'].replace({'Hyd-Radisson': 'Hyderabad'})
data['city'] = data['city'].replace({'Jaipur golden tulip': 'Jaipur'})
data['city'] = data['city'].replace({'Jaipur Hilton': 'Jaipur'})
data['city'] = data['city'].replace({'Jaipur Pink Square Mall': 'Jaipur'})
data['city'] = data['city'].replace({'Mumbai airport Lounge-1': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai airport Lounge-2': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Lemon Tree': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Niranta hotel': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Niranta Hotel-2': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Niranta Hotel-3': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Niranta Hotel-4': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Novotel': 'Mumbai'})
data['city'] = data['city'].replace({'Mumbai Novotel Khopoli': 'Mumbai'})
data['city'] = data['city'].replace({'Nagpur Le Meridien': 'Nagpur'})
# Streamlit layout containers
with st.container():
    st.title("WELCOME TO ODE SPA")
    selectbox_label = "<h3>Select a city:</h3>"
    st.sidebar.markdown(selectbox_label, unsafe_allow_html=True)
    selected_city = st.sidebar.selectbox("", data['city'].unique())
with st.container():
    # Filter data for the selected city
    city_data = data[data['city'] == selected_city]
    # Calculate the first contact month for each Guest Code
    first_contract_month = city_data.groupby(['Guest Code'])['monthExtention'].min()
    first_contract_month.name = 'first_contact_month'
    # Join the first contract month information back to the city data
    city_data = city_data.join(first_contract_month, on='Guest Code')
    # Fill missing values and convert to integers
    city_data['first_contact_month'] = city_data['first_contact_month'].fillna(0).astype(int)
    city_data['monthExtention'] = city_data['monthExtention'].fillna(0).astype(int)
    # Calculate the cohort lifetime
    city_data['cohort_lifetime'] = city_data['monthExtention'] - city_data['first_contact_month']
    city_data['monthAndYear'] = pd.to_datetime(city_data['monthAndYear'], format='%m-%Y')
    city_data['half_year'] = 'H1-' + city_data['monthAndYear'].dt.year.astype(str)
    mask = city_data['monthAndYear'].dt.quarter > 2
    city_data.loc[mask, 'half_year'] = 'H2-' + city_data[mask]['monthAndYear'].dt.year.astype(str)
    # Calculate cohorts and retention
    cohorts = city_data.groupby(['half_year', 'cohort_lifetime'])['Guest Code'].nunique().reset_index()

    # Calculate the initial users count for each cohort
    initial_users_count = cohorts[cohorts['cohort_lifetime'] == 0][['half_year', 'Guest Code']].rename(
            columns={'Guest Code': 'cohort_users'})
    cohorts = cohorts.merge(initial_users_count, on='half_year')
    # Calculate the retention rate for each cohort
    cohorts['retention'] = cohorts['Guest Code'] / cohorts['cohort_users']

    # Pivot the retention data to create the retention pivot table
    retention_pivot = cohorts.pivot_table(index='half_year', columns='cohort_lifetime', values='retention',
                                              aggfunc='sum')

    # Create heatmap for user retention
    st.write("Cohorts: User Retention for FR")
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title('Cohorts: User Retention for FR')
    sb.heatmap(retention_pivot, annot=True, fmt='.1%', linewidths=1, linecolor='yellow')
    plt.xlabel("Cohort Lifetime")
    plt.ylabel("First Contract Month")

    # Display the figure using st.pyplot()
    st.pyplot(fig)
    unique_customers_in_filtered = city_data['Guest Code'].unique()
    # Filter data to include customers from both the selected city and other cities

    customers_in_both = data[data['Guest Code'].isin(unique_customers_in_filtered)]
    customers_in_other_cities = data[
        (data['Guest Code'].isin(unique_customers_in_filtered) == True) &
        (data['city'] != selected_city)]
    # Display customers who visited other cities

    st.title("Visited Other Cities ")
    sample = customers_in_other_cities.groupby('Guest Code')['Center Name'].unique().reset_index()
    sample['count'] = sample['Center Name'].apply(lambda x: ','.join(x))
    sample['count'] = sample['count'].str.split(',').str.len()
    sample1 = sample.groupby('count')['Center Name'].count().reset_index()
    x = sample1.rename(columns={'count': 'Unique cities', 'Center Name': 'unique customer count'})
    st.write(x)

