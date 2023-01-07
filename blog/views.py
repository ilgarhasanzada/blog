from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import ArticleForm
from .models import Article
from django.contrib.auth import get_user_model
from django.db.models import Avg,Max,Min,Sum
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Q
User=get_user_model()

@login_required
def blog(request):
    user_id = request.GET.get('author')
    search=request.GET.get('search')
    if user_id:
        author = User.objects.get(id = user_id)
        if author == request.user:
            articles = Article.objects.filter(owner = author)
        else:
            articles = Article.objects.filter(owner = author,is_visible = True)
        paginator = Paginator(articles,2)
        page_number = request.GET.get("page")
        article_obg = paginator.get_page(page_number)
    elif search:
        articles1 = Article.objects.filter(owner = request.user,title__contains = request.GET["search"])
        articles2 = Article.objects.exclude(owner = request.user).filter(is_visible = True,title__contains = request.GET["search"])
        articles = articles1 | articles2
        paginator = Paginator(articles,2)
        page_number = request.GET.get("page")
        article_obg = paginator.get_page(page_number)
    else:
        # articles1 = Article.objects.filter(owner = request.user)
        # articles2 = Article.objects.exclude(owner = request.user).filter(is_visible = True)
        # articles = articles1 | articles2
        articles = Article.objects.filter(Q(is_visible=True) | Q(owner = request.user))
        paginator = Paginator(articles,2)
        page_number = request.GET.get("page")
        article_obg = paginator.get_page(page_number)
    authors = User.objects.all()
    article_statistics = Article.objects.aggregate(min = Min('view_count'),max = Max('view_count'),sum = Sum('view_count'),avg = Avg('view_count'))
    article_count = Article.objects.filter(is_visible = True).count
    min_view_article = Article.objects.filter(view_count = Article.objects.aggregate(min = Min("view_count"))["min"])
    max_view_article = Article.objects.filter(view_count = Article.objects.aggregate(max = Max("view_count"))["max"])
    return render(request,'blog.html', {"article_obg": article_obg,"authors": authors, "article_statistics": article_statistics, "article_count": article_count, "min_view_article": min_view_article, "max_view_article": max_view_article})

@login_required
def article_detail(request, id):
    article = Article.objects.get(pk = id)
    if not article.is_visible and article.owner != request.user:
        return redirect('home')
    article.view_count += 1
    article.save()
    other_articles = Article.objects.filter(owner = article.owner).exclude(id = id)
    print(other_articles)
    return render(request, 'article.html',{"article": article, "other_articles": other_articles})

@permission_required('user')
@login_required
def edit_article(request, id):
    article = Article.objects.get(pk = id)
    form = ArticleForm(instance = article)
    if request.method == "POST":
        form=ArticleForm(request.POST, request.FILES, instance = article)
        if form.is_valid():
            article = form.save(commit=False)
            article.owner = request.user
            article.save()
            return redirect(request.path)
    return render(request, 'edit_article.html', {"form": form})

@login_required
def add_article(request):
    form=ArticleForm()
    if request.method == "POST":
        form=ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article=form.save(commit = False)
            article.owner = request.user
            article.save()
            return redirect("add_article")
    return render(request, 'add_article.html',{"form": form})

@permission_required('user')
@login_required
def delete_article(request, id):
    article = Article.objects.get(pk = id)
    article.delete()
    return redirect("blog")