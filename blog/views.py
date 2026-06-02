from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog/list.html', {'posts': posts})


def blog_detail(request, slug):
    post  = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, 'blog/detail.html', {'post': post, 'related': related})
