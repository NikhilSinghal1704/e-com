import pickle
import os
import streamlit as st
import numpy as np
from django.shortcuts import render
from .models import Book, LikeDislike

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'Artifacts', 'Model.pkl')
model = pickle.load(open(model_path, 'rb'))

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(Book.objects.get(id=book_id).title)

    for name in book_name[0]: 
        ids = LikeDislike.objects.filter(book__title=name).first().id
        ids_index.append(ids)

    for idx in ids_index:
        url = LikeDislike.objects.get(id=idx).poster_url
        poster_url.append(url)

    return poster_url

def recommend_books(user_id):
    user_likes = LikeDislike.objects.filter(user_id=user_id, like=True).values_list('book_id', flat=True)
    user_book_matrix = np.zeros((1, len(Book.objects.all())))
    for user_id, liked_book in enumerate(user_likes):
        user_book_matrix[0][liked_book - 1] = 1

    distance, suggestion = model.kneighbors(user_book_matrix, n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    recommended_books = []
    for i in range(len(suggestion)):
        book_id = suggestion[i][0]
        book = Book.objects.get(id=book_id)
        recommended_books.append((book.title, book.poster_url))

    return recommended_books, poster_url

def recommend_book_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        recommended_books, poster_url = recommend_books(user_id)
        return render(request, 'recommend_books.html', {'recommended_books': recommended_books, 'poster_url': poster_url})
    else:
        return render(request, 'recommend_books.html')