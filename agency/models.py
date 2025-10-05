from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor)

    def __str__(self):
        return f"{self.title} (Topic: {self.content})"
