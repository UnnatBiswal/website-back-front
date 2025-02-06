from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

User = get_user_model()

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Scripture(models.Model):
    title = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    scripture = models.ForeignKey(Scripture, related_name='chapters', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'scripture',)

    def __str__(self):
        return f"{self.scripture.title} - Chapter {self.title}"

class ScriptureImage(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scripture_images/')
    pdf_file = models.FileField(upload_to='scripture_pdfs/', null=True, blank=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.chapter.scripture.title} - Chapter {self.chapter.title} - Image {self.id}"

    