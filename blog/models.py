from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_abolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        'blog.Categories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
