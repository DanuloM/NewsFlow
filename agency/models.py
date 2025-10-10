from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls.base import reverse


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='newspapers')
    publishers = models.ManyToManyField(Redactor, related_name='newspapers')

    class Meta:
        ordering = ["-published_date"]

    def get_absolute_url(self):
        return reverse("agency:newspaper-detail", args=[str(self.id)])


    def __str__(self):
        return f"{self.title} (Topic: {self.topic})"
