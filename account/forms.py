from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,BlogPost,BlogCategory

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea, required=True)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2', 'address', 'user_type')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']