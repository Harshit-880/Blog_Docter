from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('my-posts/', views.my_blog_posts, name='my_blog_posts'),
    path('view/', views.view_blog_posts, name='view_blog_posts'),
     path('doctor/draft-blogs/', views.doctor_draft_blogs, name='doctor_draft_blogs'),
    path('update-blog-post/<int:post_id>/', views.update_blog_post, name='update_blog_post'),
    path('add_category/', views.add_category, name='add_category'),
    # path('view/category/<int:category_id>/', views.view_blog_posts_by_category, name='view_blog_posts_by_category'),
]
