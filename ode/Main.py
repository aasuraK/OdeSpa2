import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(
    page_title="Main App",
)
@st.cache_data
def convert_df_to_csv(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def display_table_with_download(df, title, filename):
    

    csv_data = convert_df_to_csv(df)
    st.download_button(
        label=f"Download {title} as CSV",
        data=csv_data,
        file_name=filename,
        mime='text/csv',
    )
def load_data(dataset="For 07-2019 to 06-2023"):
    if dataset == "For 07-2019 to 06-2023":
        filepath = "all_files_in_one02.csv"
    else:
        filepath = "all_files_in_one01.csv"

    data = pd.read_csv(filepath)
    data['Sale Date'] = pd.to_datetime(data['Sale Date'], errors='coerce')
    data[['Sales (Exc. Tax)', 'Tax', 'Sales(Inc. Tax)', 'Redeemed']] = data[['Sales (Exc. Tax)', 'Tax', 'Sales(Inc. Tax)', 'Redeemed']].replace(',', '', regex=True).astype(float)
    return data.dropna(subset=['Sale Date'])

def center_date_summary(selected_dataset):
    data = load_data(selected_dataset)  # Load the data within the function
    data['monthAndYear'] = data['Sale Date'].dt.to_period('M')
    st.title("Welcome To ODE SPA !!")
    st.title("Sales Summary by Center and Date")
    profile_image_path = "https://massagespaindia.com/oc-content/uploads/2/5977.webp"
    st.image(profile_image_path)
    
    st.sidebar.header("Filters")
    month_year_options = data['monthAndYear'].astype(str).unique()
    selected_month_year = st.sidebar.selectbox('Select Month-Year:', month_year_options)
    center_options = data[data['monthAndYear'].astype(str) == selected_month_year]['Center Name'].unique()
    selected_center = st.sidebar.selectbox('Select Center:', center_options)
    
    # Filter data based on selections
    filtered_data = data[(data['monthAndYear'].astype(str) == selected_month_year) & (data['Center Name'] == selected_center)]
    
 
    # Top 5 Selling Items
    top_5_items = filtered_data.groupby('Item Name')['Qty'].sum().nlargest(5).reset_index()
    top_5_items.index += 1
    st.subheader("Top 5 Selling Items")
    st.write(top_5_items)
    display_table_with_download(top_5_items, "Top 5 Selling Items", 'top_5_selling_items.csv')
    
    # Sales Trend for the Selected Month
    selected_month_data = data[data['monthAndYear'].astype(str) == selected_month_year]
    daily_sales_for_selected_month = selected_month_data.groupby(selected_month_data['Sale Date'].dt.date)['Sales(Inc. Tax)'].sum()
    st.subheader(f"Sales Trend for {selected_month_year}")
    st.line_chart(daily_sales_for_selected_month)
    
    # Top 5 Highest-Spending Customers
    top_5_customers = data.groupby('Guest Name')['Sales(Inc. Tax)'].sum().nlargest(5).reset_index()
    top_5_customers.index += 1
    st.subheader("Top 5 Highest-Spending Customers")
    st.write(top_5_customers)
    display_table_with_download(top_5_customers, "Top 5 Highest-Spending Customers", 'top_5_customers.csv')
    
    
    # Bar Chart for Top 3 Guests
    top_3_guests = filtered_data.groupby('Guest Name')['Sales(Inc. Tax)'].sum().nlargest(3).reset_index(name='Sales')
    top_3_guests.index += 1
    st.subheader("Top 3 Guests")
    fig, ax = plt.subplots()
    ax.barh(top_3_guests['Guest Name'], top_3_guests['Sales'])
    ax.set_xlabel('Sales')
    ax.set_ylabel('Guest Name')
    ax.invert_yaxis()
    st.pyplot(fig)
    
    # Redeemed Values for Selected Center
    redeemed_values = filtered_data.groupby('Item Name')['Redeemed'].sum().reset_index()
    redeemed_values.index += 1
    st.subheader("Redeemed Values for Selected Center")
    st.write(redeemed_values)
    display_table_with_download(redeemed_values, "Redeemed Values for Selected Center", 'redeemed_values.csv')
    
    
    # Items-wise Sales - Top 5
    item_sales = filtered_data.groupby('Item Name')['Sales(Inc. Tax)'].sum().nlargest(5).reset_index().sort_values(by='Sales(Inc. Tax)', ascending=False)
    item_sales.index += 1
    st.subheader("Top 5 Items-wise Sales")
    st.write(item_sales)
    display_table_with_download(item_sales, "Top 5 Items-wise Sales", 'item_sales.csv')
        # Top 5 Selling Items by Quantity
    top_5_items_qty = filtered_data.groupby('Item Name')['Qty'].sum().nlargest(5).reset_index()
    
    # Items-wise Sales - Top 5 by Sales Value
    top_5_items_sales = filtered_data.groupby('Item Name')['Sales(Inc. Tax)'].sum().nlargest(5).reset_index().sort_values(by='Sales(Inc. Tax)', ascending=False)
    
    # Graphical Representation Button
    if st.button("Graphical Representation Of Items Sold[Top5]"):

        # Bar chart for Top 5 Selling Items by Quantity
        st.subheader("Top 5 Selling Items by Quantity")
        fig, ax = plt.subplots()
        top_5_items_qty.set_index('Item Name').sort_values(by='Qty', ascending=False)['Qty'].plot(kind='bar', ax=ax, color='skyblue')
        # Annotate bars
        for p in ax.patches:
            ax.annotate(str(int(round(p.get_height(), 2))), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.xticks(rotation=45, ha='right')
        ax.set_ylabel('Quantity Sold')
        st.pyplot(fig)

        # Bar chart for Top 5 Items-wise Sales by Sales Value
        st.subheader("Top 5 Items-wise Sales by Sales Value")
        fig, ax = plt.subplots()
        top_5_items_sales.set_index('Item Name').sort_values(by='Sales(Inc. Tax)', ascending=False)['Sales(Inc. Tax)'].plot(kind='bar', ax=ax, color='salmon')
        # Annotate bars
        for p in ax.patches:
            ax.annotate(str(int(round(p.get_height(), 2))), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.xticks(rotation=45, ha='right')
        ax.set_ylabel('Sales Value')
        st.pyplot(fig)
def year_summary(selected_dataset):
    data = load_data(selected_dataset) 
    data['Year'] = data['Sale Date'].dt.year
    st.title("Sales Summary by Year")
    
    year_options = sorted(data['Year'].unique())
    selected_year = st.selectbox('Select Year:', year_options)
    def count_repetitive_guests(group):
        guest_counts = group['Guest Name'].value_counts()
        repetitive_guest_count = guest_counts[guest_counts > 1].sum()
        return repetitive_guest_count if repetitive_guest_count else 0
    # Filter data based on selected year
    filtered_data = data[data['Year'] == selected_year]
    
    # Summary by Center for the Selected Year
    center_summary = filtered_data.groupby('Center Name').apply(
        lambda group: pd.Series({
            'Total_Quantity': group['Qty'].sum(),
            'Total_Sales_Without_Tax': group['Sales (Exc. Tax)'].sum(),
            'Average_Sales_Without_Tax': group['Sales (Exc. Tax)'].mean(),
            'Repetitive_Guest_Count': count_repetitive_guests(group),
        })
    ).reset_index()
    
    center_summary.index += 1  # Adjusting the index to start from 1
    st.subheader(f"Summary of Sales by Center for {selected_year}")
    st.write(center_summary)
    display_table_with_download(center_summary, "Summary of Sales by Center", 'Summary of Sales by Center.csv')
    
    # Custom y-axis formatter
    def custom_formatter(x, _):
        if x >= 1e7:  # Crores
            return f'{x*1e-7:.1f} Cr'
        elif x >= 1e5:  # Lakhs
            return f'{x*1e-5:.1f} L'
        else:  # Thousands
            return f'{x*1e-3:.1f} K'
    
    # Daywise sales for the selected year
    st.subheader(f"Sales from Monday to Sunday for {selected_year}")
    daywise_data = filtered_data.groupby(filtered_data['Sale Date'].dt.day_name())['Sales (Exc. Tax)'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ax = daywise_data.plot(kind='bar', color='lightblue', edgecolor='black')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(custom_formatter))
    plt.ylabel('Sales (Exc. Tax)')
    plt.title(f"Sales from Monday to Sunday for {selected_year}")
    st.pyplot(plt.gcf())
    plt.clf()
    
    # Top 5 Highest-Spending Customers for the selected year
    top_5_customers = filtered_data.groupby('Guest Name')['Sales(Inc. Tax)'].sum().nlargest(5).reset_index()
    top_5_customers.index += 1
    st.subheader(f"Top 5 Highest-Spending Customers for {selected_year}")
    st.write(top_5_customers)
    display_table_with_download(top_5_customers, f"Top 5 Highest-Spending Customers for {selected_year}", 'top_5_customers_year.csv')

    
    # Monthly sales for the selected year
    monthly_data = filtered_data.groupby(filtered_data['Sale Date'].dt.month_name())['Sales (Exc. Tax)'].sum().reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    ax = monthly_data.plot(kind='bar', color='lightgreen', edgecolor='black')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(custom_formatter))
    plt.ylabel('Sales (Exc. Tax)')
    plt.title(f"Monthly Sales for {selected_year}")
    st.pyplot(plt.gcf())
    plt.clf()

def main():
    st.sidebar.title("Navigation")

    # New dataset filter
    datasets = ["For 07-2019 to 06-2023", "For 01-2017 to 06-2019"]
    
    # Default to the first dataset ("For 08-2019 to 06-2023")
    selected_dataset = st.sidebar.selectbox("Select Dataset", datasets, index=0)

    pages = ["Sales Summary by Center and Date", "Sales Summary by Year"]
    selected_page = st.sidebar.selectbox("Go to", pages)

    if selected_page == "Sales Summary by Center and Date":
        center_date_summary(selected_dataset)
    elif selected_page == "Sales Summary by Year":
        year_summary(selected_dataset)



if __name__ == "__main__":
    main()
