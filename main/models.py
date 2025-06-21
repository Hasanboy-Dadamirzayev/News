from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Newletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    intro = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    author = models.CharField(max_length=55)
    reading_time = models.DurationField()
    view = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    comments = models.PositiveSmallIntegerField(default=0)

    objects = models.Manager()
    publisheds = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        if self.important:
            Article.objects.filter(important=True).exclude(pk=self.pk).update(important=False)

        super().save(*args, **kwargs)


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='article/{article.slug}/contents', blank=True, null=True)

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        if not self.text and not self.image:
            raise ValidationError('Kamida text yoki rasm bolishi shart')
        super().save(*args, **kwargs)

class Moment(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=55)
    photo = models.ImageField(upload_to='media/moment')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    published = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return f"{self.name}'s comment"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.phone and not self.email:
            raise ValidationError('Iltimos telefon raqam yoki emailingizni kiriting!')

    def __str__(self):
        return self.name



