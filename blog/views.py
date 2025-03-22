from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.forms import CommentForm
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
    posts = Paginator(posts,4)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts':posts}
    return render(request,'blog/blog.html', context) 

def single_view (request,pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'your comment submitted succesfully.')
        else:
            messages.add_message(request,messages.ERROR,'your comment didn\'t submit.')
    form = CommentForm()
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=1)
    post = get_object_or_404(posts,pk=pid)
    if not post.login_require:
        comments = Comment.objects.filter(post=post.id,approved=True)
        all_posts = Post.objects.filter(published_date__lte=timezone.now(),status=1).order_by('published_date')
        current_index = list(all_posts).index(post)
        previous_post = all_posts[current_index - 1] if current_index > 0 else None
        next_post = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
        post.counted_views += 1  
        post.save()
        context = {
            'post' :post,
            'previous_post' :previous_post,
            'next_post' :next_post,
            'comments' : comments,
            'form' : form
            }
        return render(request,'blog/single-blog.html',context) 
    else:
        return HttpResponseRedirect(reverse('accounts:login'))

def blog_category (request,cat_name):
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request,'blog/blog.html',context) 

def blog_search(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(),status=1)
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts':posts}
    return render(request,'blog/blog.html',context)