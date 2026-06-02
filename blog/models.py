from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def lv_slugify(text):
    replacements = {
        'ā': 'a', 'č': 'c', 'ē': 'e', 'ģ': 'g', 'ī': 'i',
        'ķ': 'k', 'ļ': 'l', 'ņ': 'n', 'š': 's', 'ū': 'u', 'ž': 'z',
    }
    text = text.lower()
    for lv, en in replacements.items():
        text = text.replace(lv, en)
    return slugify(text)


class BlogPost(models.Model):
    title            = models.CharField(max_length=200)
    slug             = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt          = models.CharField(max_length=300)
    content          = models.TextField()
    image            = models.ImageField(upload_to='blog/', blank=True, null=True)
    author           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords    = models.CharField(max_length=500, blank=True)
    is_published     = models.BooleanField(default=True)
    published_at     = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Raksts'
        verbose_name_plural = 'Raksti'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = lv_slugify(self.title)
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)
