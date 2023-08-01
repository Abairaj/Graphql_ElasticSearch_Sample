from django.db import models

# Create your models here.


class Author(models.Model):
    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    name = models.CharField(max_length=250)
    place = models.CharField(max_length=250)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICE)
    nationality = models.CharField(max_length=150)


class Categories(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()


class Books(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        Author, related_name='author', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Categories, related_name='categories', on_delete=models.CASCADE)

    price = models.PositiveIntegerField()
    description = models.TextField()
