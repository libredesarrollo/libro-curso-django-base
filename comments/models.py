from django.db import models

from elements.models import Element

# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self) -> str:
        return 'Comment #{}'.format(self.id)