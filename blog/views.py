from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from .models import BlogPost, StaticPage


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog/list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, 'blog/detail.html', {'post': post, 'related': related})


def static_page(request, page_type):
    page = get_object_or_404(StaticPage, page_type=page_type, is_published=True)
    lang = get_language() or 'lv'
    return render(request, 'blog/static_page.html', {
        'page': page,
        'title': page.get_title(lang),
        'content': page.get_content(lang),
    })
