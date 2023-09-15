from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogView, BlogDeleteView, BlogUserListView, BlogListView, BlogUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/create/', BlogCreateView.as_view(), name='create_blog'),
    path('blog/<slug:slug>', BlogView.as_view(), name='view_blog'),
    path('blog/delete/<slug:slug>', BlogDeleteView.as_view(), name='delete_blog'),
    path('blogs/user/', BlogUserListView.as_view(), name='user_list_blog'),
    path('blogs/', BlogListView.as_view(), name='list_blog'),
    path('blog/update/<slug:slug>', BlogUpdateView.as_view(), name='update_blog'),
]
