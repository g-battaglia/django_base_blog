from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
# TinyMCE
from tinymce import models as tinymce_models


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

    def __str__(self):
        return self.title + " - " + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    
