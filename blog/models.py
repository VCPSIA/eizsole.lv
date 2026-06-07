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


class StaticPage(models.Model):
    PAGE_TYPES = [
        ('privacy', 'Privātuma politika'),
        ('terms',   'Lietošanas noteikumi'),
        ('faq',     'Jautājumi un atbildes'),
    ]
    page_type   = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True, verbose_name='Lapas veids')
    title_lv    = models.CharField(max_length=200, verbose_name='Virsraksts (LV)')
    title_ru    = models.CharField(max_length=200, blank=True, verbose_name='Virsraksts (RU)')
    title_en    = models.CharField(max_length=200, blank=True, verbose_name='Virsraksts (EN)')
    title_de    = models.CharField(max_length=200, blank=True, verbose_name='Virsraksts (DE)')
    content_lv  = models.TextField(verbose_name='Saturs (LV)', help_text='HTML atbalstīts')
    content_ru  = models.TextField(blank=True, verbose_name='Saturs (RU)')
    content_en  = models.TextField(blank=True, verbose_name='Saturs (EN)')
    content_de  = models.TextField(blank=True, verbose_name='Saturs (DE)')
    is_published = models.BooleanField(default=True, verbose_name='Publicēts')
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Statiska lapa'
        verbose_name_plural = 'Statiskas lapas'

    def __str__(self):
        return self.get_page_type_display()

    def get_title(self, lang='lv'):
        return getattr(self, f'title_{lang}', None) or self.title_lv

    def get_content(self, lang='lv'):
        return getattr(self, f'content_{lang}', None) or self.content_lv


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
