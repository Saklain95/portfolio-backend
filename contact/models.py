from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d %H:%M}"