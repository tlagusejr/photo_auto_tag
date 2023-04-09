'''Photoapp Models'''

from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from taggit.managers import TaggableManager

class CustomTaggableManager(TaggableManager):
    def add(self, *tags):
        super().add(*tags)
        # 추가 작업 수행

    def remove(self, *tags):
        super().remove(*tags)
        # 삭제 작업 수행

class Photo(models.Model):
    
    title = models.CharField(max_length=45)
    
    description = models.CharField(max_length=250) 

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = CustomTaggableManager()

    #file_name = models.CharField(max_length=45)

    def __str__(self):
        return self.title