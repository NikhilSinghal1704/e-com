import os
import logging
from django.db import models
from Auth.models import CustomUser as User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

logger = logging.getLogger(__name__)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True, default='book_covers/default_cover.jpg')
    banner = models.ImageField(upload_to='book_banners/', null=True, blank=True, default='book_banners/default_banner.jpg')

    def __str__(self):
        return self.title
    
    def review_count(self):
        return self.review_set.count()
    
    def like_count(self):
        return self.likedislike_set.filter(like=True).count()

    def dislike_count(self):
        return self.likedislike_set.filter(like=False).count()
    
    def average_rating(self):
        average = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return round(average, 1) if average is not None else 0
    
    def delete(self, *args, **kwargs):
        if self.cover:
            logger.debug(f"Deleting cover image: {self.cover.path}")
            if os.path.exists(self.cover.path):
                os.remove(self.cover.path)
        if self.banner:
            logger.debug(f"Deleting banner image: {self.banner.path}")
            if os.path.exists(self.banner.path):
                os.remove(self.banner.path)
        super().delete(*args, **kwargs)
    
class Tag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.category} - {self.Book}"

class LikeDislike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        unique_together = ('book', 'user')  # Ensure a user can only like or dislike a book once

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.like else 'Dislike'} - {self.book.title}"
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[
        MinValueValidator(0.0), MaxValueValidator(5.0)
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title} - {self.rating}"
    

class Cart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('book', 'user')

    def price(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.user.username}'s cart"
    
    @classmethod
    def total_items(cls, user):
        return cls.objects.filter(user=user).count()
    
    @classmethod
    def total_cost(cls, user):
        return sum([cart.book.price * cart.quantity for cart in cls.objects.filter(user=user)])