from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path('blog/',views.blog, name='blog'),
    path('blog/user/<int:user_id>/',views.blog, name='user_blog'),
    path('blog/search/',views.search,name="search"),
    path('blog/article/<int:id>/',views.post, name='post'),
    path('add_article/',views.add_article, name='add_article'),
    path('edit_article/<int:id>/',views.edit_article, name='edit_article'),
    path('delete_article/<int:id>/',views.delete_article, name='delete_article'),
]
