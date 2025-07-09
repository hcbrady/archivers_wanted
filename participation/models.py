from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('project', 'project'),
        ('skill', 'skill'),
        ('interest', 'interest'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if self.category:
            self.category = self.category.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class OpportunityManager(models.Manager):
    def not_defunct(self):
        return self.filter(defunct=False)

class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    summary = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='opportunities')
    defunct = models.BooleanField(default=False)
    objects = OpportunityManager()

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
