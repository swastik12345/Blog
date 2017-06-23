from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
# Create your models here


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title= models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.FileField(null=True,blank=True)
    content=models.TextField()
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug" : self.slug})
        #return "/blogs/%s/" %(self.id)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

def pre_save_post_recevier(sender, instance, *args , **kwargs):
    slug=slugify(instance.title)

    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" %(slug, instance.id)
    instance.slug = slug


pre_save.connect( pre_save_post_recevier , sender=Post)