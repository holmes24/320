# app.py
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load your data here
books = pd.read_csv("Books.csv")
ratings = pd.read_csv("Ratings.csv") 
users = pd.read_csv("Users.csv")

# Merge data and filter
merged_data1 = pd.merge(books, ratings, on='ISBN')
merged_data = pd.merge(merged_data1, users, on='userId')
merged_data = merged_data.sort_values('ISBN', ascending=True)

# Data processing for recommendations
x = merged_data.groupby("userId").count()["bookRating"] > 200
educated_users = x[x].index
filtered_rating = merged_data[merged_data["userId"].isin(educated_users)]
y = filtered_rating.groupby("bookTitle").count()["bookRating"] >= 50
famous_books = y[y].index
final_ratings = filtered_rating[filtered_rating["bookTitle"].isin(famous_books)]

pt = final_ratings.pivot_table(index="bookTitle", columns="userId", values="bookRating")
pt.fillna(0, inplace=True)
similarity_scores = cosine_similarity(pt)

# Streamlit app code
def get_user_ratings(user_id, books_to_check):
    user_id = int(user_id)

    if user_id in pt.columns:
        book_ratings = {}
        for book_title in books_to_check:
            if book_title in pt.index:
                rating = pt.loc[book_title, user_id]
                if pd.notna(rating):
                    book_ratings[book_title] = rating
                else:
                    book_ratings[book_title] = f"User {user_id} has not rated '{book_title}'."
            else:
                book_ratings[book_title] = f"Book '{book_title}' not found in the dataset."

        return book_ratings
    else:
        return f"Invalid User ID: {user_id}. Please enter a valid User ID."

# Streamlit app code
def main():
    st.title("Book Ratings App")

    # Get user input
    user_id_to_check = st.text_input("Enter User ID:")

    # Specify the books to check
    books_to_check = ["The Golden Compass (His Dark Materials, Book 1)", "The Eyre Affair: A Novel", "Seabiscuit: An American Legend", "The Amber Spyglass (His Dark Materials, Book 3)", "Coraline"]

    # Display results
    result = get_user_ratings(user_id_to_check, books_to_check)
    st.subheader(f"Ratings for User {user_id_to_check} for the specified books:")
    for book_title, rating in result.items():
        st.write(f"{book_title}: {rating}")

if __name__ == "__main__":
    main()
