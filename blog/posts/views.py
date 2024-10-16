from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post


def index(request):
    return render(request, 'home.html')


def posts(request):
    all_posts = Post.objects.all()  # Load all posts from the database
    return render(request, 'posts.html', {'posts': all_posts})

def post(request, pk):
    single_post = Post.objects.get(id=pk)  # Load individual post by ID
    return render(request, 'post.html', {'post': single_post})


# Login
def login(request):
    if request.user.is_authenticated:
        return redirect('posts')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('posts')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Registration successful!')  # Success message
            return redirect('/login')  # Redirect to login after successful registration
        except Exception as e:
            messages.error(request, 'Registration failed! Please try again.')  # Error message
            return redirect('/login')  # Redirect back to login page

    return redirect('/login')  # Redirect if not a POST request

# Logout
def logout_view(request):
    logout(request)
    return redirect('index')


def createpost(request):
    return render(request, 'createpostform.html')


def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')  # Get uploaded file

        post = Post(
            title=title,
            content=content,
            author=request.user,  # Set the current user as the author
            image=image
        )
        post.save()  # Save the new post to the database

        messages.success(request, 'Post created successfully!')  # Success message
        return redirect('posts')  # Redirect to posts page after creation

    return render(request, 'createpostform.html')


def editpost(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('post', pk=pk)  # Redirect if not the author

    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        if request.FILES.get('image'):
            post.image = request.FILES['image']
        post.save()
        return redirect('post', pk=pk)

    return render(request, 'editpostform.html', {'post': post})

def deletepost(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure only the author can delete the post
    if request.user != post.author:
        return redirect('post', pk=pk)  # Redirect if not the author

    # Delete the post and redirect to the posts list
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('posts')
