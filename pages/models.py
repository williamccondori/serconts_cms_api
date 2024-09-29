from django.db import models

# Create your models here.

class Page(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.page)