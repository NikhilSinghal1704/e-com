from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone_no = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/person.png')

    def save(self, *args, **kwargs):
        try:
            # Get the existing instance of this user to check the old profile_pic
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.profile_pic and old_instance.profile_pic != self.profile_pic:
                # If there's an existing profile_pic and it's different from the new one, delete the old file
                old_instance.profile_pic.delete(save=False)
        except CustomUser.DoesNotExist:
            # If the user doesn't exist yet, proceed as usual
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_pic:
            self.profile_pic.delete(save=False)
        super().delete(*args, **kwargs)

    def cart_total(self):
        return sum([item.book.price * item.quantity for item in self.cart_set.all()])