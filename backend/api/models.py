from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=50)
    published_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book/%Y/%m', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.available_copies = self.quantity
        super().save(*args, **kwargs)


def default_due_date():
    return timezone.now() + timedelta(days=14)


class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=14))
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('BORROWED', 'Borrowed'), ('RETURNED', 'Returned')],
        default='BORROWED'
    )

    def save(self, *args, **kwargs):
        if self.pk:
            previous = BorrowRecord.objects.get(pk=self.pk)
            if previous.status == 'BORROWED' and self.status == 'RETURNED':
                self.return_date = timezone.now()
                self.book.available_copies += 1
                self.book.save()
            elif previous.status == 'RETURNED' and self.status == 'BORROWED':
                self.return_date = None
                if self.book.available_copies > 0:
                    self.book.available_copies -= 1
                    self.book.save()
        else:
            if self.status == 'RETURNED':
                self.return_date = timezone.now()
                self.book.available_copies += 1
            else:  # BORROWED
                if self.book.available_copies > 0:
                    self.book.available_copies -= 1
            self.book.save()

        super().save(*args, **kwargs)
