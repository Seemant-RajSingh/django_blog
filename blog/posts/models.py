from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import os

# Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default='Empty, no content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # New field

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the post already exists in the database
        if self.pk:
            old_post = Post.objects.get(pk=self.pk)
            if old_post.image and self.image != old_post.image:
                # Delete the old image file if it's being replaced
                if os.path.isfile(old_post.image.path):
                    os.remove(old_post.image.path)

        # Call the parent class's save method to save the object
        super().save(*args, **kwargs)
