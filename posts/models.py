from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="fallback.png", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the initial slug
            self.slug = slugify(self.title)
            # Check if a post with this slug already exists
            original_slug = self.slug
            queryset = Post.objects.filter(slug=self.slug).exists()
            counter = 1
            
            # If the slug exists, append a number to the slug until it's unique
            while queryset:
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Post.objects.filter(slug=self.slug).exists()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title