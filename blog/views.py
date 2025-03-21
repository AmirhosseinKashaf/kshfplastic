from django.shortcuts import render
from blog.models import Post,Comment
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# from blog.forms import CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def home_view (request,**kwargs):
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=1)
    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    posts = Paginator(posts,2)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts':posts}
    return render(request,'blog/blog.html', context) 

def single_view (request):
    return render(request,'blog/single-blog.html') 