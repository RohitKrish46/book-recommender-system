import os
import sys
import pickle
import streamlit as st
import numpy as np
from recommender.logger.log import logging
from recommender.config.configuration import AppConfiguration
from recommender.pipelines.training_pipeline import TrainingPipeline
from recommender.exception.exception_handler import AppException


class Recommendation:
    def __init__(self,app_config = AppConfiguration()):
        try:
            self.recommendation_config= app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    def fetch_poster(self,suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot =  pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            final_rating =  pickle.load(open(self.recommendation_config.final_rating_serialized_objects,'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]: 
                ids = np.where(final_rating['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        


    def recommend_book(self,book_name):
        try:
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            book_pivot =  pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

            poster_url = self.fetch_poster(suggestion)
            
            for i in range(len(suggestion)):
                    books = book_pivot.index[suggestion[i]]
                    for j in books:
                        books_list.append(j)
            return books_list , poster_url   
        
        except Exception as e:
            raise AppException(e, sys) from e


    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training Completed!")
            logging.info("Recommended successfully!")
        except Exception as e:
            raise AppException(e, sys) from e

    
    def recommendations_engine(self,selected_books):
        try:
            recommended_books,poster_url = self.recommend_book(selected_books)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(poster_url[1])
            with col2:
                st.text(recommended_books[2])
                st.image(poster_url[2])

            with col3:
                st.text(recommended_books[3])
                st.image(poster_url[3])
            with col4:
                st.text(recommended_books[4])
                st.image(poster_url[4])
            with col5:
                st.text(recommended_books[5])
                st.image(poster_url[5])
        except Exception as e:
            raise AppException(e, sys) from e



if __name__ == "__main__":
    st.set_page_config(page_title="Book Recommender", layout="wide", page_icon="📚")
    st.title("📚 Book Recommender System")
    st.caption("A collaborative filtering-based engine to suggest similar books.")

    obj = Recommendation()

    with st.sidebar:
        st.header("Recommender Controls")
        if st.button('Train Recommender System'):
            with st.spinner("Training in progress..."):
                obj.train_engine()

    tab1, tab2 = st.tabs(["📖 Get Book Recommendations", "ℹ️ About This App"])

    with tab1:
        try:
            book_names = pickle.load(open(os.path.join('templates', 'book_names.pkl'), 'rb'))

            selected_book = st.selectbox(
                "📚 Choose a book you like:",
                book_names,
                help="This book will be used as a reference to recommend similar titles."
            )

            if st.button("🔍 Show Recommendations"):
                with st.spinner("Finding great reads..."):
                    recommended_books, poster_urls = obj.recommend_book(selected_book)

                    st.subheader(f"Books similar to *{selected_book}*")
                    cols = st.columns(len(poster_urls) - 1)

                    for i in range(1, len(poster_urls)):
                        with cols[i - 1]:
                            st.image(poster_urls[i], use_container_width="always", caption=recommended_books[i])

        except Exception as e:
            st.error("⚠️ Something went wrong. Please make sure the data is available.")
            st.exception(e)

    with tab2:
        st.markdown("""
        ### How it works:
        - Uses **collaborative filtering** to recommend similar books.
        - Trained on user rating data to find relationships between books.
        - Powered by **Scikit-learn KNN**, Streamlit, and preprocessed rating data.
        
        ### Features:
        - Train the system from the sidebar.
        - Get top 5 similar book recommendations with cover images.
        - Easily extendable to hybrid or content-based methods.
        """)
