from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
User=get_user_model()
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.PositiveBigIntegerField()
    message=models.TextField()
    
    def __str__(self) -> str:
        return f'{self.name} / {self.email}'

class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True,null=True)
    explanation=models.TextField()
    content=models.TextField()
    image=models.ImageField(upload_to="posts", null=True, blank=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    view_count=models.PositiveIntegerField(default=0)
    visible=models.BooleanField(default=True)
    time=models.DateField(auto_now_add=True)
    updated_time=models.DateField(auto_now=True)

    def get_absolute_url(self):
        return f'blog/article/{self.pk}'
    
        
    def __str__(self) -> str:
        return f'{self.title} / {self.owner}'

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def show_image(self):
        if self.image:
            return mark_safe(f"<img width=250 src={self.image.url}></img>")
        return mark_safe(f"<h3>Title of {self.title} is not found</h3>")
class ArticleImage(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="article_images")
    image=models.ImageField(upload_to=f"post_images")

    def __str__(self) -> str:
        return self.post.title

    @property
    def shows_image(self):
        if self.image:
            return mark_safe(f"<img width=200 src={self.image.url}></img>")
        return mark_safe(f"<h3>Image does'nt exists for {self.post.title}</h3>")