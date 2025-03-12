from django.shortcuts import render

# Create your views here.

def home_view (request):
    return render(request,'blog/blog.html') 

def single_view (request):
    return render(request,'blog/single-blog.html') 