from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name = 'blog'),
    path('add_article/', views.add_article, name = 'add_article'), 
    path('articles/<int:id>/', views.article_detail, name = 'article_detail'),
    path('edit_article/<int:id>/', views.edit_article, name = 'edit_article'),
    path('delete_article/<int:id>/', views.delete_article, name = 'delete_article'),
]
