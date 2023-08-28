import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
def load_data(dataset="For 07-2019 to 06-2023"):
    if dataset == "For 07-2019 to 06-2023":
        filepath = "all_files_in_one02.csv"
    else:
        filepath = "all_files_in_one01.csv"
    df = pd.read_csv(filepath)
    

    visualize_item_usage_per_center(df)
def visualize_item_usage_per_center(df):
    unique_centers = df['Center Name'].unique()
    st.title("Frequent Item Usage per Center Visualization")

    # Select a center
    selected_center = st.selectbox("Select a Center", unique_centers)

    # Number of top items to show
    max_num_items = min(len(unique_centers), 15)
    num_items = st.number_input("Number of Top Items", min_value=1, max_value=max_num_items, value=5)

    # Filter data for the selected center
    center_df = df[df['Center Name'] == selected_center]

    # Get the top 'n' frequent items
    top_frequent_items = center_df['Item Name'].value_counts().nlargest(num_items).index

    data = []
    for item in top_frequent_items:
        count = center_df[center_df['Item Name'] == item]['Item Name'].count()
        data.append({'Center Name': selected_center, 'Item Name': item, 'Frequency': count})

    grouped_df = pd.DataFrame(data)
    plt.figure(figsize=(15, 8))  # Increase the figure size for better clarity
    sns.set(font_scale=1)
    ax = sns.barplot(x='Item Name', y='Frequency', data=grouped_df)
    
    # Annotate each bar with its respective value
    for p in ax.patches:
        ax.annotate(str(int(p.get_height())), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    
    plt.title(f"Top {num_items} Frequent Items Sold in {selected_center}")
    plt.xlabel("Item Name")
    plt.ylabel("Frequency")
    plt.xticks(rotation=70)  # Adjust rotation of x-axis labels
    plt.tight_layout()  # Adjust layout for better view
    st.pyplot(plt)


if __name__ == "__main__":
    # Sidebar navigation
    st.sidebar.title("Navigation")

    # New dataset filter
    datasets = ["For 07-2019 to 06-2023","For 01-2017 to 06-2019"]
    selected_dataset = st.sidebar.selectbox("Select Dataset", datasets)

    # Load the dataset based on user's selection
    df = load_data(selected_dataset)

    

