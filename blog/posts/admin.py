from django.contrib import admin
from .models import Post

# Custom admin class for Post model
class PostAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'created_at', 'updated_at')
    # Fields to search through
    search_fields = ('title', 'content')
    # Optionally, you can add filters
    list_filter = ('author', 'created_at')

# Register the Post model with the custom admin class
admin.site.register(Post, PostAdmin)
