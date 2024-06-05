from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Book, LikeDislike, Cart
#from .recommender import recommend_books

def index(request):
    context = {}
    
    # Query books with an average rating of more than 4
    top_rated_books = Book.objects.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=4)
    context['books'] = top_rated_books
    #print(recommend_books(request.user))
    return render(request, 'index.html', context)

def book_details(request, book_id):

    book = Book.objects.get(id=book_id)
    reviews = book.review_set.all()
    tags = book.tag_set.all()

    if request.user.is_authenticated:
        try:
            book.user_likedislike = LikeDislike.objects.get(book=book, user=request.user)
        except LikeDislike.DoesNotExist:
            book.user_likedislike = None

    return render(request, 'lol.html', {
        'book': book,
        'reviews': reviews,
        'tags' : tags
    })

@login_required
def likedislike(request, book_id, likedislike):
    book = get_object_or_404(Book, id=book_id)
    user = request.user
    try:
        like_dislike = LikeDislike.objects.get(user=user, book=book)
        if likedislike == 1:
            like_dislike.like = True
            like_dislike.save()
        elif likedislike == 0:
            like_dislike.like = False
            like_dislike.save()
        elif likedislike == 2:
            like_dislike.delete()
    except LikeDislike.DoesNotExist:
        if likedislike == 1:
            LikeDislike.objects.create(user=user, book=book, like=True)
        elif likedislike == 0:
            LikeDislike.objects.create(user=user, book=book, like=False)
    
    return redirect('book_details', book_id=book_id)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    cart_item, created = Cart.objects.get_or_create(book=book, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # Redirect back to the previous page or book details page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect(reverse('book_details', kwargs={'book_id': book_id}))

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    cart_item = Cart.objects.get(book=book, user=user)
    cart_item.delete()
    # Redirect back to the previous page or book details page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect(reverse('cart'))

@login_required
def subtract_from_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    cart_item = Cart.objects.get(book=book, user=user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    # Redirect back to the previous page or book details page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect(reverse('cart'))
    

@login_required
def cart(request):
    return render(request, 'cart.html')
