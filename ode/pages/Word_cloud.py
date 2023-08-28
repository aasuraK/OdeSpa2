import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.sidebar.title("Navigation")
def word_cloud_app():
    dp = pd.read_csv("reviews_with_center.csv")

    def preprocess_review(review):
        words = review.split()
        words = [word for word in words if not word[0].isdigit() and not word[-1].isdigit() and not any(c.isdigit() for c in word)]
        return ' '.join(words)

    def create_word_cloud(stemmed_reviews, selected_center, rating_label):
        vectorizer = CountVectorizer(stop_words='english')
        review_matrix = vectorizer.fit_transform(stemmed_reviews)
        review_df = pd.DataFrame(review_matrix.toarray(), columns=vectorizer.get_feature_names_out())
        word_frequencies = review_df.sum()
        top_words = word_frequencies.nlargest(20)
        wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_words)

        st.subheader(f"Top Words Word Cloud for {selected_center} - {rating_label}")
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    st.title("Center's rating based wordcloud")
    selected_center = st.sidebar.selectbox("Select a Center", dp['Center'].unique())

    low_rating_reviews = dp[(dp['Center'] == selected_center) & (dp['Rating'] <= 3)]['Review']
    high_rating_reviews = dp[(dp['Center'] == selected_center) & (dp['Rating'] > 3)]['Review']

    low_rating_stemmed_reviews = [preprocess_review(review) for review in low_rating_reviews]
    high_rating_stemmed_reviews = [preprocess_review(review) for review in high_rating_reviews]

    if high_rating_stemmed_reviews:
        show_high_rating_cloud = st.sidebar.checkbox("Show High Rating Word Cloud")
        if show_high_rating_cloud:
            create_word_cloud(high_rating_stemmed_reviews, selected_center, "High Ratings")

    if low_rating_stemmed_reviews:
        if len(low_rating_stemmed_reviews) > 1:  # Check if there are enough reviews for a word cloud
            show_low_rating_cloud = st.sidebar.checkbox("Show Low Rating Word Cloud")
            if show_low_rating_cloud:
                create_word_cloud(low_rating_stemmed_reviews, selected_center, "Low Ratings")

if __name__ == "__main__":
    word_cloud_app()
