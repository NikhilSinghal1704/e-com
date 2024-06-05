import random
from django.core.management.base import BaseCommand
from Website.models import Book, Review
from Auth.models import CustomUser as User


class Command(BaseCommand):
    help = 'Populate ratings for all books at random'

    def handle(self, *args, **kwargs):
        books = Book.objects.all()

        for book in books:
            # Randomly generate a rating between 0 and 5
            rating = round(random.uniform(0, 5), 1)

            # Create a review for the book with the generated rating
            Review.objects.create(
                book=book,
                user=User.objects.first(),  # You may want to change this to assign different users to each review
                message="Randomly generated review",
                rating=rating
            )

            self.stdout.write(self.style.SUCCESS(f"Rating generated for {book.title}: {rating}"))