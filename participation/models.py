from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('project', 'Project'),
        ('skill', 'Skill'),
        ('interest', 'Interest'),
    ]
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='interest')

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
    
    def get_absolute_url(self):
        return reverse('opportunity_detail', kwargs={'pk': self.pk})

class TagSubscription(models.Model):
    email = models.EmailField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.email} subscribed to {[tag.name for tag in self.tags.all()]}"
    def tag_list(self):
        return ", ".join(tag.name for tag in self.tags.all())
