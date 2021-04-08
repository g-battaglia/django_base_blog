from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
# TinyMCE
from tinymce import models as tinymce_models
# Taggit
from taggit.managers import TaggableManager # Tags



# Create your models here.

class Post(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    body = tinymce_models.HTMLField()
    image = models.ImageField(
        upload_to='img/%Y/%m/%d/',
        blank=True,        
        )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        through='Comment', related_name='ad_comments')

    def __str__(self):
        return self.title + " - " + self.created_at.strftime("%m/%d/%Y, %H:%M")

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'
