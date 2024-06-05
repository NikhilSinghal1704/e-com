from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "Index"),
    path('books/<int:book_id>/', views.book_details, name='book_details'),
    path('likedislike/<int:book_id>/<int:likedislike>/', views.likedislike, name='likedislike'),
    path('addtocart/<int:book_id>/', views.add_to_cart, name='addtocart'),
    path('subtractfromcart/<int:book_id>/', views.subtract_from_cart, name='subtractfromcart'),
    path('removefromcart/<int:book_id>/', views.remove_from_cart, name='removefromcart'),
    path('cart/', views.cart, name='cart'),
]