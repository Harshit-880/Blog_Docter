from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.db.models import Prefetch
from .models import BlogPost, BlogCategory
from .forms import BlogPostForm,BlogCategoryForm

def home_view(request):
    return render(request, 'account/home.html')

@method_decorator(csrf_exempt, name='dispatch')
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        print("POST request received")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("User authenticated and logged in")
                return redirect('dashboard')  # Change 'dashboard' to the appropriate URL name for your dashboard
            else:
                print("Invalid login credentials")
                messages.error(request, "Invalid username or password")
        else:
            print("Form is not valid")
            messages.error(request, "Invalid form data")
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.user_type == 'patient':
        return render(request, 'account/patient_dashboard.html')
    elif request.user.user_type == 'doctor':
        return render(request, 'account/doctor_dashboard.html')
    else:
        return redirect('login')



@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'account/create_blog_post.html', {'form': form})
@login_required
def my_blog_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'account/my_blog_posts.html', {'posts': posts})

@login_required
def view_blog_posts(request):
    if request.user.user_type == 'doctor':
        # Doctors see all their posts
        categories = BlogCategory.objects.prefetch_related(
            Prefetch('blogpost_set', queryset=BlogPost.objects.filter(author=request.user))
        )
    else:
        # Patients see all non-draft posts
        categories = BlogCategory.objects.prefetch_related(
            Prefetch('blogpost_set', queryset=BlogPost.objects.filter(is_draft=False))
        )

    return render(request, 'account/view_blog_posts.html', {
        'categories': categories,
    })


@login_required
def doctor_draft_blogs(request):
    draft_posts = BlogPost.objects.filter(author=request.user, is_draft=True)
    return render(request, 'account/doctor_draft_blogs.html', {'draft_posts': draft_posts})


@login_required
def update_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'account/update_blog_post.html', {'form': form, 'post': post})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to doctor dashboard after adding category
    else:
        form = BlogCategoryForm()
    return render(request, 'account/add_category.html', {'form': form})
# @login_required
# def view_blog_posts_by_category(request, category_id):
#     category = BlogCategory.objects.get(id=category_id)
#     posts = BlogPost.objects.filter(category=category, is_draft=False)
#     return render(request, 'account/view_blog_posts_by_category.html', {'category': category, 'posts': posts})
