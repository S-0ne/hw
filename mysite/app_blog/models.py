import random
from django.db import models
from django.utils import timezone
from django.urls import reverse

def random_number():
    return random.randint(1, 100)

class Category(models.Model):
    name = models.CharField(u'Категорія', max_length=250, help_text=u'Максимум 250 символів')
    slug = models.SlugField(u'Слаг')

    class Meta:
        verbose_name = u'Категорія'
        verbose_name_plural = u'Категорії'

    def str(self):
        return self.name

class Article(models.Model):
    title = models.CharField(u'Заголовок', max_length=250, help_text=u'Максимум 250 сим.')
    description = models.TextField(blank=True, verbose_name=u'Опис')
    pub_date = models.DateTimeField(u'Дата публікації', default=timezone.now)
    slug = models.SlugField(u'Слаг', unique_for_date='pub_date')
    main_page = models.BooleanField(u'Головна', default=True, help_text=u'Показувати на головній сторінці')
    category = models.ForeignKey(Category, related_name='articles', blank=True, null=True, verbose_name=u'Категорія', on_delete=models.CASCADE)
    random_number = models.IntegerField(u'Рандомне число', default=random_number)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = u'Стаття'
        verbose_name_plural = u'Статті'

    def str(self):
        return self.title

    def get_absolute_url(self):
        try:
            url = reverse('news-detail', kwargs={
                'year': self.pub_date.strftime("%Y"),
                'month': self.pub_date.strftime("%m"),
                'day': self.pub_date.strftime("%d"),
                'slug': self.slug,
            })
        except:
            url = "/"
        return url

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, verbose_name=u'Стаття', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(u'Фото', upload_to='photos')
    caption = models.CharField(u'Підпис', max_length=250, help_text=u'Максимум 250 сим.', blank=True)

    class Meta:
        verbose_name = u'Зображення статті'
        verbose_name_plural = u'Зображення статті'

    def str(self):
        return self.caption

    @property
    def filename(self):
        if self.image and self.image.name:
            return self.image.name.rsplit('/', 1)[-1]
        return ''