from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.urls import reverse

User=get_user_model()

class Article(models.Model):
    title = models.CharField(max_length = 200)
    explanation = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to = "articles")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'articles')
    view_count = models.PositiveIntegerField(default = 0)
    is_visible = models.BooleanField(default = True)
    created_time = models.DateField(auto_now_add = True)
    updated_time = models.DateField(auto_now = True)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'id': self.pk})
        
    def __str__(self) -> str:
        return f'{self.title} / {self.owner}'

    @property
    def image_detail(self):
        if self.image:
            return mark_safe(f"<img width=250 src={self.image.url}></img>")
        return mark_safe(f"<h3>Title of {self.title} is not found</h3>")
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name = "article_images")
    image = models.ImageField(upload_to = "article_images")

    def __str__(self) -> str:
        return self.article.title

    @property
    def image_detail(self):
        if self.image:
            return mark_safe(f"<img width=200 src={self.image.url}></img>")
        return mark_safe(f"<h3>Image does'nt exists for {self.article.title}</h3>")