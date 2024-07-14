
from django.contrib import admin
from .models import CustomUser,BlogCategory,BlogPost

admin.site.register(CustomUser)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
