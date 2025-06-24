from django.db import models
from ckeditor.fields import RichTextField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    summary = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='opportunities')

    def __str__(self):
        return self.title
    
    def tag_list(self):
        return ", ".join(tag.name for tag in self.tags.all())
