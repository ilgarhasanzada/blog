from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .forms import ContactForm,PostForm
from .models import Post
from django.contrib.auth import get_user_model
from django.db.models import Avg,Max,Min,Sum
User=get_user_model()
# Create your views here.
def home(request):
    return render(request,'pages/home.html')
def contact(request):
    form = ContactForm()
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request,'pages/contact.html',{"form":form})

def search(request):
    authors=User.objects.all()
    posts=Post.objects.filter(title__contains=request.GET["search"])
    paginator=Paginator(posts,2)
    page_number=request.GET.get("page")
    post_obg=paginator.get_page(page_number)
    post_statistics=Post.objects.aggregate(min=Min('view_count'),max=Max('view_count'),sum=Sum('view_count'),avg=Avg('view_count'))
    post_count=Post.objects.all().count
    min_view_post=Post.objects.filter(view_count=Post.objects.aggregate(min=Min("view_count"))["min"])
    max_view_post=Post.objects.filter(view_count=Post.objects.aggregate(max=Max("view_count"))["max"])
    
    return render(request,'pages/blog.html',{"posts":post_obg,"authors":authors,"post_statistics":post_statistics,"article_count":post_count,"min_view_article":min_view_post,"max_view_article":max_view_post})

def blog(request,user_id=None):
    if not request.user.is_authenticated:
        return redirect("login")
    if user_id is not None:
        author=User.objects.get(id=user_id)
        posts=Post.objects.filter(owner=author)
        paginator=Paginator(posts,2)
        page_number=request.GET.get("page")
        post_obg=paginator.get_page(page_number)
    else:
        posts=Post.objects.all()
        paginator=Paginator(posts,2)
        page_number=request.GET.get("page")
        post_obg=paginator.get_page(page_number)
    authors=User.objects.all()
    post_statistics=Post.objects.aggregate(min=Min('view_count'),max=Max('view_count'),sum=Sum('view_count'),avg=Avg('view_count'))
    post_count=Post.objects.all().count
    min_view_post=Post.objects.filter(view_count=Post.objects.aggregate(min=Min("view_count"))["min"])
    max_view_post=Post.objects.filter(view_count=Post.objects.aggregate(max=Max("view_count"))["max"])
    return render(request,'pages/blog.html',{"posts":post_obg,"authors":authors,"post_statistics":post_statistics,"article_count":post_count,"min_view_article":min_view_post,"max_view_article":max_view_post})

def post(request,id):
    post=Post.objects.get(pk=id)
    post.view_count+=1
    post.save()
    other_posts=Post.objects.filter(owner=post.owner).exclude(id=id)
    return render(request,'pages/post.html',{"post":post,"other_posts":other_posts})
def edit_article(request, id):
    post=Post.objects.get(pk=id)
    form=PostForm(instance=post)
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.owner=request.user
            post.save()
            return redirect(request.path)
    return render(request,'pages/edit_post.html',{"form":form})

def add_article(request):
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.owner=request.user
            post.save()
            return redirect("add_article")
    return render(request,'pages/add_article.html',{"form":form})

def delete_article(request,id):
    post=Post.objects.get(pk=id)
    post.delete()
    return redirect("blog")